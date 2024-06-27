import React, { useState } from 'react';
import { Button, Image, View, StyleSheet, Alert, Text, TouchableOpacity } from 'react-native';
import * as ImagePicker from 'expo-image-picker';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { useRoute } from '@react-navigation/native';

const GroupImage = ({ navigation }) => {
    const [imageUri, setImageUri] = useState(null);
    const route = useRoute();
    const { group_id } = route.params; 

    const pickImageAndUpload = async () => {
        const token = await AsyncStorage.getItem('jwt_token');

        if (!token) {
            Alert.alert("Error", "JWT token not found");
            return;
        }

        let permissionResult = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (permissionResult.granted === false) {
            Alert.alert("Permission Required", "Permission to access camera roll is required!");
            return;
        }

        let result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            allowsEditing: true,
            aspect: [4, 3],
            quality: 1,
        });

        if (result.cancelled) {
            Alert.alert("Cancelled", "Image selection was cancelled.");
            return;
        }

        const firstAsset = result.assets[0];
        if (!firstAsset || !firstAsset.uri) {
            Alert.alert("Error", "No image was selected.");
            return;
        }

        const localUri = firstAsset.uri;
        setImageUri(localUri); 
        const filename = localUri.split('/').pop();
        const type = firstAsset.type || 'image';

        const formData = new FormData();
        formData.append('file', { uri: localUri, name: filename, type });

        fetch(`http://127.0.0.1:5000/group_photo/${group_id}`, {
            method: 'POST',
            body: formData,
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'multipart/form-data',
            },
        })
        .then(response => response.json())
        .then(response => {
            console.log('Upload success:', response);
            Alert.alert("Upload Successful", "Image uploaded successfully!");
        })
        .catch(error => {
            console.error('Upload Error:', error);
            Alert.alert("Upload Error", "An error occurred during the upload.");
        });
    };

    return (
        <View style={styles.container}>
            <Button title="Upload an Image" onPress={pickImageAndUpload} />
            {imageUri && (
                <View style={styles.imageContainer}>
                    <Image source={{ uri: imageUri }} style={styles.image} />
                    <Text style={styles.imageText}>Image Preview</Text>
                </View>
            )}
            <TouchableOpacity style={styles.button} onPress={() => navigation.goBack()}>
                    <Text style={styles.buttonText}>Go Back</Text>
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
    imageContainer: {
        marginTop: 20,
        alignItems: 'center',
    },
    image: {
        width: 300,
        height: 300,
        resizeMode: 'contain',
        borderRadius: 10,
    },
    imageText: {
        marginTop: 10,
        fontSize: 16,
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

export default GroupImage;
