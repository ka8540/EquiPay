import React, { useState, useEffect } from 'react';
import { View, Button, FlatList, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Menu = ({ navigation }) => {
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const sessionKey = await AsyncStorage.getItem('sessionKey');
        const token = await AsyncStorage.getItem('jwt_token');

        if (!sessionKey || !token) {
          Alert.alert('Error', 'Missing session key or token');
          setLoading(false);
          return;
        }

        const response = await axios.get('http://127.0.0.1:5000/listUsers', {
          headers: {
            Authorization: `Bearer ${token}`,
            'Session-Key': sessionKey,
          },
        });

        const transformedData = response.data.map(user => ({
          id: user[0],
          name: user[1],
          email: user[2],
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

  const handleSelectUser = (userId) => {
    setSelectedUserId(userId);
    // Perform any action here such as navigation or displaying user details
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity
      style={[
        styles.row,
        { backgroundColor: item.id === selectedUserId ? '#d0ebff' : '#fff' }
      ]}
      onPress={() => handleSelectUser(item.id)}
    >
      <View style={styles.cellContainer}>
        <Text style={styles.cell}>{item.name}</Text>
        <Text style={styles.cell}>{item.email}</Text>
      </View>
      <Text style={styles.radioText}>{item.id === selectedUserId ? '🔘' : '⚪️'}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Button
        title="Add Item"
        onPress={() => navigation.navigate('AddItem')}
      />
      {loading ? (
        <Text>Loading...</Text>
      ) : (
        <FlatList
          data={users}
          keyExtractor={(item) => item.id.toString()}
          renderItem={renderItem}
          contentContainerStyle={styles.listContainer}
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
  cellContainer: {
    flexDirection: 'row',
    flex: 1,
    justifyContent: 'space-between',
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
