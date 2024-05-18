import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState, useEffect } from 'react';
import { SafeAreaView, View, Text, StyleSheet, TouchableOpacity, Alert } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function Account({ navigation }) {
    const [firstName, setFirstName] = useState('');
    const [lastName, setLastName] = useState('');
    const [email, setEmail] = useState('');
    const [username, setUsername] = useState('');

    useEffect(() => {
        const fetchUserDetails = async () => {
            try {
                // Retrieve the session key from storage
                const sessionKey = await AsyncStorage.getItem('sessionKey');
                if (!sessionKey) {
                    console.error('Session key not found');
                    return;
                }

                const response = await fetch('http://127.0.0.1:5000/userdetail', {
                    method: 'GET',
                    headers: {
                        // Include the session key in the request headers
                        'X-Session-Key': sessionKey,
                    },
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                if (data && data.length > 0) {
                    const user = data[0]; // Access the first user details
                    setFirstName(user.firstname);
                    setLastName(user.lastname);
                    setEmail(user.email);
                    setUsername(user.username);
                }
            } catch (error) {
                console.error('There was an error fetching the user details:', error);
            }
        };

        fetchUserDetails();
    }, []);

    const handleLogout = async () => {
        Alert.alert(
            "Logout",
            "Are you sure you want to logout?",
            [
                {
                    text: "Cancel",
                    onPress: () => console.log("Cancel Pressed"),
                    style: "cancel"
                },
                { 
                    text: "Yes", onPress: async () => {
                        console.log("Logout Pressed");
                        // Retrieve the session key from storage
                        const sessionKey = await AsyncStorage.getItem('sessionKey');
                        if (sessionKey) {
                            // Send a POST request to the backend to notify about the logout
                            try {
                                const response = await fetch('http://127.0.0.1:5000/logout', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                        // Optionally include the session key in the headers if required
                                        'X-Session-Key': sessionKey
    
                                    },
                                    body: JSON.stringify({
                                        session_key: sessionKey, // Include session key in the body if this is your backend's expected format
                                    }),
                                });
    
                                if (!response.ok) {
                                    throw new Error('Failed to notify backend about logout');
                                }
    
                                // Handle response from the backend, if necessary
                                console.log('Logout successful, backend notified');
                                
                                // Optionally remove sessionKey from AsyncStorage here, if required
                                // await AsyncStorage.removeItem('sessionKey');
    
                                // Navigate back to the login screen or perform other cleanup
                                navigation.reset({
                                    index: 0,
                                    routes: [{ name: 'Login' }],
                                });
    
                            } catch (error) {
                                console.error('There was an error notifying the backend about logout:', error);
                            }
                        } else {
                            console.log('No session key found');
                        }
                    } 
                }
            ]
        );
    };

    return (
        <SafeAreaView style={styles.container}>

            {/* Main Content */}
            <View style={styles.content}>
                <MaterialCommunityIcons name="account-circle" size={100} color="black" />
                <Text style={styles.username}>{username}</Text>
                {/* Display additional account information here */}
                <Text style={styles.detailText}>First Name: {firstName}</Text>
                <Text style={styles.detailText}>Last Name: {lastName}</Text>
                <Text style={styles.detailText}>Email: {email}</Text>
            </View>

            {/* Logout Button */}
            <TouchableOpacity style={styles.button} onPress={handleLogout}>
                <Text style={styles.buttonText}>Logout</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    navbar: {
        height: 60,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'cyan',
    },
    navbarText: {
        fontSize: 20,
        fontWeight: 'bold',
        color: '#fff',
    },
    content: {
        flex: 1,
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 60, // Leave space for the logout button
    },
    username: {
        fontSize: 24,
        marginVertical: 20,
    },
    detailText: {
        fontSize: 18,
        marginVertical: 5,
    },
    button: {
        height: 60,
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: 'navy',
    },
    buttonText: {
        fontSize: 20,
        color: '#fff',
        fontWeight: 'bold',
    },
});