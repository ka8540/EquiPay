import React, { useState } from 'react';
import { View, TextInput, Button, Text, StyleSheet, Alert, Image } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';
import * as ImagePicker from 'expo-image-picker';

const AddGroupExpense = ({ route, navigation }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [includeSelf, setIncludeSelf] = useState(false);
  const [message, setMessage] = useState('');
  const [imageUri, setImageUri] = useState(null);
  const { groupId, selectedUserIds } = route.params;

  const handleSplitExpense = async () => {
    const token = await AsyncStorage.getItem('jwt_token');
    if (!token) {
      setMessage('JWT token is missing.');
      return;
    }

    try {
      const response = await axios.post(`http://192.168.0.137:31000/group_expense/${groupId}`, {
        amount: parseFloat(amount),
        friend_ids: selectedUserIds,
        include_self: includeSelf,
        description: description
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setMessage(response.data.message);
      Alert.alert("Success", "Group expense split successfully.", [{ text: "OK", onPress: () => navigation.goBack() }]);
    } catch (error) {
      setMessage('Failed to split group expense: ' + (error.response ? error.response.data.message : error.message));
      Alert.alert("Error", "Failed to split group expense.", [{ text: "OK" }]);
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

    setImageUri(firstAsset.uri); // Update state to show the preview
    const filename = firstAsset.uri.split('/').pop();
    const type = firstAsset.type || 'image/jpeg';

    const formData = new FormData();
    formData.append('file', { uri: firstAsset.uri, name: filename, type });

    axios.post('http://192.168.0.137:31000/upload-and-analyze', formData, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'multipart/form-data',
      },
    })
    .then(response => {
      if (response.data.total_amount && response.data.shop_name) {
        setAmount(response.data.total_amount);
        setDescription(response.data.shop_name);
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
  message: {
    marginTop: 20,
    fontSize: 16,
    color: 'red',
  }
});

export default AddGroupExpense;
