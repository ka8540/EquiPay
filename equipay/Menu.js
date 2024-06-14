import React, { useState, useEffect } from 'react';
import { View, Button, FlatList, Text, TouchableOpacity, StyleSheet, Alert, RefreshControl , loadData} from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Menu = ({ navigation }) => {
  const [users, setUsers] = useState([]);
  const [groups, setGroups] = useState([]);
  const [selectedUserIds, setSelectedUserIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchUsers();
    fetchGroups();
  }, []);

  const handleRefresh = () => {
    setRefreshing(true);
    Promise.all([fetchUsers(), fetchGroups()]).finally(() => {
        setRefreshing(false);
    });
};

  
  const fetchUsers = async () => {
    setLoading(true);
    try {
      const token = await AsyncStorage.getItem('jwt_token');
      if (!token) {
        Alert.alert('Error', 'JWT token not found');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://127.0.0.1:5000/friends', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const transformedData = response.data.map(user => ({
        id: user[0].toString(),
        name: user[1],
      }));

      setUsers(transformedData);
    } catch (error) {
      console.error('Error fetching users:', error);
      Alert.alert('Error', 'Failed to fetch users');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const fetchGroups = async () => {
    setLoading(true);
    const token = await AsyncStorage.getItem('jwt_token');
    console.log("Token:",token);
    if (!token) {
      Alert.alert('Error', 'JWT token not found');
      setLoading(false);
      return;
    }
  
    try {
      const response = await axios.get('http://127.0.0.1:5000/user_group', {
        headers: { Authorization: `Bearer ${token}` },
      });
      // Check if the response data is valid and is an array
      if (response.data && Array.isArray(response.data)) {
        setGroups(response.data.map(group => ({
          group_id: group.group_id.toString(), // Ensure group_id is a string
          group_name: group.group_name
        })));
      } else {
        setGroups([]); // Set to an empty array if no valid data
      }
    } catch (error) {
      console.error('Error fetching groups:', error);
      setGroups([]); // Set to an empty array in case of error
    } finally {
      setLoading(false);
    }
  };

  const handleSelectUser = userId => {
    const isSelected = selectedUserIds.includes(userId);
    if (isSelected) {
      setSelectedUserIds(currentIds => currentIds.filter(id => id !== userId));
    } else {
      setSelectedUserIds(currentIds => [...currentIds, userId]);
    }
  };

  const navigateToAddItem = () => {
    if (selectedUserIds.length === 0) {
      Alert.alert("Select Friends", "Please select at least one friend to split the expense.");
      return;
    }
    navigation.navigate('AddItem', { userIds: selectedUserIds });
  };

  const renderGroupItem = ({ item }) => (
    <TouchableOpacity
      style={[
        styles.row,
        { backgroundColor: '#fff' }
      ]}
      onPress={() => navigation.navigate('GroupMembers', { groupId: item.group_id })}
    >
      <Text style={styles.cell}>{item.group_name}</Text>
    </TouchableOpacity>
  );

  const renderUserItem = ({ item }) => (
    <TouchableOpacity
      style={[
        styles.row,
        { backgroundColor: selectedUserIds.includes(item.id) ? '#d0ebff' : '#fff' }
      ]}
      onPress={() => handleSelectUser(item.id)}
    >
      <Text style={styles.cell}>{item.name}</Text>
      <Text style={styles.radioText}>{selectedUserIds.includes(item.id) ? '🔘' : '⚪️'}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      {loading ? (
        <Text>Loading...</Text>
      ) : (
        <>
          <Text style={styles.sectionHeader}>Friends</Text>
          <FlatList
              data={users}
              keyExtractor={item => item.id.toString()}
              renderItem={renderUserItem}
              refreshControl={
                <RefreshControl
                  refreshing={refreshing}
                  onRefresh={handleRefresh}
                />
              }
            />
            <Text style={styles.sectionHeader}>Groups</Text>
            <FlatList
              data={groups}
              keyExtractor={item => item.group_id.toString()}
              renderItem={renderGroupItem}
              refreshControl={
                <RefreshControl
                  refreshing={refreshing}
                  onRefresh={handleRefresh}
                />
              }
            />
          <Button title="Continue" onPress={navigateToAddItem} />
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
  listContainer: {
    flexGrow: 1,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 15,
    paddingHorizontal: 10,
    borderBottomWidth: 1,
    borderColor: '#ccc',
  },
  sectionHeader: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 20,
    marginBottom: 10,
  },
  groupName: {
    fontSize: 16,
    color: '#333',
  },
  cell: {
    fontSize: 16,
    color: '#333',
  },
  radioText: {
    fontSize: 20,
  },
});

export default Menu;
