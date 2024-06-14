import React, { useState } from 'react';
import { View, TextInput, Button, Text, Switch, Alert, StyleSheet, Image } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import * as ImagePicker from 'expo-image-picker';

const AddItem = ({ route, navigation }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [includeSelf, setIncludeSecretly] = useState(false);
  const [message, setMessage] = useState('');
  const [imageUri, setImageUri] = useState(null);
  const { userIds } = route.params;

  const handleSplitExpense = async () => {
    const sessionKey = await AsyncStorage.getItem('sessionKey');
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token || !sessionKey) {
      setMessage('Session key or token is missing.');
      return;
    }

    try {
      const response = await axios.post('http://127.0.0.1:5000/split-expense', {
        amount: parseFloat(amount),
        friend_ids: userIds,
        include_self: includeSelf,
        description: description
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Session-Key': sessionKey,
        },
      });
      setMessage(response.data.message);
      Alert.alert("Success", "Expense split successfully.", [{ text: "OK", onPress: () => navigation.goBack() }]);
    } catch (error) {
      setMessage('Failed to split expense: ' + (error.response ? error.response.data.message : error.message));
      Alert.alert("Error", "Failed to split expense.", [{ text: "OK" }]);
    }
  };

  const pickImageAndUpload = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token) {
      Alert.alert("Error", "JWT token not found");
      return;
    }

    let permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (!permissionResult.granted) {
      Alert.alert("Permission Required", "Permission to access camera roll is required!");
      return;
    }

    let result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      aspect: [4, 3],
      quality: 1,
    });

    if (result.cancelled) {
      Alert.alert("Cancelled", "Image selection was cancelled.");
      return;
    }

    const firstAsset = result.assets && result.assets[0];
    if (!firstAsset || !firstAsset.uri) {
      Alert.alert("Error", "No image was selected.");
      return;
    }

    setImageUri(firstAsset.uri);
    const filename = firstAsset.uri.split('/').pop();
    const type = firstAsset.type || 'image/jpeg';

    const formData = new FormData();
    formData.append('file', {
      uri: firstAsset.uri,
      name: filename,
      type: type,
    });

    fetch('http://127.0.0.1:5000/upload-and-analyze', {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => response.json())
    .then(response => {
      if (response.total_amount && response.shop_name) {
        setAmount(response.total_amount);
        setDescription(response.shop_name);
        Alert.alert("Upload Successful", "Image analyzed successfully.");
      } else {
        Alert.alert("Error", "Image analyzed but no data found.");
      }
    })
    .catch(error => {
      console.error('Upload Error:', error);
      Alert.alert("Upload Error", "An error occurred during the upload.");
    });
  };

  return (
    <View style={styles.container}>
      <TextInput
        placeholder="$ Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
        style={styles.input}
      />
      <TextInput
        placeholder="Description"
        value={description}
        onChangeText={setDescription}
        style={styles.input}
      />
      <View style={styles.switchContainer}>
        <Text style={styles.label}>Include Yourself:</Text>
        <Switch
          trackColor={{ false: "#767577", true: "#d3ff4d" }}
          thumbColor={includeSelf ? "#f9ffe5" : "#d3ff4d"}
          onValueChange={setIncludeSecretly}
          value={includeSelf}
        />
      </View>
      <Button title="Add Image" onPress={pickImageAndUpload} />
      <Button title="Split Expense" onPress={handleSplitExpense} />
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
    backgroundColor: '#f9f9f9',
  },
  input: {
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
    width: '80%',
    marginBottom: 20,
    fontSize: 18,
    padding: 10,
  },
  image: {
    width: 300,
    height: 300,
    resizeMode: 'contain',
    margin: 20,
  },
  switchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  label: {
    marginRight: 10,
    fontSize: 16,
  },
  message: {
    marginTop: 20,
    fontSize: 16,
    color: 'red',
  }
});

export default AddItem;
