import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const EditProfile = ({ navigation }) => {
    const [username, setUsername] = useState('');
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [editable, setEditable] = useState(false);
    const [email, setEmail] = useState('');

    useEffect(() => {
        const fetchUserProfile = async () => {
            const token = await AsyncStorage.getItem('jwt_token');
            const sessionKey = await AsyncStorage.getItem('sessionKey');
            if (!token || !sessionKey) {
                Alert.alert("Session Error", "Authentication credentials not found");
                return;
            }
            try {
                const response = await fetch('http://127.0.0.1:5000/accountapi', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                        'session-key': sessionKey
                    }
                });
                const data = await response.json();
                console.log("Fetched Data", data); // Debugging to check the fetched data
                if (response.ok && data.length > 0) {
                    const userDetails = data[0];
                    setUsername(userDetails.username);
                    setFirstName(userDetails.firstname);
                    setLastName(userDetails.lastname);
                    setEmail(userDetails.email);
                } else {
                    Alert.alert("Fetch Error", "No user data found.");
                }
            } catch (error) {
                console.error('Fetch Error:', error);
                Alert.alert("Fetch Error", "Unable to fetch user data");
            }
        };
        fetchUserProfile();
    }, []);

    const handleUpdate = async () => {
        const token = await AsyncStorage.getItem('jwt_token');
        const sessionKey = await AsyncStorage.getItem('sessionKey');
        if (!token || !sessionKey) {
            Alert.alert("Session Error", "Authentication credentials not found");
            return;
        }
        try {
            const response = await fetch('http://127.0.0.1:5000/accountapi', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    'session-key': sessionKey
                },
                body: JSON.stringify({
                    username,
                    firstname: firstName,
                    lastname: lastName,
                    email: email
                })
            });
            const data = await response.json();
            if (response.ok) {
                Alert.alert("Update Success", "Profile updated successfully");
                navigation.goBack(); // or update UI accordingly
            } else {
                Alert.alert("Update Error", data.message || "Failed to update profile");
            }
        } catch (error) {
            console.error('Update Error:', error);
            Alert.alert("Update Error", "Unable to update profile");
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Edit Profile</Text>
            <TextInput
                style={styles.input}
                value={username}
                onChangeText={setUsername}
                editable={editable}
            />
            <TextInput
                style={styles.input}
                value={firstName}
                onChangeText={setFirstName}
                editable={editable}
            />
            <TextInput
                style={styles.input}
                value={lastName}
                onChangeText={setLastName}
                editable={editable}
            />
            <TextInput
                style={styles.input}
                value={email}
                onChangeText={setEmail}
                editable={editable}
            />
            <TouchableOpacity style={styles.button} onPress={() => setEditable(!editable)}>
                <Text style={styles.buttonText}>{editable ? "Submit" : "Edit"}</Text>
            </TouchableOpacity>
            {editable && (
                <TouchableOpacity style={styles.button} onPress={handleUpdate}>
                    <Text style={styles.buttonText}>Submit Changes</Text>
                </TouchableOpacity>
            )}
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        padding: 20,
        backgroundColor: '#f5f5f5'
    },
    title: {
        fontSize: 22,
        fontWeight: 'bold',
        marginBottom: 20
    },
    input: {
        width: '90%',
        marginVertical: 10,
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        fontSize: 16,
        borderRadius: 5,
        backgroundColor: '#fff'
    },
    button: {
        marginTop: 10,
        backgroundColor: '#00aaff',
        padding: 10,
        borderRadius: 5
    },
    buttonText: {
        color: '#fff',
        fontSize: 18
    }
});

export default EditProfile;
