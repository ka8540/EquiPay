import React, { useState, useEffect } from 'react';
import { View, Button, FlatList, Text, StyleSheet, Alert } from 'react-native';
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Menu = ({ navigation }) => {
  const [users, setUsers] = useState([]);
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
          email: user[5],
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

  const renderItem = ({ item }) => (
    <View style={styles.row}>
      <Text style={styles.cell}>{item.id}</Text>
      <Text style={styles.cell}>{item.name}</Text>
      <Text style={styles.cell}>{item.email}</Text>
    </View>
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
          ListHeaderComponent={
            <View style={styles.headerRow}>
              <Text style={styles.headerCell}>ID</Text>
              <Text style={styles.headerCell}>Name</Text>
              <Text style={styles.headerCell}>Email</Text>
            </View>
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
    backgroundColor: '#f9f9f9', // Slightly off-white to distinguish from item background
  },
  listContainer: {
    flexGrow: 1,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderColor: '#ccc',
    backgroundColor: '#fff', // White background for items
  },
  cell: {
    flex: 1,
    textAlign: 'center',
    fontSize: 16, // Larger font size
    color: '#333', // Darker text for better visibility
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 10,
    backgroundColor: '#ddd', // Distinguish header with a grey background
  },
  headerCell: {
    flex: 1,
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: 18, // Even larger font size for headers
  },
});

export default Menu;
