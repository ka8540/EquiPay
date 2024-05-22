import React from 'react';
import { View, Button } from 'react-native';

const Menu = ({ navigation }) => {
  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Button
        title="Add Item"
        onPress={() => navigation.navigate('AddItem')}
      />
    </View>
  );
};

export default Menu;
