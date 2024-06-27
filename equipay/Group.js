import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator, RefreshControl } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { useNavigation } from '@react-navigation/native';

const Group = () => {
  const [groups, setGroups] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const navigation = useNavigation();

  useEffect(() => {
    fetchGroups();
  }, []);

  const fetchGroups = async () => {
    setIsLoading(true);
    const token = await AsyncStorage.getItem('jwt_token');
    if (token) {
      fetch('http://127.0.0.1:5000/user_group', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then(response => response.json())
      .then(data => {
        setGroups(data.length ? data : ['No groups']);
      })
      .catch(error => {
        console.error('Error fetching groups:', error);
        setGroups(['No groups']);
      })
      .finally(() => {
        setIsLoading(false);
        setRefreshing(false);
      });
    } else {
      setGroups(['No groups']);
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    fetchGroups();  
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => navigation.navigate('GroupAddMembers')}>
          <MaterialCommunityIcons name="account-multiple-plus" size={30} color="#000" />
        </TouchableOpacity>
      </View>
      {isLoading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        <FlatList
          data={groups}
          keyExtractor={(item, index) => index.toString()}
          renderItem={({ item }) => (
            <TouchableOpacity
              style={styles.groupItem}
              onPress={() => typeof item === 'object' && navigation.navigate('GroupMembersDashboard', { group_id: item.group_id })}
            >
              <Text style={styles.groupText}>{typeof item === 'string' ? item : item.group_name}</Text>
            </TouchableOpacity>
          )}
          ListEmptyComponent={() => (
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No groups</Text>
            </View>
          )}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
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
    backgroundColor: '#fff',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'flex-end',
    marginBottom: 20,
    marginTop: 50, 
  },
  groupItem: {
    padding: 10,
    marginVertical: 5,
    backgroundColor: '#f9f9f9',
    borderColor: '#ddd',
    borderWidth: 1,
    borderRadius: 5,
    marginTop: 15,
  },
  groupText: {
    fontSize: 16,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  emptyText: {
    fontSize: 18,
    color: '#666',
  },
});

export default Group;
