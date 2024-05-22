import React, { useState } from 'react';
import { View, TextInput, Button, Text, FlatList, StyleSheet } from 'react-native';

const Activity = () => {
  const [activityName, setActivityName] = useState('');
  const [activities, setActivities] = useState([]);

  const addActivity = () => {
    if (activityName.trim() !== '') {
      setActivities([...activities, activityName]);
      setActivityName('');
    }
  };

  return (
    <View style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Enter Activity Name"
        value={activityName}
        onChangeText={setActivityName}
      />
      <Button title="Add Activity" onPress={addActivity} />
      <FlatList
        data={activities}
        keyExtractor={(item, index) => index.toString()}
        renderItem={({ item }) => (
          <View style={styles.activityItem}>
            <Text style={styles.activityText}>{item}</Text>
          </View>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#fff',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 10,
    paddingHorizontal: 10,
  },
  activityItem: {
    padding: 10,
    marginVertical: 5,
    backgroundColor: '#f9f9f9',
    borderColor: '#ddd',
    borderWidth: 1,
    borderRadius: 5,
  },
  activityText: {
    fontSize: 16,
  },
});

export default Activity;
