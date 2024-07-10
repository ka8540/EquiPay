import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Alert, Button } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Contacts from 'expo-contacts';

const AddFriends = ({ navigation }) => {
  const [users, setUsers] = useState([]);
  const [pendingRequests, setPendingRequests] = useState([]);
  const [matchedContacts, setMatchedContacts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    fetchDeviceContacts();
  }, []);

  const fetchDeviceContacts = async () => {
    const { status } = await Contacts.requestPermissionsAsync();
    if (status === 'granted') {
      const { data } = await Contacts.getContactsAsync({
        fields: [Contacts.Fields.Emails, Contacts.Fields.PhoneNumbers, Contacts.Fields.Name],
      });

      if (data.length > 0) {
        const deviceContacts = data.map(contact => ({
          id: contact.id,
          name: contact.name,
          email: contact.emails?.[0]?.email,
          phoneNumber: normalizePhoneNumber(contact.phoneNumbers?.[0]?.number),
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

      const response = await axios.get('http://127.0.0.1:5000/contact_list', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });

      const serverContacts = response.data.map(contact => ({
        firstname: contact.firstname,
        phoneNumber: normalizePhoneNumber(contact.contact)
      }));

      console.log("Contacts:", serverContacts);
      const matchedContacts = deviceContacts.filter(deviceContact =>
        serverContacts.some(serverContact => serverContact.phoneNumber === deviceContact.phoneNumber)
      ).map(matchedContact => ({
        ...matchedContact,
        firstname: serverContacts.find(serverContact => serverContact.phoneNumber === matchedContact.phoneNumber)?.firstname
      }));

      console.log("deviceContacts:", deviceContacts);
      console.log("Matched Contacts:", matchedContacts);
      setMatchedContacts(matchedContacts);
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
      const userResponse = await axios.get('http://127.0.0.1:5000/listUsers', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });

      const pendingResponse = await axios.get('http://127.0.0.1:5000/addFriend', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });

      const transformedUsers = userResponse.data.map(user => ({
        id: user[0], 
        name: user[1],
        email: user[3],
      }));

      const transformedRequests = pendingResponse.data.map((user, index) => ({
        id: user[0],
        name: user[1],
      }));

      setUsers(transformedUsers);
      setPendingRequests(transformedRequests);
    } catch (error) {
      console.error('Error fetching data:', error);
      Alert.alert('Error', 'Failed to fetch data');
    } finally {
      setLoading(false);
    }
  };

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

  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.item} onPress={() => handleAddFriend(item)}>
      <Text style={styles.title}>{item.firstname || item.name}</Text>
    </TouchableOpacity>
  );

  const handleAddFriend = (user) => {
    const matchedUser = users.find(u => u.name === user.firstname);
    const userId = matchedUser ? matchedUser.id : null;
    if (!userId) {
      Alert.alert('Error', 'User ID not found');
      return;
    }

    Alert.alert(
      "Add Friend",
      `Do you really want to add ${user.name} to your friend list?`,
      [
        { text: "Cancel", style: "cancel" },
        { text: "Yes", onPress: () => sendFriendRequest(userId) }
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

  const renderPendingRequestItem = ({ item }) => (
    <View style={styles.item}>
      <Text style={styles.title}>{item.name}</Text>
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
            keyExtractor={(item) => item.id.toString()}
            renderItem={renderItem}
            contentContainerStyle={styles.list}
          />
          <Text style={styles.header}>Pending Request</Text>
          <FlatList
            data={pendingRequests}
            keyExtractor={(item) => item.id}
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
