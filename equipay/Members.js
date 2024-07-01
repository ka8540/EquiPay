import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, Alert, StyleSheet } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useNavigation, useRoute } from '@react-navigation/native';

const Members = () => {
  const [friends, setFriends] = useState([]);
  const navigation = useNavigation();
  const route = useRoute();
  const { group_id } = route.params;

  useEffect(() => {
    fetchFriends();
  }, []);

  const fetchFriends = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token) {
      Alert.alert("Error", "JWT token not found");
      return;
    }
    try {
      const response = await axios.get('http://127.0.0.1:5000/friends', {
        headers: { Authorization: `Bearer ${token}` }
      });
      // Transform the data from array of arrays to array of objects
      const transformedFriends = response.data.map(friend => ({
        id: friend[0].toString(), // Ensure the ID is a string for keyExtractor
        name: friend[1]
      }));
      setFriends(transformedFriends);
    } catch (error) {
      console.log(error);
      Alert.alert("Error", "Failed to fetch friends");
    }
  };

  const addMember = async (friendId) => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token) {
      Alert.alert("Error", "Authentication token not found");
      return;
    }
    try {
      const response = await axios.put(`http://127.0.0.1:5000/add_group_member/${group_id}`, { friend_id: friendId }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.status === 200) {
        navigation.goBack();
      } else if (response.status === 201) {
        Alert.alert("Limit Reached", "You cannot add more members as the group limit is reached.");
      }else if (response.status === 202) {
        Alert.alert("Aready a Member", "Member alreay exist in the group.");
      }
    } catch (error) {
      console.log(error);
      Alert.alert("Error", "Failed to add member");
    }
  };

  return (
    <View style={styles.container}>
      <FlatList
        data={friends}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.friendItem} onPress={() => addMember(item.id)}>
            <Text style={styles.friendName}>{item.name}</Text>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f0f0f0',
  },
  friendItem: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
    backgroundColor: 'white',
  },
  friendName: {
    fontSize: 18,
    color: '#333',
  }
});

export default Members;
