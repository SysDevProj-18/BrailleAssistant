import { CameraCapturedPicture } from 'expo-camera';
import { CameraView, useCameraPermissions } from 'expo-camera/next';
import { Stack, useRouter } from 'expo-router';
import { useEffect, useRef, useState } from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { Button } from '~/components/ui/button';

const upload = async (url, base64) => {
  const form = new FormData();
  form.append('base64', base64);


  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    body: form
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
      // send post 
      const base64 = picture.base64;
      const formData = new FormData();
      formData.append('base64', base64!);

      upload('http://127.0.0.1:5000/process-documents', base64!).then((response) => {
        console.log(response);
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
