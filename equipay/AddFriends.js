import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const AddFriends = ({ navigation }) => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      setLoading(true);
      const sessionKey = await AsyncStorage.getItem('sessionKey');
      const token = await AsyncStorage.getItem('jwt_token');

      if (!sessionKey || !token) {
        Alert.alert('Error', 'Missing session key or token');
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get('http://127.0.0.1:5000/listUsers', {
          headers: {
            'Authorization': `Bearer ${token}`,
            'Session-Key': sessionKey,
          },
        });
        // Assume response data is an array of arrays or objects
        const transformedData = response.data.map(user => ({
          id: user[0], // Adjust these indices according to your actual data structure
          name: user[1],
          email: user[3],
        }));
        setUsers(transformedData);
      } catch (error) {
        console.error('Error fetching users:', error);
        Alert.alert('Error', 'Failed to fetch users');
      } finally {
        setLoading(false);
      }
    };

    fetchUsers();
  }, []);

  const handleAddFriend = (user) => {
    Alert.alert(
      "Add Friend",
      `Do you really want to add ${user.name} to your friend list?`,
      [
        { text: "Cancel", style: "cancel" },
        { text: "Yes", onPress: () => sendFriendRequest(user.id) }
      ]
    );
  };

  const sendFriendRequest = async (friendId) => {
    const sessionKey = await AsyncStorage.getItem('sessionKey');
    const token = await AsyncStorage.getItem('jwt_token');
  
    // Ensure you have retrieved the friendId correctly and it's not undefined
    if (!friendId) {
      console.error('Friend ID is undefined');
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
      } else {
        throw new Error(`Failed to send friend request: Status Code ${response.status}`);
      }
    } catch (error) {
      console.error('Error sending friend request:', error);
      Alert.alert('Error', 'Failed to send friend request');
    }
  };
  
  const renderItem = ({ item }) => (
    <TouchableOpacity style={styles.item} onPress={() => handleAddFriend(item)}>
      <Text style={styles.title}>{item.name} ({item.email})</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {loading ? (
        <Text>Loading...</Text>
      ) : (
        <FlatList
          data={users}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
          contentContainerStyle={styles.list}
        />
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
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  title: {
    fontSize: 18,
  },
  list: {
    paddingBottom: 10,
  }
});

export default AddFriends;
