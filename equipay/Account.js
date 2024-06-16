import React, { useState, useEffect } from 'react';
import { SafeAreaView, Text, StyleSheet, TouchableOpacity, ScrollView, Alert, Image, RefreshControl, View } from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Account = ({ navigation }) => {
    const [profileImageUrl, setProfileImageUrl] = useState(null);
    const [refreshing, setRefreshing] = useState(false);

    const fetchProfileImage = async () => {
        setRefreshing(true);
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
                if (response.ok && data.url && data.url.length > 0) {
                    setProfileImageUrl(data.url[0]);
                } else {
                    setProfileImageUrl(null);
                }
            } catch (error) {
                console.error('Error fetching profile image:', error);
                setProfileImageUrl(null);
            }
        }
        setRefreshing(false);
    };

    useEffect(() => {
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

    return (
        <SafeAreaView style={styles.container}>
            <ScrollView
                contentContainerStyle={styles.scrollViewContent}
                refreshControl={
                    <RefreshControl
                        refreshing={refreshing}
                        onRefresh={fetchProfileImage}
                    />
                }
            >
                {profileImageUrl ? (
                    <Image source={{ uri: profileImageUrl }} style={styles.profilePic} />
                ) : (
                    <View style={[styles.profilePic, styles.profilePicPlaceholder]}>
                        <Text style={styles.placeholderText}>No Image Available</Text>
                    </View>
                )}
                {menuItems.map(item => (
                    <TouchableOpacity key={item.id} style={styles.item} onPress={item.action}>
                        <MaterialCommunityIcons name={item.icon} size={40} color="black" />
                        <Text style={styles.title}>{item.title}</Text>
                    </TouchableOpacity>
                ))}
            </ScrollView>
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
    scrollViewContent: {
        alignItems: 'flex-start', 
        paddingTop: 20,
    },
    item: {
        flexDirection: 'row',
        padding: 32,
        width: '100%', 
        alignItems: 'center',
        borderBottomWidth: 2,
        borderBottomColor: '#ccc',
        justifyContent: 'flex-start',
    },
    title: {
        marginLeft: 20,
        fontSize: 25,
        fontWeight: 'bold',
    },
    logoutButton: {
        position: 'absolute', 
        bottom: 0,
        left: 0,
        right: 0,
        backgroundColor: 'navy',
        padding: 20,
        justifyContent: 'center',
        alignItems: 'center',
        width: '100%',
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