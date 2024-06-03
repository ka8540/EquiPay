import AsyncStorage from '@react-native-async-storage/async-storage';
import React from 'react';
import { SafeAreaView, Text, StyleSheet, TouchableOpacity, FlatList, Alert } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

export default function Account({ navigation }) {
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
                        const token = await AsyncStorage.getItem('jwt_token');
                        const sessionKey = await AsyncStorage.getItem('sessionKey');
                        if (!token || !sessionKey) {
                            console.error('JWT token or session key not found');
                            return;
                        }
    
                        const response = await fetch('http://127.0.0.1:5000/logout', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                                'Authorization': `Bearer ${token}`,
                            },
                            body: JSON.stringify({ session_key: sessionKey })
                        });
    
                        if (!response.ok) {
                            throw new Error('Failed to log out');
                        }
    
                        await AsyncStorage.removeItem('sessionKey');
                        await AsyncStorage.removeItem('jwt_token');
                        navigation.reset({
                            index: 0,
                            routes: [{ name: 'Login' }],
                        });
                    }
                }
            ]
        );
    };
    
    const menuItems = [
        {
            id: '1',
            title: 'Profile',
            icon: 'account-circle',
            action: () => navigation.navigate('EditProfile')
        },
        {
            id: '2',
            title: 'Change Password',
            icon: 'lock-reset',
            action: () => navigation.navigate('ChangePassword')
        },
        {
            id: '3',
            title: 'Advanced Features',
            icon: 'feature-search',
            action: () => navigation.navigate('AdvancedFeatures')
        },
    ];

    const renderItem = ({ item }) => (
        <TouchableOpacity style={styles.item} onPress={item.action}>
            <MaterialCommunityIcons name={item.icon} size={35} color="black" />
            <Text style={styles.title}>{item.title}</Text>
        </TouchableOpacity>
    );

    return (
        <SafeAreaView style={styles.container}>
            <FlatList
                data={menuItems}
                renderItem={renderItem}
                keyExtractor={item => item.id}
            />
            <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
                <Text style={styles.logoutButtonText}>Log out</Text>
            </TouchableOpacity>
        </SafeAreaView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    item: {
        flexDirection: 'row',
        padding: 30, 
        marginVertical: 12, 
        alignItems: 'center',
        borderBottomWidth: 1,  
        borderBottomColor: '#ccc', 
    },
    title: {
        marginLeft: 20, 
        fontSize: 22, 
        fontWeight: 'bold', 
    },
    logoutButton: {
        backgroundColor: 'navy',
        padding: 20,
        justifyContent: 'center',
        alignItems: 'center',
        marginTop: 20, 
    },
    logoutButtonText: {
        fontSize: 20,
        color: '#fff',
        fontWeight: 'bold',
    },
});
