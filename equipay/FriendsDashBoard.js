import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator, TouchableOpacity, Alert, FlatList } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const FriendsDashboard = ({ route, navigation }) => {
  const { friend_id } = route.params;
  const [isLoading, setIsLoading] = useState(true);
  const [profile, setProfile] = useState({
    name: '',
    netAmount: 0,
    profilePicUrl: null,
    debts: []
  });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    const sessionKey = await AsyncStorage.getItem('sessionKey');

    if (!token || !sessionKey) {
      Alert.alert("Error", "Authentication details are missing");
      return;
    }

    try {
      const amountUrl = `http://127.0.0.1:5000/total-amount/${friend_id}`;
      const profilePicUrl = `http://127.0.0.1:5000/friend-profile-picture/${friend_id}`;
      const debtsUrl = `http://127.0.0.1:5000/debts-by-friend/${friend_id}`;
      const responses = await Promise.all([
        axios.get(amountUrl, { headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey }}),
        axios.get(profilePicUrl, { headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey }}),
        axios.get(debtsUrl, { headers: { Authorization: `Bearer ${token}`, 'Session-Key': sessionKey }})
      ]);

      const amountResponse = responses[0];
      const profilePicResponse = responses[1];
      const debtsResponse = responses[2];
      console.log("Debt Response:",responses[2]);
      if (amountResponse.data && profilePicResponse.data && debtsResponse.data) {
        setProfile({
          name: amountResponse.data.friend_name,
          netAmount: amountResponse.data.net_amount,
          profilePicUrl: profilePicResponse.data.url || null,
          debts: debtsResponse.data || []
        });
        console.log("Debts:",debtsResponse);
      } else {
        Alert.alert("Error", "Failed to fetch profile data");
      }
    } catch (error) {
      console.error("Error fetching profile data:", error);
    }
    setIsLoading(false);
  };

  const handleDebtSettlement = async (debt) => {
    const token = await AsyncStorage.getItem('jwt_token');
    const sessionKey = await AsyncStorage.getItem('sessionKey');
  
    if (!token || !sessionKey) {
      Alert.alert("Authentication Error", "Missing authentication details");
      return;
    }
  
    const postData = {
      friend_id: friend_id,
      amount_owed: parseFloat(debt.amount_owed) // Ensure this is a number if required
    };
  
    console.log("Sending Post Data:", postData);
  
    try {
      const response = await axios.post('http://127.0.0.1:5000/delete-debt', postData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Session-Key': sessionKey,
          'Content-Type': 'application/json'
        }
      });
  
      if (response.status === 200) {
        Alert.alert("Success", "Debt settled successfully");
        fetchData();  // Refresh data
      } else {
        Alert.alert("Error", "Failed to settle debt: " + (response.data.error || "Unknown Error"));
      }
    } catch (error) {
      console.error("API Call Failed", error);
      Alert.alert("Error", "Failed to settle debt: " + error.message);
    }
  };
  
  
  return (
    <View style={styles.container}>
      <View style={styles.profileCard}>
        {profile.profilePicUrl ? (
          <Image source={{ uri: profile.profilePicUrl }} style={styles.profilePic} />
        ) : (
          <View style={[styles.profilePic, styles.profilePicPlaceholder]}>
            <Text style={styles.placeholderText}>No Profile Picture</Text>
          </View>
        )}
        <Text style={styles.name}>{profile.name}</Text>
        <Text style={[styles.amount, { color: profile.netAmount < 0 ? 'red' : 'green' }]}>
          {profile.netAmount < 0 ? `You owe $${Math.abs(profile.netAmount)}` : `You are owed $${profile.netAmount}`}
        </Text>
        <FlatList
          data={profile.debts}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => (
            <TouchableOpacity onPress={() => handleDebtSettlement(item)} style={styles.debtItem}>
              <Text>{item.description} - ${item.amount_owed}</Text>
            </TouchableOpacity>
          )}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 20,
  },
  profileCard: {
    backgroundColor: 'white',
    borderRadius: 8,
    width: '100%',
    padding: 20,
    shadowColor: "#000",
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
  },
  profilePic: {
    width: 100,
    height: 100,
    borderRadius: 50,
    alignSelf: 'center',
    marginBottom: 20,
  },
  profilePicPlaceholder: {
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#e1e4e8',
  },
  placeholderText: {
    color: '#000',
    fontSize: 16,
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
    textAlign: 'center',
  },
  amount: {
    fontSize: 18,
    textAlign: 'center',
  },
  debtItem: {
    padding: 10,
    marginTop: 10,
    backgroundColor: '#ccc',
    borderRadius: 5
  }
});

export default FriendsDashboard;
