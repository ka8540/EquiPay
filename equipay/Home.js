import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, FlatList, Alert, RefreshControl, StatusBar, SafeAreaView, Animated, ScrollView } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';
import Speedometer from 'react-native-speedometer-chart';

const MySpeedometer = ({ netAmount = 0 }) => {
  const getStatusText = (amount) => {
    if (amount > 400) return "Spending too much";
    if (amount > 70) return "Warning: High spending";
    return "Good spending";
  };

  const getSegmentColors = (amount) => {
    if (amount > 400) return ['#FF0000', '#FF0000', '#FF0000', '#FF0000']; 
    if (amount > 70) return ['#00FF00', '#00FF00', '#FFFF00', '#FF0000'];
    return ['#00FF00', '#00FF00', '#00FF00', '#FFFF00']; 
  };

  return (
    <View style={styles.speedometerContainer}>
      <Speedometer
        value={Number(netAmount)} 
        totalValue={1000}
        size={250}
        outerColor="#d3d3d3"
        internalColor={netAmount > 400 ? 'red' : netAmount > 70 ? 'orange' : 'green'}
        showIndicator
        needleSharpness={1}
        indicatorColor="black"
        segments={3}
        segmentColors={getSegmentColors(netAmount)}
        labelFormatter={(value) => `${value}%`}
      />
      <Text style={styles.speedometerText}>{getStatusText(netAmount)}</Text>
    </View>
  );
};

