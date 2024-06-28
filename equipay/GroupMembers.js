import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const GroupMembers = ({ navigation, route }) => {
  const { groupId } = route.params;
  const [members, setMembers] = useState([]);
  const [selectedUserIds, setSelectedUserIds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGroupMembers();
  }, []);

  const fetchGroupMembers = async () => {
    setLoading(true);
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.get(`http://127.0.0.1:5000/group_members/${groupId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMembers(response.data);
    } catch (error) {
      console.error('Error fetching group members:', error);
      Alert.alert('Error', 'Failed to fetch group members');
    } finally {
      setLoading(false);
    }
  };

  const handleSelectMember = (userId) => {
    setSelectedUserIds(prev => 
      prev.includes(userId) ? prev.filter(id => id !== userId) : [...prev, userId]
    );
  };

  const navigateToAddGroupExpense = () => {
    navigation.navigate('AddGroupExpense', { selectedUserIds, groupId });
  };

  return (
    <View style={styles.container}>
      {loading ? (
        <Text>Loading...</Text>
      ) : (
        <>
          <FlatList
            data={members}
            keyExtractor={(item) => item.user_id.toString()}
            renderItem={({ item }) => (
              <TouchableOpacity
                style={[
                  styles.memberRow,
                  { backgroundColor: selectedUserIds.includes(item.user_id) ? '#d0ebff' : '#fff' }
                ]}
                onPress={() => handleSelectMember(item.user_id)}
              >
                <Text style={styles.memberName}>{item.first_name} ({item.is_admin ? 'Admin' : 'Member'})</Text>
              </TouchableOpacity>
            )}
          />
          <TouchableOpacity style={styles.button} onPress={navigateToAddGroupExpense}>
            <Text style={styles.buttonText}>Add Expense</Text>
          </TouchableOpacity>
        </>
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f9f9f9',
  },
  memberRow: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    marginTop: 10,
  },
  memberName: {
    fontSize: 16,
    color: '#333',
  },
  button: {
    marginTop: 20,
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontSize: 18,
  },
});

export default GroupMembers;
