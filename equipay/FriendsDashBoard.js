import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, Image, TouchableOpacity, Alert, FlatList, RefreshControl, Dimensions } from 'react-native';
import { useNavigation, useRoute } from '@react-navigation/native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { SectionList } from 'react-native';

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
  
      let debtsGroupedByMonth = {};
      if (debtsResponse.status === 200 && debtsResponse.data && debtsResponse.data.length > 0) {
        debtsResponse.data.forEach(debt => {
          const date = new Date(debt.date);
          const monthYear = `${date.toLocaleString('default', { month: 'long' })} ${date.getFullYear()}`;
          if (!debtsGroupedByMonth[monthYear]) {
            debtsGroupedByMonth[monthYear] = [];
          }
          debtsGroupedByMonth[monthYear].push({
            ...debt,
            date: formatDate(debt.date) // Store the formatted date
          });
        });
      }
  
      setProfile({
        name: nameResponse.data && nameResponse.data.friend_name ? nameResponse.data.friend_name : 'Name Not Found', 
        netAmount: amountResponse.data && amountResponse.data.net_amount ? amountResponse.data.net_amount : 0,
        profilePicUrl: profilePicResponse.data && profilePicResponse.data.url ? profilePicResponse.data.url : null,
        debts: debtsGroupedByMonth
      });
    } catch (error) {
      console.error("Error fetching profile data:", error);
      Alert.alert("Error", "Failed to fetch profile data");
    }
  };
  

  const getMonthFromDebts = () => {
    if (profile.debts.length > 0) {
      const firstDebtDate = new Date(profile.debts[0].originalDate); // Use the original date
      console.log("Date:", firstDebtDate);
      return firstDebtDate.toLocaleString('default', { month: 'long' });
    }
    return ''; // Return empty string or some default value if no debts
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return `${date.toLocaleString('default', { month: 'short' })} ${date.getDate()}`; 
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
        <View style={styles.profileContainer}>
        {profile.profilePicUrl ? (
            <Image source={{ uri: profile.profilePicUrl }} style={styles.profilePic} />
          ) : (
            <View style={styles.profilePicPlaceholder}>
              <MaterialCommunityIcons name="account" size={50} color="#fff" />
            </View>
          )}
          <Text style={styles.name}>{profile.name}</Text>
        </View>
        <View style={styles.horizontalLine}></View>
        <TouchableOpacity onPress={handleDebtSettlement} style={styles.settleButton}>
          <Text style={styles.settleButtonText}>Settle Up</Text>
        </TouchableOpacity>
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
      <SectionList
          sections={Object.keys(profile.debts).map((month, idx) => ({
            title: month, 
            data: profile.debts[month]
          }))}
          keyExtractor={(item, index) => `item-${index}`}
          renderItem={({ item, index }) => {
            console.log(`Rendering item with key: item-${index}, ID: ${item.id}`);
            return (
              <View style={styles.debtItem}>
                <Text style={styles.debtDescription}>{item.description} - ${item.amount_owed}</Text>
                <Text style={styles.debtDate}>{item.date}</Text>
              </View>
            );
          }}
          renderSectionHeader={({ section: { title } }) => (
            <Text style={styles.monthTitle}>{title}</Text>
          )}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f7f7f7',
  },
  header: {
    padding: 20,
    backgroundColor: '#ffffff',
    alignItems: 'flex-start', // Align items to the left
    width: '100%', // Make sure the header spans the full width
  },
  profileContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'flex-start', // Ensures content aligns to the left
    width: '100%', // Ensures the container spans the full width
    marginBottom: 15,
  },
  profilePic: {
    width: 100,
    height: 100,
    borderRadius: 60,
    borderWidth: 4,
    borderColor: '#007bff',
    marginLeft: 0, // Adjust if more left spacing is needed
  },
  profilePicPlaceholder: {
    width: 100,
    height: 100,
    borderRadius: 60,
    backgroundColor: '#007bff',
    justifyContent: 'center',
    alignItems: 'center',
    borderWidth: 4,
    borderColor: '#007bff',
    overflow: 'hidden',
    marginLeft: 0, // Keep consistent with profilePic
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#333',
    marginLeft: 80, // Space between the picture and the name
  },
  horizontalLine: {
    width: '100%',
    height: 1,
    backgroundColor: '#d3d3d3',
    marginBottom: 10,  
  },
  debtItem: {
    padding: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 0, 
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
    marginBottom: 5, 
  },
  debtDescription: {
    fontSize: 18,
    color: '#333',
  },
  settleButton: {
    paddingHorizontal: 10,
    paddingVertical: 5,
    backgroundColor: '#007bff',
    borderRadius: 8,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.25,
    shadowRadius: 3.84,
    elevation: 5,
    width: 92,
    height: 30,
    alignSelf: 'center',  // This centers the button in the available space
    marginTop: 5,
    position:'relative',
    right:150,  // Adds some space from the top element
  },
  settleButtonText: {
    fontSize: 16,
    color: '#fff',
    fontWeight: 'bold',
    textAlign: 'center',  // Center text inside the button
  },
monthDisplay: {
  fontSize: 18,
  fontWeight: 'bold',
  color: '#555',
  textAlign: 'left',
  marginBottom: 10,
  marginLeft:10,
},
monthTitle: {
  fontSize: 18,
  fontWeight: 'bold',
  backgroundColor: '#f7f7f7',
  color: '#000',
  paddingTop: 2,
  paddingLeft: 10,
  paddingRight: 10,
  paddingBottom: 2,
}

});


export default FriendsDashboard;
