import React, { useState } from 'react';
import { View, TextInput, Button, Text, Switch } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import axios from 'axios';

const AddItem = ({ route }) => {
  const [amount, setAmount] = useState('');
  const [description, setDescription] = useState('');
  const [includeSelf, setIncludeSelf] = useState(false);
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
    } catch (error) {
      setMessage('Failed to split expense: ' + (error.response ? error.response.data.message : error.message));
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <TextInput
        placeholder="$ Amount"
        value={amount}
        onChangeText={setAmount}
        keyboardType="numeric"
        style={{ borderBottomWidth: 1, width: '80%', marginBottom: 20 }}
      />
      <TextInput
        placeholder="Description"
        value={description}
        onChangeText={setDescription}
        style={{ borderBottomWidth: 1, width: '80%', marginBottom: 20 }}
      />
      <View style={{ flexDirection: 'row', alignItems: 'center', marginBottom: 20 }}>
        <Text>Include Yourself: </Text>
        <Switch
          onValueChange={setIncludeSelf}
          value={includeSelf}
        />
      </View>
      <Button title="Split Expense" onPress={handleSplitExpense} />
      {message ? <Text style={{ marginTop: 20 }}>{message}</Text> : null}
    </View>
  );
};

export default AddItem;
