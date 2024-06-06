import React, { useState, useEffect } from 'react';
import { View, Button, FlatList, Text, TouchableOpacity, StyleSheet, Alert, RefreshControl } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Menu = ({ navigation }) => {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(null);
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
    setSelectedUserId(userId);
    navigation.navigate('AddItem', { userId });
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={[
        styles.row,
        { backgroundColor: item.id === selectedUserId ? '#d0ebff' : '#fff' }
      ]}
      onPress={() => handleSelectUser(item.id)}
    >
      <Text style={styles.cell}>{item.name}</Text>
      <Text style={styles.radioText}>{item.id === selectedUserId ? '🔘' : '⚪️'}</Text>
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
          contentContainerStyle={styles.listContainer}
          RefreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={handleRefresh}
            />
          }
        />
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
