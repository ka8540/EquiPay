import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Alert, FlatList, RefreshControl, Dimensions } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const FriendsDashboard = () => {
  const navigation = useNavigation();
  const route = useRoute();
  const { friend_id } = route.params;
  const [profile, setProfile] = useState({
    name: '',
    netAmount: 0,
    profilePicUrl: null,
    debts: []
  });
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', loadData);
    loadData();
    return unsubscribe;
  }, [navigation, friend_id]);

  const loadData = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const fetchData = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    const sessionKey = await AsyncStorage.getItem('sessionKey');
    if (!token || !sessionKey) {
      Alert.alert("Error", "Authentication details are missing");
      return;
    }
  
    try {
      const responses = await Promise.all([
        axios.get(`http://127.0.0.1:5000/total-amount/${friend_id}`, { headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey }}),
        axios.get(`http://127.0.0.1:5000/friend-profile-picture/${friend_id}`, { headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey }}),
        axios.get(`http://127.0.0.1:5000/debts-by-friend/${friend_id}`, { headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey }}),
        axios.get(`http://127.0.0.1:5000/friend_name/${friend_id}`, { headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey }})
      ]);
  
      const [amountResponse, profilePicResponse, debtsResponse, nameResponse] = responses;
  
      const sortedDebts = debtsResponse.data.sort((a, b) => new Date(a.date) - new Date(b.date)).map(debt => ({
        ...debt,
        date: formatDate(debt.date) // Apply the formatting here
      }));
  
      setProfile({
        name: nameResponse.data.friend_name || 'Name Not Found', // Use the name from the new API or fallback to a default
        netAmount: amountResponse.data.net_amount,
        profilePicUrl: profilePicResponse.data.url || null,
        debts: sortedDebts
      });
    } catch (error) {
      console.error("Error fetching profile data:", error);
      Alert.alert("Error", "Failed to fetch profile data");
    }
  };
  
  

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return `${date.toLocaleString('default', { month: 'short' })} ${date.getDate()}`; // Example: Jun 15
  };
  
  const handleDebtSettlement = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    const sessionKey = await AsyncStorage.getItem('sessionKey');
    if (!token || !sessionKey) {
      Alert.alert("Authentication Error", "Missing authentication details");
      return;
    }
    try {
      const response = await axios.post('http://127.0.0.1:5000/delete-debt', { friend_id }, {
        headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey, 'Content-Type': 'application/json' }
      });
      if (response.status === 200) {
        Alert.alert("Success", "Debt settled successfully");
        loadData(); // Refresh data
      } else {
        Alert.alert("Error", "Failed to settle debt: " + (response.data.error || "Unknown Error"));
      }
    } catch (error) {
      console.error("API Call Failed", error);
      Alert.alert("Error", "Failed to settle debt: " + error.message);
    }
  };

  const onRefresh = () => {
    loadData();
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        {profile.profilePicUrl ? (
          <Image source={{ uri: profile.profilePicUrl }} style={styles.profilePic} />
        ) : (
          <View style={[styles.profilePic, styles.profilePicPlaceholder]}>
            <MaterialCommunityIcons name="account" size={50} color="#fff" />
          </View>
        )}
        <Text style={styles.name}>{profile.name}</Text>
      </View>
      <Text style={{
        color: profile.netAmount < 0 ? 'red' : 'green',
        fontSize: 24, 
        fontWeight: 'bold', 
        textAlign: 'center',
        marginVertical: 20
      }}>
        {profile.netAmount < 0 ? `You owe $${Math.abs(profile.netAmount)}` : `You are owed $${profile.netAmount}`}
      </Text>

      <TouchableOpacity onPress={handleDebtSettlement} style={styles.settleButton}>
        <Text style={styles.settleButtonText}>Settle All Debts</Text>
      </TouchableOpacity>
      <FlatList
        data={profile.debts}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.debtItem}>
            <Text style={styles.debtDescription}>{item.description} - ${item.amount_owed}</Text>
            <Text style={styles.debtDate}>{item.date}</Text>
          </View>
        )}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f7f7f7', // Lighter background color
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: '#e1e1e1', // Softer border color
    backgroundColor: '#ffffff',
  },
  profilePic: {
    width: 120, // Larger profile picture
    height: 120,
    borderRadius: 60,
    borderWidth: 4,
    borderColor: '#007bff', // Brighter border color
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 6,
    elevation: 4,
  },
  profilePicPlaceholder: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: '#007bff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  name: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#333',
    flex: 1,
    textAlign: 'center',
    marginHorizontal: 10, // Added margin for better spacing
  },
  debtItem: {
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 0, // Removed border
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    marginHorizontal: 10,
    borderRadius: 10,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.15,
    shadowRadius: 3.84,
    elevation: 3,
    marginBottom: 5, // Space between items
  },
  debtDescription: {
    fontSize: 18,
    color: '#333',
  },
  settleButton: {
    backgroundColor: '#007bff', // Consider using a gradient here
    padding: 15,
    marginVertical: 20,
    alignItems: 'center',
    borderRadius: 10,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  settleButtonText: {
    fontSize: 18,
    color: '#fff',
    fontWeight: 'bold',
  }
});


export default FriendsDashboard;
