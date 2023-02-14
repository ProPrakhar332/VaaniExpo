import React, { useState, useRef } from "react";
import {
  StyleSheet,
  Text,
  View,
  TouchableOpacity,
  SafeAreaView,
  TextInput,
  KeyboardAvoidingView,
} from "react-native";
import { Camera } from "expo-camera";
import Icons from "react-native-vector-icons";
import FAIcons from "react-native-vector-icons/FontAwesome5";

//import * as handpose from "handpose";

function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.front);
  const cameraRef = useRef(null);
  const [showText, setshowText] = useState("");
  const [getStarted, setgetStarted] = useState(false);

  React.useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  // const predictGesture = async () => {
  //   const predictions = await handpose.estimateHands(
  //     cameraRef.current.videoElement
  //   );
  //   if (predictions.length > 0) {
  //     const hand = predictions[0].landmarks;
  //     // Convert hand landmarks to text here
  //   }
  // };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={styles.container}
      enabled={true}
    >
      <SafeAreaView style={{ flex: 1, marginTop: 30 }}>
        {getStarted ? (
          <View style={{ flex: 1 }}>
            <Camera
              style={{ flex: 0.7, margin: 10 }}
              type={type}
              ref={cameraRef}
            >
              <View
                style={{
                  flex: 1,
                  backgroundColor: "transparent",
                  flexDirection: "row",
                }}
              >
                <TouchableOpacity
                  style={{
                    flex: 1,
                    alignSelf: "flex-end",
                    alignItems: "center",
                  }}
                  onPress={() => {
                    setType(
                      type === Camera.Constants.Type.back
                        ? Camera.Constants.Type.front
                        : Camera.Constants.Type.back
                    );
                  }}
                >
                  <Text
                    style={{
                      fontSize: 18,
                      color: "white",
                      alignSelf: "center",
                      backgroundColor: "gray",
                      padding: 10,
                      borderRadius: 10,
                      marginBottom: 10,
                    }}
                  >
                    {" "}
                    Flip Camera{" "}
                  </Text>
                </TouchableOpacity>
              </View>
            </Camera>
            <View style={{ flex: 0.3 }}>
              <TouchableOpacity
                onPress={() => {
                  setshowText(
                    showText == ""
                      ? "Hn bhai aa gye apni maut ka circus dekhne"
                      : ""
                  );
                }}
                style={{
                  marginVertical: 10,
                  alignSelf: "center",
                }}
              >
                <Text style={{ fontWeight: "bold", fontSize: 15 }}>
                  Predict Gesture
                </Text>
              </TouchableOpacity>
              <View
                style={{
                  flexDirection: "row",
                  borderWidth: 1,
                  borderRadius: 10,
                  borderColor: "black",
                  width: "95%",
                  padding: 10,
                  alignSelf: "center",
                  justifyContent: "space-between",
                }}
              >
                <TextInput
                  style={{
                    flex: 1,
                    alignSelf: "center",
                  }}
                  multiline={true}
                  onChangeText={(text) => setshowText(text)}
                  value={showText}
                ></TextInput>
                <FAIcons
                  name="copy"
                  size={20}
                  style={{
                    alignSelf: "center",
                  }}
                  //onPress={()=>}
                />
              </View>
            </View>
          </View>
        ) : (
          <View style={{ flex: 1, flexDirection: "row", alignSelf: "center" }}>
            <TouchableOpacity
              style={{
                width: 100,
                alignSelf: "center",
                justifyContent: "center",
                backgroundColor: "limegreen",
                flexDirection: "row",
                padding: 10,
                borderRadius: 10,
              }}
              onPress={() => setgetStarted(true)}
            >
              <Text style={{ color: "white", fontWeight: "bold" }}>
                Get Started
              </Text>
            </TouchableOpacity>
          </View>
        )}
      </SafeAreaView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "white",
  },
});

export default App;
