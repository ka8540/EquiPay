import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, TouchableOpacity, Image } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { MaterialIcons } from '@expo/vector-icons';

const ViewProfile = ({ navigation }) => {
    const [isLoading, setIsLoading] = useState(true);
    const [userData, setUserData] = useState({});
    const [profileImageUrl, setProfileImageUrl] = useState(null);

    useEffect(() => {
        const fetchUserData = async () => {
            const sessionKey = await AsyncStorage.getItem('sessionKey');
            const token = await AsyncStorage.getItem('jwt_token');

            if (!sessionKey || !token) {
                console.error("Session key or JWT token not found");
                setIsLoading(false);
                return;
            }

            try {
                const userResponse = await fetch('http://192.168.0.137:31000/accountapi', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Session-Key': sessionKey,
                        'Content-Type': 'application/json'
                    }
                });

                if (!userResponse.ok) {
                    throw new Error("Failed to fetch user data");
                }

                const userData = await userResponse.json();

                if (userData && userData.length > 0) {
                    const userDetails = userData[0];
                    setUserData({
                        username: userDetails.username,
                        firstname: userDetails.firstname,
                        lastname: userDetails.lastname
                    });
                } else {
                    console.error("Received empty data array");
                }

                const imageResponse = await fetch('http://192.168.0.137:31000/upload', {
                    method: 'GET',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Session-Key': sessionKey
                    }
                });

                if (!imageResponse.ok) {
                    throw new Error("Failed to fetch profile image");
                }

                const imageResult = await imageResponse.json();
                if (imageResult.url) {
                    setProfileImageUrl(imageResult.url[0]); 
                } else {
                    setProfileImageUrl(null);
                }
                setIsLoading(false);
            } catch (error) {
                console.error("Error fetching data:", error);
                setIsLoading(false);
            }
        };

        fetchUserData();
    }, []);

    if (isLoading) {
        return <View style={styles.container}><ActivityIndicator size="large" color="#0000ff" /></View>;
    }

    return (
        <View style={styles.container}>
            <View style={styles.card}>
                {profileImageUrl ? (
                    <Image source={{ uri: profileImageUrl }} style={styles.profilePic} />
                ) : (
                    <View style={[styles.profilePic, styles.profilePicPlaceholder]}>
                        <Text style={styles.placeholderText}>No Image Available</Text>
                    </View>
                )}
                <Text style={styles.title}>User Profile</Text>
                <View style={styles.detailRow}>
                    <MaterialIcons name="person-outline" size={24} color="black" />
                    <Text style={styles.detail}>Username: {userData.username}</Text>
                </View>
                <View style={styles.detailRow}>
                    <MaterialIcons name="face" size={24} color="black" />
                    <Text style={styles.detail}>First Name: {userData.firstname}</Text>
                </View>
                <View style={styles.detailRow}>
                    <MaterialIcons name="face" size={24} color="black" />
                    <Text style={styles.detail}>Last Name: {userData.lastname}</Text>
                </View>
                <TouchableOpacity style={styles.button} onPress={() => navigation.navigate('ImageUploader')}>
                    <Text style={styles.buttonText}>Update Profile Picture</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.button} onPress={() => navigation.goBack()}>
                    <Text style={styles.buttonText}>Back to Account</Text>
                </TouchableOpacity>
            </View>
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
    card: {
        backgroundColor: 'white',
        borderRadius: 8,
        width: '100%',
        padding: 20,
        shadowColor: "#000",
        shadowOffset: {
            width: 0,
            height: 2,
        },
        shadowOpacity: 0.25,
        shadowRadius: 3.84,
        elevation: 5,
    },
    profilePic: {
        width: 100,
        height: 100,
        borderRadius: 50,
        alignSelf: 'center',
        marginBottom: 20,
    },
    profilePicPlaceholder: {
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#e1e4e8',
    },
    placeholderText: {
        color: '#000',
        fontSize: 16,
    },
    title: {
        fontSize: 24,
        fontWeight: 'bold',
        marginBottom: 20,
        textAlign: 'center',
    },
    detailRow: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 10,
    },
    detail: {
        fontSize: 18,
        marginLeft: 10,
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

export default ViewProfile;
