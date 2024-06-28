import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

const ChangePassword = ({ navigation }) => {
    const [oldPassword, setOldPassword] = useState('');
    const [newPassword, setNewPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');

    const handleChangePassword = async () => {
        if (newPassword !== confirmPassword) {
            Alert.alert("Error", "New password and confirm password do not match.");
            return;
        }

        const sessionKey = await AsyncStorage.getItem('sessionKey');
        const token = await AsyncStorage.getItem('jwt_token');

        if (!sessionKey || !token) {
            Alert.alert("Error", "Authentication error. Please login again.");
            return;
        }

        try {
            const response = await fetch('http://127.0.0.1:5000/passwordapi', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                    'session-key': sessionKey
                },
                body: JSON.stringify({
                    old_password: oldPassword,
                    new_password: newPassword
                })
            });

            const jsonResponse = await response.json();
            if (response.ok) {
                Alert.alert("Success", "Password changed successfully.");
                navigation.goBack();
            } else {
                Alert.alert("Error", jsonResponse.message || "Failed to change password.");
            }
        } catch (error) {
            console.error(error);
            Alert.alert("Error", "An error occurred while trying to change the password.");
        }
    };

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Change Password</Text>
            <TextInput
                style={styles.input}
                secureTextEntry
                placeholder="Old Password"
                value={oldPassword}
                onChangeText={setOldPassword}
            />
            <TextInput
                style={styles.input}
                secureTextEntry
                placeholder="New Password"
                value={newPassword}
                onChangeText={setNewPassword}
            />
            <TextInput
                style={styles.input}
                secureTextEntry
                placeholder="Confirm New Password"
                value={confirmPassword}
                onChangeText={setConfirmPassword}
            />
            <TouchableOpacity style={styles.button} onPress={handleChangePassword}>
                <Text style={styles.buttonText}>Change Password</Text>
            </TouchableOpacity>
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
        padding: 20,
        backgroundColor: '#f5f5f5'
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        color: '#333'
    },
    input: {
        width: '95%',
        height: 50,
        marginBottom: 15,
        borderWidth: 1,
        borderColor: '#ccc',
        padding: 10,
        borderRadius: 5,
        backgroundColor: '#fff',
        fontSize: 16
    },
    button: {
        width: '100%',
        padding: 15,
        borderRadius: 5,
        alignItems: 'center',
        backgroundColor: '#00EED0',
        marginTop: 10,
    },
    buttonText: {
        fontSize: 18,
        color: '#fff',
        fontWeight: 'bold'
    }
});

export default ChangePassword;
