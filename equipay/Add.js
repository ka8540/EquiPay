import React, { useState } from 'react';
import { View, TextInput, Button, Text } from 'react-native';

const AddItem = () => {
  const [itemName, setItemName] = useState('');
  const [itemDescription, setItemDescription] = useState('');
  const [message, setMessage] = useState('');

  const handleAddItem = () => {
    // Handle item addition logic here
    setMessage(`Item Added: ${itemName}`);
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <TextInput
        placeholder="Item Name"
        value={itemName}
        onChangeText={setItemName}
        style={{ borderBottomWidth: 1, width: '80%', marginBottom: 20 }}
      />
      <TextInput
        placeholder="Item Description"
        value={itemDescription}
        onChangeText={setItemDescription}
        style={{ borderBottomWidth: 1, width: '80%', marginBottom: 20 }}
      />
      <Button title="Add Item" onPress={handleAddItem} />
      {message ? <Text style={{ marginTop: 20 }}>{message}</Text> : null}
    </View>
  );
};

export default AddItem;
