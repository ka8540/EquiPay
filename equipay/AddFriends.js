import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Alert, Button } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Contacts from 'expo-contacts';

const AddFriends = ({ navigation }) => {
  const [matchedContacts, setMatchedContacts] = useState([]);
  const [pendingRequests, setPendingRequests] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    fetchDeviceContacts();
  }, []);

  const fetchDeviceContacts = async () => {
    const { status } = await Contacts.requestPermissionsAsync();
    if (status === 'granted') {
      const { data } = await Contacts.getContactsAsync({
        fields: [Contacts.Fields.Name, Contacts.Fields.PhoneNumbers],
      });

      if (data.length > 0) {
        const deviceContacts = data.map(contact => ({
          firstname: contact.name,
          contact: normalizePhoneNumber(contact.phoneNumbers?.[0]?.number),
        }));
        matchContacts(deviceContacts);
      }
    }
  };

  const normalizePhoneNumber = (phoneNumber) => {
    if (!phoneNumber) return '';
    return phoneNumber.replace(/[^\d]/g, '');
  };

  const matchContacts = async (deviceContacts) => {
    try {
      const sessionKey = await AsyncStorage.getItem('sessionKey');
      const token = await AsyncStorage.getItem('jwt_token');
  
      const batchSize = 50;
      for (let i = 0; i < deviceContacts.length; i += batchSize) {
        const batch = deviceContacts.slice(i, i + batchSize);
  
        const encodedContacts = encodeURIComponent(JSON.stringify(batch));
  
        const response = await axios.post('http://127.0.0.1:5000/contact_list', {}, {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Session-Key': sessionKey,
          },
          params: {
            contacts: encodedContacts,
          },
        });
  
        console.log(`Response Status: ${response.status}`, response.data);
  
        if (response.status === 201) {
          // Silently handle the 201 status
          continue;
        } else if (response.status === 200) {
          // Process and display first names if status is 200
          if (Array.isArray(response.data)) {
            const serverContacts = response.data.map(contact => ({
              user_id: contact[0],
              firstname: contact[1]
            }));
            console.log("Batch Response:", serverContacts);
            setMatchedContacts(prevContacts => [...prevContacts, ...serverContacts]); // Append new matched contacts
          }
        } else {
          // Handle other statuses
          console.error("Failed request:", response);
          Alert.alert('Error', `Unexpected server response with status: ${response.status}`);
        }
      }
  
    } catch (error) {
      console.error('Error matching contacts:', error);
      Alert.alert('Error', 'Failed to match contacts');
    }
  };
  
  
  const fetchData = async () => {
    setLoading(true);
    const sessionKey = await AsyncStorage.getItem('sessionKey');
    const token = await AsyncStorage.getItem('jwt_token');

    if (!sessionKey || !token) {
      Alert.alert('Error', 'Missing session key or token');
      setLoading(false);
      return;
    }

    try {
      const pendingResponse = await axios.get('http://127.0.0.1:5000/addFriend', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });

      const transformedRequests = pendingResponse.data.map(request => ({
        id: request[0],
        firstname: request[1],
      }));

      setPendingRequests(transformedRequests);
    } catch (error) {
      console.error('Error fetching data:', error);
      Alert.alert('Error', 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

  const handleAddFriend = (user) => {
    Alert.alert(
      "Add Friend",
      `Do you really want to add ${user.firstname} to your friend list?`,
      [
        { text: "Cancel", style: "cancel" },
        { text: "Yes", onPress: () => sendFriendRequest(user.user_id) }
      ]
    );
  };

  const sendFriendRequest = async (friendId) => {
    const sessionKey = await AsyncStorage.getItem('sessionKey');
    const token = await AsyncStorage.getItem('jwt_token');

    if (!friendId) {
      Alert.alert('Error', 'Friend ID is missing');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/addFriend', { friend_id: friendId }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });
      if (response.status === 200) {
        Alert.alert("Success", "Friend request sent successfully!");
        fetchData(); 
      }
    } catch (error) {
      if (error.response) {
        if (error.response.status === 409) {
          Alert.alert("Notice", "Friend request already sent.");
        } else {
          Alert.alert('Error', `Failed to send friend request: ${error.response.status}`);
        }
      } else {
        Alert.alert('Error', 'Failed to send friend request due to network or server issue');
      }
    }
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.item} onPress={() => handleAddFriend(item)}>
      <Text style={styles.title}>{item.firstname}</Text>
    </TouchableOpacity>
  );

  const handleResponse = async (friendId, action) => {
    const sessionKey = await AsyncStorage.getItem('sessionKey');
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.put('http://127.0.0.1:5000/addFriend', {
        friend_id: friendId, 
        action: action
      }, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });
      console.log("Response:", response);
      if (response.status === 200) {
        Alert.alert("Success", `Friend request ${action}ed successfully!`);
        setPendingRequests(prevRequests => 
          prevRequests.filter(req => req.id !== friendId)
        );
      }
    } catch (error) {
      Alert.alert('Error', `Failed to update friend request: ${error.response ? error.response.data.message : error.message}`);
    }
  };

  const renderPendingRequestItem = ({ item }) => (
    <View style={styles.item}>
      <Text style={styles.title}>{item.firstname}</Text>
      <Button title="Accept" onPress={() => handleResponse(item.id, 'accept')} />
      <Button title="Reject" onPress={() => handleResponse(item.id, 'reject')} />
    </View>
  );

  return (
    <View style={styles.container}>
      {loading ? (
        <Text>Loading...</Text>
      ) : (
        <>
          <Text style={styles.header}>People</Text>
          <FlatList
            data={matchedContacts}
            keyExtractor={(item) => item.user_id ? item.user_id.toString() : Math.random().toString()}
            renderItem={renderItem}
            contentContainerStyle={styles.list}
          />
          <Text style={styles.header}>Pending Requests</Text>
          <FlatList
            data={pendingRequests}
            keyExtractor={(item) => item.id ? item.id.toString() : Math.random().toString()}
            renderItem={renderPendingRequestItem}
            contentContainerStyle={styles.list}
          />
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
    backgroundColor: '#f5f5f5',
  },
  item: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  title: {
    fontSize: 18,
  },
  list: {
    paddingBottom: 10,
  },
  header: {
    fontSize: 20,
    fontWeight: 'bold',
    marginTop: 20,
  }
});

export default AddFriends;
