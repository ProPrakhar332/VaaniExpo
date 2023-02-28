import React, { useState, useRef } from "react";
import {
  Alert,
  StyleSheet,
  Text,
  View,
  useWindowDimensions,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  TextInput,
  KeyboardAvoidingView,
  Image,
} from "react-native";
import { Camera } from "expo-camera";
import Icons from "react-native-vector-icons";
import FAIcons from "react-native-vector-icons/FontAwesome5";
import MCIcons from "react-native-vector-icons/MaterialCommunityIcons";
import * as Clipboard from "expo-clipboard";
//import TFLite from "react-native-tensorflow-lite";

import logo from "./assets/Logo3.jpg";

//import * as handpose from "handpose";

function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.front);
  const cameraRef = useRef(null);
  const [showText, setshowText] = useState("");
  const [getStarted, setgetStarted] = useState(false);

  const layout = useWindowDimensions();

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

  const copyToClipboard = async () => {
    Alert.alert("Copied", `The copied text is :- \n${showText}`);
    await Clipboard.setStringAsync(showText);
  };

  const fetchCopiedText = async () => {
    const text = await Clipboard.getStringAsync();
    setshowText(text);
  };

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === "ios" ? "padding" : "height"}
      style={styles.container}
      enabled={true}
    >
      <SafeAreaView
        style={{
          backgroundColor: "#2B8ADA",
          width: "100%",
        }}
      >
        <ScrollView
          style={{
            width: "100%",
            alignSelf: "center",
            backgroundColor: "#e8f0fe",
            marginTop: 20,
          }}
          showsVerticalScrollIndicator={false}
          nestedScrollEnabled={true}
        >
          <Image
            source={logo}
            style={{
              width: 320,
              height: 80,
              alignSelf: "center",
              padding: 0,
            }}
          />
          {getStarted ? (
            <View style={{ flex: 1 }}>
              <Camera
                style={{ flex: 1, height: (layout.height * 3) / 5 }}
                type={type}
                ref={cameraRef}
              >
                <View
                  style={{
                    flex: 1,
                    backgroundColor: "transparent",
                    flexDirection: "row",
                    justifyContent: "center",
                  }}
                >
                  <TouchableOpacity
                    style={{
                      alignSelf: "flex-end",
                      alignItems: "center",
                      backgroundColor: "gray",
                      padding: 10,
                      borderRadius: 80,
                      marginBottom: 10,
                      marginRight: 10,
                    }}
                    onPress={() => {
                      setType(
                        type === Camera.Constants.Type.back
                          ? Camera.Constants.Type.front
                          : Camera.Constants.Type.back
                      );
                    }}
                  >
                    <MCIcons
                      name="camera-flip"
                      size={25}
                      color={"white"}
                      style={{}}
                    />
                  </TouchableOpacity>
                  <TouchableOpacity
                    style={{
                      alignSelf: "flex-end",
                      alignItems: "center",
                      backgroundColor: "red",
                      padding: 10,
                      borderRadius: 80,
                      marginBottom: 10,
                    }}
                    onPress={() => {
                      setgetStarted(false);
                    }}
                  >
                    <MCIcons
                      name="close"
                      size={25}
                      color={"white"}
                      style={{ alignSelf: "center" }}
                    />
                  </TouchableOpacity>
                </View>
              </Camera>
            </View>
          ) : (
            <View style={{ flexDirection: "column" }}>
              <View
                style={{
                  flex: 1,
                  flexWrap: "wrap",
                  width: "90%",
                  alignSelf: "center",
                  marginVertical: 15,
                  backgroundColor: "white",
                  borderRadius: 10,
                  padding: 20,
                }}
              >
                <Text style={{ alignSelf: "center", fontSize: 18 }}>
                  " Talk to a man in a language he understands, that goes to his
                  head. Talk to him in his own language, that goes to his heart.
                  " The name “Vaani” refers to the Indian Goddess of Speech,
                  Goddess Saraswati.{" "}
                </Text>

                <Text
                  style={{ alignSelf: "center", fontSize: 18, marginTop: 10 }}
                >
                  Vaani is a real time sign language interpreter that is used to
                  bridge the gap between the vocally muted and the rest of the
                  world. With the help of Vaani we become their voice. It is a
                  deep learning based model embedded in a web application which
                  takes live webcam feed as input and outputs the performed sign
                  language as text on the screen. It uses a CNN LSTM based deep
                  learning model architecture to detect the action performed in
                  each frame and after the action is completely performed, the
                  value associated with it is displayed.
                </Text>
              </View>

              <TouchableOpacity
                onPress={() => setgetStarted(true)}
                style={{
                  marginVertical: 10,
                  padding: 10,
                  paddingHorizontal: 20,
                  backgroundColor: "limegreen",
                  borderRadius: 10,
                  justifyContent: "center",
                  alignSelf: "center",
                }}
              >
                <Text style={{ color: "white" }}>Get Started</Text>
              </TouchableOpacity>
            </View>
          )}
        </ScrollView>
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
    backgroundColor: "#e8f0fe",
  },
});

export default App;
