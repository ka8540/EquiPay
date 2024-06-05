import AsyncStorage from '@react-native-async-storage/async-storage';
import React, { useState, useEffect } from 'react';
import { SafeAreaView, Text, StyleSheet, TouchableOpacity, FlatList, Alert, Image, View } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';

const Account = ({ navigation }) => {
    const [profileImageUrl, setProfileImageUrl] = useState(null);

    useEffect(() => {
        const fetchProfileImage = async () => {
            const sessionKey = await AsyncStorage.getItem('sessionKey');
            const token = await AsyncStorage.getItem('jwt_token');
            if (sessionKey && token) {
                try {
                    const response = await fetch('http://127.0.0.1:5000/upload', {
                        method: 'GET',
                        headers: {
                            'Authorization': `Bearer ${token}`,
                            'Session-Key': sessionKey
                        }
                    });
                    const data = await response.json();
                    console.log("Fetched image data:", data);
                    // Check if the response is ok and data.url is not empty
                    if (response.ok && data.url && data.url.length > 0) {
                        setProfileImageUrl(data.url[0]); // Access the first element if it's an array
                    } else {
                        setProfileImageUrl(null);  // Use null for no image and handle the UI accordingly
                    }
                } catch (error) {
                    console.error('Error fetching profile image:', error);
                    setProfileImageUrl(null);
                }
            }
        };
        fetchProfileImage();
    }, []);

    const handleLogout = async () => {
        Alert.alert(
            "Logout",
            "Are you sure you want to logout?",
            [
                { text: "Cancel", onPress: () => console.log("Cancel Pressed"), style: "cancel" },
                { text: "Yes", onPress: async () => {
                    await AsyncStorage.removeItem('sessionKey');
                    await AsyncStorage.removeItem('jwt_token');
                    navigation.reset({
                        index: 0,
                        routes: [{ name: 'Login' }],
                    });
                }}
            ]
        );
    };

    const menuItems = [
        { id: '1', title: 'Profile', icon: 'account-circle-outline', action: () => navigation.navigate('ViewProfile') },
        { id: '2', title: 'Change Password', icon: 'lock-reset', action: () => navigation.navigate('ChangePassword') },
        { id: '3', title: 'Advanced Features', icon: 'feature-search-outline', action: () => navigation.navigate('AdvancedFeatures') },
        { id: '4', title: 'Edit Profile', icon: 'account-edit-outline', action: () => navigation.navigate('EditProfile') },
    ];

    const renderItem = ({ item }) => (
        <TouchableOpacity style={styles.item} onPress={item.action}>
            <MaterialCommunityIcons name={item.icon} size={35} color="black" />
            <Text style={styles.title}>{item.title}</Text>
        </TouchableOpacity>
    );

    return (
        <SafeAreaView style={styles.container}>
            {profileImageUrl ? (
                <Image source={{ uri: profileImageUrl }} style={styles.profilePic} />
            ) : (
                <View style={[styles.profilePic, styles.profilePicPlaceholder]}>
                    <Text style={styles.placeholderText}>No Image Available</Text>
                </View>
            )}
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
};

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
    },
    item: {
        flexDirection: 'row',
        padding: 22, 
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
    profilePic: {
        width: 150,
        height: 150,
        borderRadius: 80,
        alignSelf: 'center',
        marginBottom: 20,
        marginTop:20,
    },
    profilePicPlaceholder: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#e1e4e8',
        width: 100,
        height: 100,
        borderRadius: 50,
        alignSelf: 'center',
        marginBottom: 20,
    },
    placeholderText: {
        color: '#000',
        fontSize: 16,
    },
});

export default Account;
