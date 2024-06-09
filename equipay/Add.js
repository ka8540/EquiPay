import React, { useState } from 'react';
import { View, TextInput, Button, Text, Switch, Alert, StyleSheet } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const AddItem = ({ route, navigation }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [includeSelf, setIncludeSecretly] = useState(false);
  const [message, setMessage] = useState('');
  const { userIds } = route.params;  // Receive userIds from previous screen

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
