import React, { useState, useEffect } from 'react';
import { View, Button, FlatList, Text, TouchableOpacity, StyleSheet, Alert, RefreshControl } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Menu = ({ navigation }) => {
  const [users, setUsers] = useState([]);
  const [selectedUserIds, setSelectedUserIds] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const sessionKey = await AsyncStorage.getItem('sessionKey');
      const token = await AsyncStorage.getItem('jwt_token');
      if (!sessionKey || !token) {
        Alert.alert('Error', 'Missing session key or token');
        setLoading(false);
        return;
      }

      const response = await axios.get('http://127.0.0.1:5000/friends', {
        headers: {
          Authorization: `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });

      const transformedData = response.data.map(user => ({
        id: user[0].toString(), // Ensure id is a string for keyExtractor
        name: user[1], // Assuming the second element is the name
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

  const handleRefresh = () => {
    setRefreshing(true);
    fetchUsers();
  };

  const handleSelectUser = (userId) => {
    const isSelected = selectedUserIds.includes(userId);
    if (isSelected) {
      setSelectedUserIds(currentIds => currentIds.filter(id => id !== userId));
    } else {
      if (selectedUserIds.length < 4) {
        setSelectedUserIds(currentIds => [...currentIds, userId]);
      } else {
        Alert.alert("Limit reached", "You can select up to 4 friends.");
      }
      console.log("selected ids:",selectedUserIds)
    }
  };

  const navigateToAddItem = () => {
    if (selectedUserIds.length === 0) {
      Alert.alert("Select Friends", "Please select at least one friend to split the expense.");
      return;
    }
    navigation.navigate('AddItem', { userIds: selectedUserIds });
  };

  const renderItem = ({ item }) => (
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
          <FlatList
            data={users}
            keyExtractor={(item) => item.id.toString()}
            renderItem={renderItem}
            contentContainerStyle={styles.listContainer}
            RefreshControl={
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
  cell: {
    fontSize: 16,
    color: '#333',
  },
  radioText: {
    fontSize: 20,
  },
});

export default Menu;
