import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState } from 'react';
import { SafeAreaView, Alert, StyleSheet, Text, View, TextInput, TouchableOpacity, Image, StatusBar } from 'react-native';

export default function Login({ navigation }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const navigateToSignUp = () => {
    navigation.navigate('SignUp');
  };

  const handleSubmit = () => {
    if (!username || !password) {
      Alert.alert("Invalid Input", "Username and password must not be empty");
      return;
    }
    const url = 'http://127.0.0.1:5000/login';
  
    const formData = {
      username: username,
      password: password,
    };
  
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    };
  
    fetch(url, requestOptions)
    .then(response => {
      if (response.ok) {
        return response.json();
      } else if (response.status === 211 || response.status === 201) {
        const statusMessage = response.status === 211 ? "Invalid Password" : "Invalid Credentials";
        Alert.alert(statusMessage, "Username or password is incorrect.");
        console.error(`Login failed with status ${response.status}`);
        return null;  
      } else {
        throw new Error(`Unhandled exception with status ${response.status}`);
      }
    })
    .then(data => {
      console.log('Data received:', data); // Log the data to see what's received
      if (!data) {
        console.log('No data received, stopping execution');
        return;
      }
      if (data.sessionKey && data.access_token) {
        AsyncStorage.setItem('sessionKey', data.sessionKey);
        AsyncStorage.setItem('jwt_token', data.access_token);
        Alert.alert("Login Successfully");
        navigation.reset({
          index: 0,
          routes: [{ name: 'MainApp' }],
        });
      } else if (data.message) {
        Alert.alert("Login Error", data.message);
      } else {
        console.error('Incomplete data received:', data);
        throw new Error('No session key or token received');
      }
    })
    .catch(error => {
      Alert.alert("Login Error", error.message);
      console.error('Login Error:', error);
    });  
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      <View style={styles.content}>
        <Image 
          source={{ uri: 'https://profile-picture-docs.s3.amazonaws.com/LogoRemade-2.png' }}  
          style={styles.image}
        />
        <Text style={styles.headerText}>EQUIPAY</Text>
        <Text style={styles.header}>Login</Text>
        <TextInput
          style={styles.input}
          placeholder="Username"
          value={username}
          onChangeText={setUsername}
          keyboardType="default"
        />
        <TextInput
          style={styles.input}
          placeholder="Password"
          value={password}
          onChangeText={setPassword}
          keyboardType="default"
          secureTextEntry={true}
        />
        <TouchableOpacity onPress={handleSubmit} style={styles.button}>
          <Text style={styles.buttonText}>Login</Text>
        </TouchableOpacity>
        <Text style={styles.signupPrompt}>
          Don't have an account? <Text onPress={navigateToSignUp} style={styles.signupLink}>Sign Up</Text>
        </Text>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  content: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    margin: 10,
  },
  headerText: {
    fontSize: 50,             // Set the font size
    fontWeight: '600',        // Medium-bold font weight
    color: '#333',            // Set the text color to a deep gray
    textAlign: 'center',      // Center the text horizontally
    marginTop: 10,            // Moderate top margin
    marginBottom: 5,          // Moderate bottom margin
    fontFamily: 'Arial',      // Arial is a close match to Amazon’s font
    marginBottom: 40,
  },  
  input: {
    height: 50,
    marginVertical: 10,
    borderWidth: 1,
    padding: 15,
    width: '80%',
    borderRadius: 10,
    backgroundColor: '#fff',
  },
  image: {
    width: 300, 
    height: 300,
    marginBottom: 20, 
    borderRadius: 60, 
  },
  button: {
    backgroundColor: 'navy',
    padding: 15,
    marginTop: 20,
    borderRadius: 10,
    width: '80%',
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  signupPrompt: {
    marginTop: 20,
    fontSize: 14,
  },
  signupLink: {
    fontWeight: 'bold',
    color: 'blue',
  }
});
