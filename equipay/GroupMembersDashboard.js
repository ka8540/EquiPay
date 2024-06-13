import React, { useState, useEffect } from 'react';
import { View, Text, TouchableOpacity, Image, FlatList, StyleSheet, Alert, RefreshControl } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';

const GroupMembersDashboard = () => {
  const [groupName, setGroupName] = useState('');
  const [groupImage, setGroupImage] = useState(null);
  const [members, setMembers] = useState([]);
  const [selectedMemberId, setSelectedMemberId] = useState(null);
  const navigation = useNavigation();
  const route = useRoute();
  const { group_id } = route.params;
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();

    const unsubscribe = navigation.addListener('focus', () => {
      loadData();
    });

    return unsubscribe; // Cleanup listener on unmount
  }, [navigation, group_id]);

  const loadData = async () => {
    setRefreshing(true);
    await fetchGroupName(group_id);
    await fetchGroupImage(group_id);
    await fetchGroupMembers(group_id);
    setRefreshing(false);
  };

  const onRefresh = () => {
    loadData();
  };

  const selectMember = (member) => {
    if (member.debtAmount > 0) {
      setSelectedMemberId(member.user_id);
    } else {
      setSelectedMemberId(null);
    }
  };


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

  
  const handleSettleDebt = async (friend_id, amount) => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.post(`http://127.0.0.1:5000/group_settle/${group_id}`, {
        friend_id,
        amount_owed: amount
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (response.status === 200) {
        Alert.alert("Success", "Debt settled successfully");
        loadData(); // Refresh data
      } else {
        Alert.alert("Error", "Failed to settle debt");
      }
    } catch (error) {
      console.error('Error settling debt:', error);
      Alert.alert("Error", "Failed to settle debt");
    }
  };

  
  const fetchGroupMembers = async (groupId) => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const membersResponse = await axios.get(`http://127.0.0.1:5000/group_members/${groupId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      console.log("MemberResponse:", membersResponse.data);
      if (membersResponse.data) {
        const membersWithDebts = await Promise.all(membersResponse.data.map(async member => {
          try {
            const debtResponse = await axios.get(`http://127.0.0.1:5000/group_total/${groupId}/${member.user_id}`, {
              headers: { Authorization: `Bearer ${token}` }
            });
            console.log("debtResponse:", debtResponse.data);
            // Ensure debtAmount is always a number
            return { ...member, debtAmount: parseFloat(debtResponse.data.net_amount) || 0 };  // Use parseFloat to ensure it's a number
          } catch (debtError) {
            console.error('Error fetching debt for member:', member.user_id, debtError);
            return { ...member, debtAmount: 0 };  // Default to 0 if there's an error
          }
        }));
        setMembers(membersWithDebts);
      }
    } catch (error) {
      console.error('Error fetching group members:', error);
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
          <TouchableOpacity style={styles.memberItem} onPress={() => selectMember(item)}>
            <Ionicons name={item.is_admin ? 'shield-checkmark' : 'people'} size={24} color="#4CAF50" />
            <Text style={styles.memberName}>
              {item.first_name} 
            </Text>
            <Text style={[
              styles.debtAmount,
              {
                color: item.debtAmount >= 0 ? 'green' : 'red', // Apply green or red color based on debt amount
                position: 'absolute',  // Position it absolutely
                right: 10  // Adjust the left value as needed to position it from the left side of its container
              }
            ]}>
              ${item.debtAmount.toFixed(2)}
            </Text>

            {selectedMemberId === item.user_id && item.debtAmount > 0 && (
              <TouchableOpacity style={styles.settleButton} onPress={() => handleSettleDebt(item.user_id, item.debtAmount)}>
                <Text style={styles.settleButtonText}>Settle Debt</Text>
              </TouchableOpacity>
            )}
          </TouchableOpacity>
        )}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
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
    paddingTop: 50,
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
    top: 10,
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
    marginBottom: 10,
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
  debtAmount: {
    fontSize: 16,  // Matching font size of memberName for consistency
    marginLeft: 5,  // Slight margin for visual separation
  },
  settleButton: {
    backgroundColor: 'green',
    padding: 10,
    borderRadius: 5,
    margin: 5,
    position: 'absolute',
    right: 150
  },
  settleButtonText: {
    color: 'white',
    fontSize: 16,
    textAlign: 'center',
  }
});

export default GroupMembersDashboard;

