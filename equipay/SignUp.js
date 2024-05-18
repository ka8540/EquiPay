import React, { useState } from 'react';
import { SafeAreaView, Alert, StyleSheet, Text, View, TextInput, TouchableOpacity} from 'react-native';
import { StatusBar } from 'expo-status-bar';

export default function SignUp({ navigation }) {
  const [firstname, setFirstName] = useState('');
  const [lastname, setLastName] = useState('');
  const [email, setEmail] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmpassword,setConfirmPassword] = useState('');

  const handleSubmit = () => {
    if (password !== confirmpassword) {
      Alert.alert("Password Mismatch", "The passwords do not match. Please try again.");
      return;
    }
    if (!firstname || !lastname || !email || !username || !password || !confirmpassword) {
      Alert.alert("Invalid Input", "Please fill in all fields.");
      return;
    }
    if(!email.includes('@')){
      Alert.alert("Invalid Email","email should contain @.")
      return;
    }
    // Endpoint URL
    const url = 'http://127.0.0.1:5000/signUp';
  
    // Form data to be sent
    const formData = {
      firstname: firstname,
      lastname: lastname,
      email: email,
      username: username,
      password: password,
      confirmpassword: confirmpassword,
    };
  
    // POST request options
    const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData),
    };
  
    fetch(url, requestOptions)
    .then(response => {
      if (response.ok) {
        return response.json();
      } else if (response.status === 409) {
        // Correctly handle the case when a user already exists
        Alert.alert("User Exists", "This username is already taken. Please choose another one.");
        return Promise.reject(new Error('User already exists'));
      } else {
        throw new Error('Network response was not ok.');
      }
    })
    .then(data => {
      console.log(data);
      Alert.alert("User Registered", "Registration has been completed");
      navigation.navigate('SignUp');
      navigation.reset({
        index: 0,
        routes: [{ name: 'Login' }],
      });
    })
    .catch(error => {
      console.error('There was an error!', error);
      if (error.message !== 'User already exists') {
        Alert.alert("Network Error", "Failed to submit form. Please check your network connection and try again.");
      }
    });

  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar style="auto" />
      
      {/* Orange Navbar */}
      <View style={styles.navbar}>
      </View>
      
      {/* App Content */}
      <View style={styles.content}>
        <Text style={styles.header}>Sign Up</Text>
        <View style={styles.row}>
        <TextInput
          style={[styles.input, styles.halfInput]}
          placeholder="Firstname"
          value={firstname}
          onChangeText={setFirstName}
        />
        <TextInput
          style={[styles.input, styles.halfInput]}
          placeholder="Lastname"
          value={lastname}
          onChangeText={setLastName}
        />
      </View>
        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
        />

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

        <TextInput
          style={styles.input}
          placeholder="ConfirmPassword"
          value={confirmpassword}
          onChangeText={setConfirmPassword}
          keyboardType="default" 
          secureTextEntry={true}
        />

        <TouchableOpacity onPress={handleSubmit} style={styles.button}>
          <Text style={styles.buttonText}>Sign Up</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  navbar: {
    backgroundColor: 'orange',
    alignItems: 'center',
    justifyContent: 'flex-start',
    flexDirection: 'row',
    paddingHorizontal: 10,
  },
  navbarText: {
    color: '#fff',
    fontSize: 18,
    fontWeight: 'bold',
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
  input: {
    height: 50,
    marginVertical: 10,
    borderWidth: 1,
    padding: 15,
    width: '90%',
    borderRadius: 10,
    backgroundColor: '#fff',
  },
  button: {
    backgroundColor: 'navy',
    padding: 15,
    marginTop: 20,
    borderRadius: 10,
    width: '90%',
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  image: {
    width: 120, 
    height: 100,
    borderRadius: 10,
    marginVertical: 10,
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '90%',
  },
  halfInput: {
    width: '48%', 
  }
  
});