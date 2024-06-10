import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, ActivityIndicator, TouchableOpacity, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const FriendsDashboard = ({ route }) => {
  const { friend_id } = route.params;
  const [isLoading, setIsLoading] = useState(true);
  const [profile, setProfile] = useState({
    name: '',
    netAmount: 0,
    profilePicUrl: null
  });

  useEffect(() => {
    const fetchData = async () => {
      const token = await AsyncStorage.getItem('jwt_token');
      const sessionKey = await AsyncStorage.getItem('sessionKey');

      if (!token || !sessionKey) {
        Alert.alert("Error", "Authentication details are missing");
        return;
      }

      try {
        // Fetch the amount information
        const amountUrl = `http://127.0.0.1:5000/total-amount/${friend_id}`;
        const amountResponse = await axios.get(amountUrl, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Session-Key': sessionKey
          }
        });

        // Fetch the profile picture
        const profilePicUrl = `http://127.0.0.1:5000/friend-profile-picture/${friend_id}`;
        const profilePicResponse = await axios.get(profilePicUrl, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Session-Key': sessionKey
          }
        });

        if (amountResponse.data) {
          setProfile({
            name: amountResponse.data.friend_name, // Assuming the API returns friend_name
            netAmount: amountResponse.data.net_amount, // Assuming the API returns net_amount
            profilePicUrl: profilePicResponse.data.url || null // Assuming the API returns the URL or it's null if not available
          });
        } else {
          Alert.alert("Error", "Failed to fetch profile data");
        }
      } catch (error) {
        console.error("Error fetching profile data:", error);
      }
      setIsLoading(false);
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <View style={styles.container}><ActivityIndicator size="large" color="#0000ff" /></View>;
  }

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
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
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
  }
});

export default FriendsDashboard;
