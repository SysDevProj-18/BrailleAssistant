import { CameraCapturedPicture } from 'expo-camera';
import { CameraView, useCameraPermissions } from 'expo-camera/next';
import { Stack, useRouter } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Button } from '~/components/ui/button';
import MlkitOcr, { MlkitOcrResult } from 'react-native-mlkit-ocr';
import MLKit from 'react-native-mlkit-ocr';
const upload = async (url: string, text: string) => {
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    body: JSON.stringify({ text: text }),
  });
  const responseJson = await response.json();
  return responseJson;
}

export default function Page() {
  const [facing, setFacing] = useState('back');
  const [permission, requestPermission] = useCameraPermissions();
  const [picture, setPicture] = useState<CameraCapturedPicture | null>(null);
  const camera = useRef<CameraView>(null);
  const router = useRouter()

  useEffect(() => {
    if (picture) {
      const call = async () => {
        const result = await MlkitOcr.detectFromUri(picture.uri)
        return result
      }


      call().then((res) => {
        let text = ''
        res.forEach((block) => {
          text += block.text + '\n'
        })
        fetch('http://192.168.175.66:5001/send', {
          // fetch('http://192.168.175.245:5001/send', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text: text }),
        })
          .then((response) => response.json())
          .then((responseJson) => {
            router.dismiss(1)
          })
          .catch((error) => {
            console.error(error);
          });
      })
    }
  }, [picture]);

  return (
    <View className='flex-1 h-full'>
      <Stack.Screen
        options={{
          headerTitle: 'Home',
          title: 'index'
        }}
      />
      <View className='h-full'>
        <CameraView ref={camera} facing="back" className='h-full'>
          <View className='h-full flex flex-col justify-end'>
            <TouchableOpacity
            >
              <Button className='bg-red-100'
                onPress={() => {
                  console.log('Taking picture...');
                  camera.current?.takePictureAsync({
                    base64: true,
                  }).then((result) => {
                    setPicture(result!);
                  });
                }}
              >
                <Text>
                  Take Picture
                </Text>
              </Button>
            </TouchableOpacity>
          </View>
        </CameraView>
      </View>

    </View >
  );
}
