import React from 'react';
import { StyleSheet, View } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import Login from './Login';
import SignUp from './SignUp';
import Home from './Home';
import Account from './Account';
import Menu from './Menu';
import AddItem from './Add';
import Group from './Group';
import Activity from './Activity.Js';
import ViewProfile from './ViewProfile';
import ChangePassword from './ChangePassword';
import AdvancedFeatures from './AdvancedFeatures'; // Assuming you have this component
import EditProfile from './EditProfile'; // Assuming you have this component
import ImageUploader from './ImageUploder';

const Stack = createNativeStackNavigator();
const Tab = createBottomTabNavigator();

function MenuStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Menu" component={Menu} />
      <Stack.Screen name="AddItem" component={AddItem} />
    </Stack.Navigator>
  );
}

function MainAppTabs() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          if (route.name === 'Home') {
            iconName = focused ? 'home' : 'home-outline';
          } else if (route.name === 'MenuStack') {
            iconName = focused ? 'menu' : 'menu-outline';
          } else if (route.name === 'Account') {
            iconName = focused ? 'person' : 'person-outline';
          } else if (route.name === 'Group') {
            iconName = focused ? 'people' : 'people-outline';
          } else if (route.name === 'Activity') {
            iconName = focused ? 'stats-chart' : 'stats-chart-outline';
          }
          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: 'black',
        tabBarInactiveTintColor: 'gray',
        tabBarStyle: { backgroundColor: '#D1FFFF' },
      })}
    >
      <Tab.Screen name="Home" component={Home} />
      <Tab.Screen name="Group" component={Group} />
      <Tab.Screen name="MenuStack" component={MenuStack} options={{ title: 'Menu' }} />
      <Tab.Screen name="Activity" component={Activity} />
      <Tab.Screen name="Account" component={Account} />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <View style={{ flex: 1, backgroundColor: '#fff' }}>
      <NavigationContainer>
        <Stack.Navigator initialRouteName="Login" screenOptions={{ headerShown: false }}>
          <Stack.Screen name="Login" component={Login} />
          <Stack.Screen name="SignUp" component={SignUp} />
          <Stack.Screen name="MainApp" component={MainAppTabs} />
          <Stack.Screen name="ViewProfile" component={ViewProfile} />
          <Stack.Screen name="ChangePassword" component={ChangePassword} />
          <Stack.Screen name="AdvancedFeatures" component={AdvancedFeatures} />
          <Stack.Screen name="EditProfile" component={EditProfile} />
          <Stack.Screen name ="ImageUploder" component={ImageUploader} />
        </Stack.Navigator>
      </NavigationContainer>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
