import React, { useEffect, useRef, useState } from "react";
import { CameraView, useCameraPermissions } from 'expo-camera/next';
import {
  Button,
  SafeAreaView,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
} from "react-native";
import DeviceModal from "./DeviceConnectionModal";
import useBLE from "./useBLE";
import { CameraType } from "expo-camera";

const App = () => {
  const {
    requestPermissions,
    scanForPeripherals,
    allDevices,
    connectToDevice,
    connectedDevice,
    sendCommand,
    disconnectFromDevice,
  } = useBLE();
  const [isModalVisible, setIsModalVisible] = useState<boolean>(false);
  const [permission, requestPermission] = useCameraPermissions();
  const ref = useRef<CameraView>(null);



  const scanForDevices = async () => {
    const isPermissionsEnabled = await requestPermissions();
    if (isPermissionsEnabled) {
      scanForPeripherals();
    }
  };

  const hideModal = () => {
    setIsModalVisible(false);
  };

  const openModal = async () => {
    scanForDevices();
    setIsModalVisible(true);
  };

  useEffect(() => {
    requestPermission();
  }, []);

  return (
    <SafeAreaView style={styles.container}>
      <View style={{ flex: 1, flexDirection: "column", backgroundColor: "red" }}>
        {connectedDevice ? (
          <View style={{ flex: 1 }}>
            <CameraView facing={"back"} style={{ flex: 1 }} ref={ref}>
              <View
                style={{
                  height: "100%",
                  flex: 1,
                  flexDirection: "column",
                  justifyContent: "space-between",
                  margin: 20,
                }}
              >
                <TouchableOpacity
                  style={{
                    flex: 0.2,
                    alignSelf: "flex-end",
                    alignItems: "center",
                    justifyContent: "center",
                    backgroundColor: "#666",
                    marginBottom: 40,
                    marginLeft: 20,
                  }}
                  onPress={async () => {
                    console.log("TEST");
                    const photo = await ref.current?.takePictureAsync({
                      base64: true,
                    })
                    if (photo) {
                      if (photo.base64) {
                        sendCommand(photo.base64);
                      }
                    }
                  }
                  }
                >
                  <Text style={{ fontSize: 30, padding: 10, color: "white" }}>📸</Text>
                </TouchableOpacity>
              </View>
            </CameraView>
          </View>
        ) : (
          <Text style={styles.heartRateTitleText}>
            Please Connect to a BrailleEd Device
          </Text>
        )}
      </View>
      <TouchableOpacity
        onPress={connectedDevice ? disconnectFromDevice : openModal}
        style={styles.ctaButton}
      >
        <Text style={styles.ctaButtonText}>
          {connectedDevice ? "Disconnect" : "Connect"}
        </Text>
      </TouchableOpacity>
      <DeviceModal
        closeModal={hideModal}
        visible={isModalVisible}
        connectToPeripheral={connectToDevice}
        devices={allDevices}
      />
    </SafeAreaView >
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "#f2f2f2",
  },
  heartRateTitleWrapper: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  heartRateTitleText: {
    fontSize: 30,
    fontWeight: "bold",
    textAlign: "center",
    marginHorizontal: 20,
    color: "black",
  },
  heartRateText: {
    fontSize: 25,
    marginTop: 15,
  },
  ctaButton: {
    backgroundColor: "#FF6060",
    justifyContent: "center",
    alignItems: "center",
    height: 50,
    marginHorizontal: 20,
    marginBottom: 5,
    borderRadius: 8,
  },
  ctaButtonText: {
    fontSize: 18,
    fontWeight: "bold",
    color: "white",
  },
});

export default App;
