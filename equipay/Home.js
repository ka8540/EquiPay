import React from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';

export default function Home({ navigation }) {
  return (
    <View style={styles.container}>
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
    flexDirection: 'column',
    alignItems: 'center',
  },
  menuButton: {
    padding: 15,
    margin: 10,
    backgroundColor: '#007AFF',
    borderRadius: 5,
    width: 200,
    alignItems: 'center',
  },
  menuText: {
    color: '#fff',
    fontSize: 18,
  },
});
