import React from 'react';
import { View, Text, Button, Alert, StyleSheet, TouchableOpacity } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const AdvancedFeatures = ({ navigation }) => {
    const handleDeleteAccount = async () => {
        // Confirm before deleting
        Alert.alert(
            "Delete Account",
            "Are you sure you want to permanently delete your account?",
            [
                {
                    text: "Cancel",
                    onPress: () => console.log("Cancel Pressed"),
                    style: "cancel"
                },
                { 
                    text: "Yes", 
                    onPress: () => deleteAccount() 
                }
            ]
        );
    };

    const deleteAccount = async () => {
        const sessionKey = await AsyncStorage.getItem('sessionKey');
        const token = await AsyncStorage.getItem('jwt_token');

        if (!sessionKey || !token) {
            console.error("Session key or JWT token not found");
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/deleteaccount', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Session-Key': sessionKey,
                    'Content-Type': 'application/json'
                }
            });

            const responseData = await response.json();
            if (response.ok) {
                // Clear session storage and perform logout
                await AsyncStorage.clear();
                Alert.alert("Account Deleted", "Your account has been successfully deleted.", [
                    { text: "OK", onPress: () => navigation.navigate('Login') }
                ]);
            } else {
                Alert.alert("Error", responseData.message || "Failed to delete account");
            }
        } catch (error) {
            console.error("Error deleting account:", error);
            Alert.alert("Error", "An error occurred while deleting your account.");
        }
    };

    return (
        <View style={styles.container}>
            <Text>Advanced Feature Screen</Text>
            <Button
                title="Delete My Account"
                onPress={handleDeleteAccount}
                color="red"
            />
            <TouchableOpacity style={styles.button} onPress={() => navigation.goBack()}>
                <Text style={styles.buttonText}>Back to Account</Text>
            </TouchableOpacity>
        </View>
    );
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f5f5f5',
        padding: 20,
    },
    button: {
        marginTop: 20,
        backgroundColor: '#007AFF',
        padding: 10,
        borderRadius: 5,
    },
    buttonText: {
        color: 'white',
        fontSize: 18,
        textAlign: 'center',
    }
});

export default AdvancedFeatures;
