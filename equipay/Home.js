import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, Alert, RefreshControl, ScrollView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

export default function Home({ navigation }) {
  const [debts, setDebts] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    fetchDebts();
  }, []);

  const fetchDebts = async () => {
    try {
      const token = await AsyncStorage.getItem('jwt_token');
      const sessionKey = await AsyncStorage.getItem('sessionKey');
      if (!token || !sessionKey) {
        Alert.alert("Error", "Authentication details are missing");
        return;
      }
      
      const response = await axios.get('http://127.0.0.1:5000/total-amount', {
        headers: {
          Authorization: `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });
      setDebts(response.data);
      setRefreshing(false);  // Reset refreshing state when data is loaded
    } catch (error) {
      Alert.alert("Error", "Failed to fetch debts: " + error.message);
      setRefreshing(false);  // Reset refreshing state on error as well
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchDebts();
  };

  const renderItem = ({ item }) => (
    <TouchableOpacity 
      style={styles.debtItem}
      onPress={() => navigation.navigate('FriendsDashBoard', { friend_id: item.friend_id })}
    >
      <Text style={styles.friendName}>{item.friend_name}</Text>
      <Text style={[styles.amount, { color: item.net_amount < 0 ? 'red' : 'green' }]}>
        {item.net_amount < 0 ? `-$${Math.abs(item.net_amount)}` : `$${item.net_amount}`}
      </Text>
    </TouchableOpacity>
  );

  return (
    <FlatList
      data={debts}
      renderItem={renderItem}
      keyExtractor={item => item.friend_id.toString()}
      contentContainerStyle={[styles.listContainer, { backgroundColor: '#fff' }]} 
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={onRefresh}
        />
      }
      ListHeaderComponent={(
        <TouchableOpacity 
          style={styles.addFriendButton}
          onPress={() => navigation.navigate('AddFriends')}
        >
          <MaterialIcons name="person-add" size={28} color="black" />
        </TouchableOpacity>
      )}
    />
  );  
}

const styles = StyleSheet.create({
  listContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 20,
  },
  menu: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 10,
  },
  menuButton: {
    padding: 15,
    margin: 10,
    backgroundColor: '#007AFF',
    borderRadius: 5,
    alignItems: 'center',
  },
  menuText: {
    color: '#fff',
    fontSize: 18,
  },
  addFriendButton: {
    position: 'absolute',  // Position the button absolutely
    bottom: 280,               // Distance from the top of its container
    left: 160,             // Distance from the right of its container
    backgroundColor: '#fff',
    padding: 10,
    borderRadius: 30,
    borderWidth: 1,
    borderColor: '#fff',
  },  
  debtItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 10,
    borderBottomWidth: 1,
    borderColor: '#ccc',
    width: '100%',
  },
  friendName: {
    fontSize: 16,
    color: '#333',
  },
  amount: {
    fontSize: 16,
  }
});
