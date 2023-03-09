import React, { useState, useRef, useEffect } from "react";
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
import * as tf from "@tensorflow/tfjs";
//import "@tensorflow/tfjs-react-native";

import logo from "./assets/Logo3.jpg";

function App() {
  const [hasPermission, setHasPermission] = useState(null);
  const [type, setType] = useState(Camera.Constants.Type.front);
  const cameraRef = useRef(null);
  const [showText, setshowText] = useState("");
  const [getStarted, setgetStarted] = useState(false);
  const modelJson = require("./model/model_new.json");
  const modelWeights = require("./model/model_new.h5");

  const layout = useWindowDimensions();

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === "granted");
    })();
  }, []);

  useEffect(() => {
    const bundleResourceIOExample = async () => {
      console.log("Inside loading model");

      await tf
        .ready()
        .then(() => {
          console.log("Loaded successfully");
        })
        .catch((error) => {
          console.log(error);
        });

      const model = await tf.loadLayersModel(
        tf.io.browserFiles([modelJson, modelWeights])
      );

      // console.log(modelJson);
      // console.log(modelWeights);

      // const model = await tf.loadLayersModel(
      //   bundleResourceIO(modelJson, modelWeights)
      // );
      // const res = model.predict(tf.randomNormal([1, 28, 28, 1]));
      // console.log(res);
    };
    bundleResourceIOExample();
  }, []);

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

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
              <View style={{ alignSelf: "center", marginVertical: 20 }}>
                <Text
                  style={{
                    fontWeight: "bold",
                    marginVertical: 10,
                    textDecorationStyle: "double",
                    textDecorationColor: "black",
                    textDecorationLine: "underline",
                    fontSize: 18,
                  }}
                >
                  Translation
                </Text>
                <Text>Hello brother</Text>
              </View>
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
