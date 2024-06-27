import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, FlatList, StyleSheet, RefreshControl, SafeAreaView } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Activity = () => {
  const [logs, setLogs] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const fetchActivities = async () => {
    setRefreshing(true);
    try {
      const token = await AsyncStorage.getItem('jwt_token');
      console.log("TokenActivity:", token);
      const response = await fetch('http://127.0.0.1:5000/activity', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });
      const json = await response.json();
      if (json.logs) {
        setLogs(json.logs.map(log => ({
          ...log,
          icon: getIconName(log.actiontype) // Assuming a function to get icon names
        })));
      } else {
        console.error('No logs found', json);
      }
    } catch (error) {
      console.error('Failed to fetch activities', error);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchActivities(); // Fetch logs initially
  }, []);

  const onRefresh = useCallback(() => {
    fetchActivities();
  }, [fetchActivities]);

  const formatDate = (timestamp) => {
    const date = new Date(timestamp);
    return `${date.getDate()}/${date.getMonth() + 1}`;  // JavaScript months are 0-indexed
  };

  // Utility to decide icon based on the action type
  const getIconName = (actionType) => {
    switch (actionType) {
      case 'Added Expense':
        return 'cash-plus';
      case 'Created Group':
        return 'account-group';
      case 'Incurred Debt':
        return 'bank';
      default:
        return 'file-document';
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <Text style={styles.header}>Recent Activity</Text>
      <FlatList
        data={logs}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.logItem}>
            <MaterialCommunityIcons name={item.icon} size={24} color="#4CAF50" />
            <View style={styles.textContainer}>
              <Text style={styles.logText}>{item.actiontype} - {formatDate(item.timestamp)}</Text>
              <Text style={styles.logDetail}>{item.details}</Text>
            </View>
          </View>
        )}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={onRefresh}
          />
        }
      />
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingTop: 10,
  },
  header: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#333',
    padding: 20,
    backgroundColor: '#FFFFFF',
    textAlign: 'center',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 3,
    elevation: 3,
  },
  logItem: {
    flexDirection: 'row',
    padding: 15,
    marginVertical: 8,
    backgroundColor: '#FFFFFF',
    borderRadius: 10,
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
    elevation: 2,
    marginLeft: 20,
    marginRight: 20,
    alignItems: 'center',
  },
  textContainer: {
    marginLeft: 15,
    flex: 1,
  },
  logText: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#2C3E50',
  },
  logDetail: {
    fontSize: 14,
    color: '#34495E',
  },
});

export default Activity;
