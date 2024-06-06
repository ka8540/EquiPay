import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { MaterialIcons } from '@expo/vector-icons';

export default function Home({ navigation }) {
  return (
    <View style={styles.container}>
      {/* Positioned the AddFriends button at the top-right corner with a white background */}
      <TouchableOpacity 
        style={styles.addFriendButton}
        onPress={() => navigation.navigate('AddFriends')}
      >
        <MaterialIcons name="person-add" size={28} color="black" />
      </TouchableOpacity>

      <View style={styles.menu}>
        <TouchableOpacity
          style={styles.menuButton}
          onPress={() => navigation.navigate('Home')}
        >
          <Text style={styles.menuText}>Home</Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={styles.menuButton}
          onPress={() => navigation.navigate('Account')}
        >
          <Text style={styles.menuText}>Account</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    justifyContent: 'center',
    alignItems: 'center',
  },
  menu: {
    flexDirection: 'row',
    alignItems: 'center',
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
    position: 'absolute',
    right: 10,
    top: 60,  // Adjust this value to better fit your layout, considering the status bar height
    backgroundColor: '#fff',  // Set background color to white
    padding: 10,
    borderRadius: 30,
    borderWidth: 1,
    borderColor: '#fff'  // Optional: add a border to make the button more visible
  }
});
