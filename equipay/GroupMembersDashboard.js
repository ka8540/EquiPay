import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Image, FlatList, StyleSheet, Alert } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';

const GroupMembersDashboard = () => {
  const [groupName, setGroupName] = useState('');
  const [groupImage, setGroupImage] = useState(null);
  const [members, setMembers] = useState([]);
  const navigation = useNavigation();
  const route = useRoute();
  const { group_id } = route.params;

  useEffect(() => {
    fetchGroupName(group_id);
    fetchGroupImage(group_id);
    fetchGroupMembers(group_id);

    // Set up a listener for when this screen is focused to refresh data
    const unsubscribe = navigation.addListener('focus', () => {
      // Re-fetch group image or other data as necessary
      fetchGroupImage(group_id);
    });

    return unsubscribe; // Cleanup listener on unmount
  }, [navigation, group_id]);

  const fetchGroupName = async (groupId) => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.get(`http://127.0.0.1:5000/group_name/${groupId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setGroupName(response.data.group_name);
    } catch (error) {
      Alert.alert("Error", "Failed to fetch group name");
    }
  };

  const fetchGroupImage = async (groupId) => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.get(`http://127.0.0.1:5000/group_photo/${groupId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.data.url && response.data.url.length > 0) {
        setGroupImage(response.data.url[0]); // Assuming the URL is the first element of the array
      } else {
        setGroupImage(null);
      }
    } catch (error) {
      console.log(error);
      setGroupImage(null); // Handle "Add photo" scenario more robustly
    }
  };

  const fetchGroupMembers = async (groupId) => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.get(`http://127.0.0.1:5000/group_members/${groupId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log("Resonse:",response.data);
      setMembers(response.data);
    } catch (error) {
      Alert.alert("Error", "Failed to fetch group members");
    }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity
          style={styles.profilePicContainer}
          onPress={() => navigation.navigate('GroupImage', { group_id })}
        >
          {groupImage ? (
            <Image source={{ uri: groupImage }} style={styles.profilePic} />
          ) : (
            <Ionicons name="person-add" size={40} color="#ccc" />
          )}
        </TouchableOpacity>
        <Text style={styles.groupName}>{groupName}</Text>
      </View>
      <FlatList
        data={members}
        keyExtractor={item => item.user_id.toString()}
        renderItem={({ item }) => (
          <View style={styles.memberItem}>
            <Ionicons name={item.is_admin ? 'shield-checkmark' : 'people'} size={24} color="#4CAF50" />
            <Text style={styles.memberName}>{item.first_name} ({item.is_admin ? 'Admin' : 'Member'})</Text>
          </View>
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
    header: {
      flexDirection: 'row',
      justifyContent: 'center',
      alignItems: 'center',
      paddingTop: 50,  // Increased top padding to push down the content, fitting the profile image
      paddingBottom: 30,
      paddingHorizontal: 10,
      borderBottomWidth: 1,
      borderBottomColor: '#cccccc',
      backgroundColor: '#ffffff',
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 2 },
      shadowOpacity: 0.1,
      shadowRadius: 2,
      elevation: 2,
    },
    profilePicContainer: {
      position: 'absolute',
      left: 15,
      top: 10,  // Minor adjustment if needed for top position
      width: 100,
      height: 100,
      borderRadius: 50,
      backgroundColor: '#e0e0e0',
      overflow: 'hidden',
      justifyContent: 'center',
      alignItems: 'center',
    },
    profilePic: {
      width: '100%',
      height: '100%',
    },
    addPhotoText: {
      fontSize: 12,
      color: '#888888',
    },
    groupName: {
      fontSize: 24,
      fontWeight: 'bold',
      color: '#333333',
      marginBottom:10,
    },
    memberItem: {
      flexDirection: 'row',
      alignItems: 'center',
      padding: 15,
      borderBottomWidth: 1,
      borderBottomColor: '#eaeaea',
      backgroundColor: '#ffffff',
      marginTop: 10,
    },
    memberName: {
      fontSize: 16,
      color: '#555555',
      marginLeft: 10,
    },
  });
  
export default GroupMembersDashboard;