export default function Home({ navigation }) {
  const [debts, setDebts] = useState([]);
  const [netAmount, setNetAmount] = useState(0);
  const [refreshing, setRefreshing] = useState(false);
  const fadeAnim = useRef(new Animated.Value(0)).current;
  const [isExpanded, setIsExpanded] = useState(false);
  const animationController = useRef(new Animated.Value(0)).current;
  const [graphData, setGraphData] = useState(null);
  useEffect(() => {
    fetchDebts();
    fetchNetAmount();
    fetchGraphData();

    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 2000,
      useNativeDriver: true
    }).start();
  }, []);

  const toggleExpansion = () => {
    setIsExpanded(!isExpanded);
    Animated.timing(animationController, {
      toValue: isExpanded ? 0 : 1,
      duration: 300,
      useNativeDriver: false
    }).start();
  };

  const maxHeight = animationController.interpolate({
    inputRange: [0, 1],
    outputRange: [0, 200]
  });

  const fetchDebts = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token) {
      Alert.alert("Error", "Authentication token is missing or expired. Please login again.");
      return;
    }

    try {
      const response = await axios.get('http://127.0.0.1:5000/total-amount', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setDebts(response.data);
    } catch (error) {
      Alert.alert("Error", "Failed to fetch debts: " + error.message);
    }
    setRefreshing(false);
  };

  const fetchNetAmount = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.get('http://127.0.0.1:5000/net_amount', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setNetAmount(Number(response.data.total)); 
    } catch (error) {
      Alert.alert("Error", "Failed to fetch net amount: " + error.message);
    }
  };

  

  const onRefresh = () => {
    setRefreshing(true);
    fetchDebts();
    fetchNetAmount();
  };

  const fetchGraphData = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    try {
      const response = await axios.get('http://127.0.0.1:5000/graph_values', {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.status === 201 || !response.data || response.data.length === 0) {
        setGraphData({
          labels: ["Start", "End"],
          datasets: [{ data: [0, 0] }]
        });
      } else {
        const labels = response.data.map(item => {
          const date = new Date(item[1]);
          return date.toLocaleDateString("en-US", { month: 'short', day: 'numeric' });
        });
        const data = response.data.map(item => parseFloat(item[0]));
        setGraphData({
          labels,
          datasets: [{ data }]
        });
      }
    } catch (error) {
      console.error("Error fetching graph data: ", error);
      Alert.alert("Error", "Failed to fetch graph data: " + (error.response ? error.response.data.message : error.message));
    }
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
    <SafeAreaView style={styles.safeArea}>
      <StatusBar barStyle="dark-content" backgroundColor="black" />
      <FlatList
        ListHeaderComponent={
          <>
            <View style={styles.header}>
              <Text style={styles.headerTitle}>EquiPay</Text>
              <TouchableOpacity
                style={styles.addFriendButton}
                onPress={() => navigation.navigate('AddFriends')}
              >
                <MaterialIcons name="person-add" size={28} color="black" />
              </TouchableOpacity>
            </View>
            <TouchableOpacity style={styles.totalAmountContainer} onPress={toggleExpansion}>
              <Text style={styles.totalNetAmountTitle}>Total:</Text>
              <Text style={[styles.totalAmount, { color: netAmount < 0 ? 'red' : 'green' }]}>
                {netAmount < 0 ? `-$${Math.abs(netAmount)}` : `$${netAmount}`}
              </Text>
            </TouchableOpacity>
            <Animated.View style={{ maxHeight, overflow: 'hidden' }}>
              <FlatList
                data={debts}
                renderItem={renderItem}
                keyExtractor={item => item.friend_id.toString()}
                contentContainerStyle={styles.listContainer}
                scrollEnabled={false} 
              />
            </Animated.View>
            <MySpeedometer netAmount={netAmount} />
          </>
        }
        ListFooterComponent={
          graphData && (
            <LineChart
              data={graphData}
              width={Dimensions.get("window").width}
              height={220}
              yAxisLabel="$"
              yAxisInterval={1}
              chartConfig={{
                backgroundColor: "#fff",
                backgroundGradientFrom: "#fff",
                backgroundGradientTo: "#fff",
                decimalPlaces: 2,
                color: (opacity = 1) => `rgba(27, 201, 18, ${opacity})`,
                labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                style: {
                  borderRadius: 16
                },
                propsForDots: {
                  r: "2",
                  strokeWidth: "2",
                  stroke: "black"
                },
                bezier: false
              }}
              style={{
                marginVertical: 8,
                borderRadius: 16,
                shadowColor: '#071718',
                shadowOffset: { width: 0, height: 1 },
                shadowOpacity: 0.3,
                shadowRadius: 3,
              }}
            />
          )
        }
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      />
    </SafeAreaView>
  );
}  

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: '#ffffff',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 15,
    paddingHorizontal: 10,
    backgroundColor: '#fff',
    borderRadius:50,
  },
  headerTitle: {
    fontSize: 26,
    fontWeight: 'bold',
    color: 'black',
  },
  addFriendButton: {
    backgroundColor: '#fff',
    padding: 10,
    borderRadius: 30,
    borderWidth: 1,
    borderColor: '#fff',
  },
  totalAmountContainer: {
    padding: 35,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#fff',
    shadowColor: '#071718',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.2,
    shadowRadius: 3,
    elevation: 10,
    borderRadius:20,
  },
  totalNetAmountTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 10,
  },
  totalAmount: {
    fontSize: 25,
    fontWeight: 'bold',
    color: '#333',
  },
  speedometerContainer: {
    alignItems: 'center',
    padding: 20,
  },
  speedometerText: {
    fontSize: 16,
    color: '#333',
    marginTop: 10,
  },
  listContainer: {
    paddingVertical: 20,
  },
  debtItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    padding: 15,
    borderBottomWidth: 1,
    borderColor: '#ccc',
    width: '100%',
  },
  friendName: {
    fontSize: 18,
    color: '#333',
  },
  amount: {
    fontSize: 18,
  },
  speedometerContainer: {
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#fff',  // Assuming a light background
    borderRadius: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowRadius: 8,
    shadowOpacity: 0.2,
    elevation: 10,
    marginTop:5,
  },
  speedometerText: {
    fontSize: 18,
    color: '#333',
    marginTop: 10,
    fontWeight: 'bold',
  },
});
