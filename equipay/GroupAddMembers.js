import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, FlatList, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { useNavigation } from '@react-navigation/native';

const GroupAddMembers = () => {
  const [groupName, setGroupName] = useState('');
  const [profilePictureUrl, setProfilePictureUrl] = useState('');
  const [friends, setFriends] = useState([]);
  const [selectedFriends, setSelectedFriends] = useState([]);
  const navigation = useNavigation();

  useEffect(() => {
    fetchFriends();
  }, []);

  const fetchFriends = async () => {
    try {
      const token = await AsyncStorage.getItem('jwt_token');
      if (!token) {
        Alert.alert("Error", "Authentication token is not available");
        return;
      }
      const response = await axios.get('http://127.0.0.1:5000/friends', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      console.log("Fetched friends:", response.data); // Verify the data structure
      const transformedFriends = response.data.map(friend => ({
        id: friend[0].toString(), // Assuming the ID is the first element
        name: friend[1], // Assuming the name is the second element
      }));
      console.log("Transformed friends:", transformedFriends);
      setFriends(transformedFriends);
    } catch (error) {
      Alert.alert("Error fetching friends", error.toString());
    }
  };

  const handleSelectFriend = id => {
    const isSelected = selectedFriends.includes(id);
    if (isSelected) {
      setSelectedFriends(currentIds => currentIds.filter(fid => fid !== id));
    } else if (selectedFriends.length < 4) {
      setSelectedFriends(currentIds => [...currentIds, id]);
    } else {
      Alert.alert("Limit Reached", "You can select up to 4 members only.");
    }
  };

  const createGroup = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token) {
      Alert.alert("Error", "Authentication token is not available");
      return;
    }
    try {
      const response = await axios.post('http://127.0.0.1:5000/create_group', {
        group_name: groupName,
        profile_picture_url: profilePictureUrl,
        friend_ids: selectedFriends,
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (response.status === 200) {
        Alert.alert("Success", "Group created successfully!");
        navigation.goBack();
      } else {
        throw new Error('Failed to create group');
      }
    } catch (error) {
      Alert.alert("Error creating group", error.message);
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Enter Group Name"
        value={groupName}
        onChangeText={setGroupName}
      />
      <FlatList
        data={friends}
        keyExtractor={item => item.id}
        renderItem={({ item }) => (
          <TouchableOpacity
            style={[styles.friendItem, { backgroundColor: selectedFriends.includes(item.id) ? '#d0ebff' : '#fff' }]}
            onPress={() => handleSelectFriend(item.id)}
          >
            <Text>{item.name}</Text>
          </TouchableOpacity>
        )}
      />
      <Button title="Create Group" onPress={createGroup} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    marginTop:70,
  },
  profilePicPlaceholder: {
    height: 100,
    width: 100,
    borderRadius: 50,
    backgroundColor: '#ddd',
    justifyContent: 'center',
    alignItems: 'center',
    alignSelf: 'center',
    marginBottom: 20,
  },
  profilePicText: {
    textAlign: 'center',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
  friendItem: {
    padding: 10,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
    marginBottom: 5,
  },
});

export default GroupAddMembers;
