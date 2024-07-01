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
  const [expenses, setExpenses] = useState([]);
  const [isAdmin, setIsAdmin] = useState(false);
  

  useEffect(() => {
    loadData();

    const unsubscribe = navigation.addListener('focus', () => {
        loadData();
    });

    return unsubscribe;
}, [navigation, group_id]);

const loadData = async () => {
  setRefreshing(true);
  await fetchGroupName(group_id);
  await fetchGroupImage(group_id);
  await fetchGroupMembers(group_id);
  await fetchExpenses();  
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

  const fetchExpenses = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token) {
        Alert.alert("Error", "JWT token not found");
        return;
    }

    try {
        const response = await axios.get(`http://127.0.0.1:5000/group_expenselist/${group_id}`, {
            headers: { Authorization: `Bearer ${token}` }
        });
        setExpenses(response.data);
    } catch (error) {
        console.error('Failed to fetch expenses:', error);
        Alert.alert("Error", "Failed to fetch expenses");
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
        setGroupImage(response.data.url[0]); 
      } else {
        setGroupImage(null);
      }
    } catch (error) {
      console.log(error);
      setGroupImage(null); 
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
        loadData(); 
      } else {
        Alert.alert("Error", "Failed to settle debt");
      }
    } catch (error) {
      console.error('Error settling debt:', error);
      Alert.alert("Error", "Failed to settle debt");
    }
  };

  const handleDeleteGroup = async (group_id) => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.post(`http://127.0.0.1:5000/delete_group/${group_id}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });
  
      if (response.status === 200) {
        Alert.alert("Success", "Group deleted successfully");
        navigation.goBack(); // Assuming you want to navigate back after deletion
      } else if (response.status === 201) {
        Alert.alert("Permission Denied", "You are not an admin, so you can't delete the group.");
      } else {
        Alert.alert("Error", "Failed to delete group");
      }
    } catch (error) {
      console.error('Error deleting group:', error);
      Alert.alert("Error", "Failed to delete group");
    }
  };

  const handleLeaveGroup = async () => {
    Alert.alert(
      "Confirm",
      "Are you sure you want to leave the group?",
      [
        {
          text: "Cancel",
          style: "cancel"
        },
        { text: "Yes", onPress: async () => {
          const token = await AsyncStorage.getItem('jwt_token');
          if (!token) {
            Alert.alert("Error", "Authentication token not found");
            return;
          }
  
          try {
            const response = await axios.put(`http://127.0.0.1:5000/leave_group/${group_id}`, {}, {
              headers: { Authorization: `Bearer ${token}` }
            });
            if (response.status === 200) {
              Alert.alert("Success", "You have left the group");
              navigation.goBack();
            } else {
              Alert.alert("Error", "Could not leave the group");
            }
          } catch (error) {
            console.error('Error leaving group:', error);
            Alert.alert("Error", "Failed to leave the group");
          }
        }}
      ],
      { cancelable: false }
    );
  };
  
  

  
  const fetchGroupMembers = async (groupId) => {
    const token = await AsyncStorage.getItem('jwt_token');
    const userId = await AsyncStorage.getItem('user_id'); 
    try {
      const membersResponse = await axios.get(`http://127.0.0.1:5000/group_members/${groupId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      if (membersResponse.data) {
        const membersWithDebts = await Promise.all(membersResponse.data.map(async member => {
          const isCurrentUserAdmin = member.user_id.toString() === userId && member.is_admin;
          if (isCurrentUserAdmin) setIsAdmin(true);
          const debtResponse = await axios.get(`http://127.0.0.1:5000/group_total/${groupId}/${member.user_id}`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          return { ...member, debtAmount: parseFloat(debtResponse.data.net_amount) || 0 };
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
      <View style={{ flexDirection: 'row', alignItems: 'center' }}>
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
      <View style={styles.horizontalLine}></View>
      <View style={{ flexDirection: 'row', alignItems: 'center' }}>
      <TouchableOpacity style={styles.deleteButton} onPress={() => handleDeleteGroup(group_id)}>
        <Text style={styles.deleteButtonText}>Delete Group</Text>
      </TouchableOpacity>
      <TouchableOpacity style={styles.leaveButton} onPress={handleLeaveGroup}>
      <Text style={styles.leaveButtonText}>Leave Group</Text>
    </TouchableOpacity>
    <TouchableOpacity
      style={styles.AddMemberButton}
      onPress={() => navigation.navigate('Members', { group_id })}
    >
      <Text style={styles.leaveButtonText}>Add Member</Text>
    </TouchableOpacity>

    </View>
    </View>
      <FlatList
        data={members}
        keyExtractor={item => item.user_id.toString()}
        renderItem={({ item }) => (
          <TouchableOpacity style={styles.memberItem} onPress={() => selectMember(item)}>
            <Ionicons name={item.is_admin ? 'shield-checkmark' : 'people'} size={24} color="#4CAF50" />
            <Text style={styles.memberName}>{item.first_name}</Text>
            <Text style={[
              styles.debtAmount,
              {color: item.debtAmount >= 0 ? 'green' : 'red', position: 'absolute', right: 10}
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
      <FlatList
          data={expenses}
          keyExtractor={item => item.expense_id.toString()}
          renderItem={({ item }) => (
              <View style={styles.itemContainer}>
                  <Text style={styles.description}>{item.description}</Text>
                  <Text style={[
                      styles.amount,
                      item.status === 'lend' ? styles.lendAmount : styles.borrowedAmount
                  ]}>
                      {item.status === 'lend' ? `You lent $${item.amount}` : `You borrowed $${item.amount}`}
                  </Text>
                  <Text style={styles.date}>{new Date(item.date).toLocaleDateString()}</Text>
              </View>
          )}
          refreshControl={
              <RefreshControl refreshing={refreshing} onRefresh={loadData} />
          }
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
    alignItems: 'center',
    paddingTop: 10,
    paddingBottom: 10,
    paddingHorizontal: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#cccccc',
    backgroundColor: '#ffffff',
},
profilePicContainer: {
    width: 140,
    height: 140,
    borderRadius: 80,
    backgroundColor: '#e0e0e0',
    overflow: 'hidden',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 10,
    position:'static',
    right:60,
},
profilePic: {
    width: '100%',
    height: '100%',
},
groupName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333333',
    marginLeft: 20,
},
deleteButton: {
  backgroundColor: 'red',
  padding: 10,
  borderRadius: 5,
  alignSelf: 'left', 
},
deleteButtonText: {
  color: 'white',
  fontSize: 16,
  textAlign: 'center',
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
      fontSize: 16,  
      marginLeft: 5, 
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
  },
  itemContainer: {
      padding: 10,
      marginVertical: 8,
      backgroundColor: 'white',
      flexDirection: 'column',
      borderBottomWidth: 1,
      borderBottomColor: '#ddd',
      alignItems: 'flex-start'
  },
  description: {
      fontSize: 18,
      color: '#333'
  },
  amount: {
    fontSize: 16,
    marginTop: 5
  },
  lendAmount: {
      color: 'green',
  },
  borrowedAmount: {
      color: 'red',
  },
  date: {
      fontSize: 14,
      color: '#999',
      marginTop: 5
  },
  horizontalLine: {
    width: '100%',
    height: 1,
    backgroundColor: '#d3d3d3',
    marginBottom: 10,  
  },
  leaveButton: {
    backgroundColor: 'orange',
    padding: 10,
    borderRadius: 5,
    marginLeft:10
  },
  leaveButtonText: {
    color: 'white',
    fontSize: 16,
    textAlign: 'center'
  },
  AddMemberButton:{
    backgroundColor: 'green',
    padding: 10,
    borderRadius: 5,
    marginLeft:10
  },
});
export default GroupMembersDashboard;

