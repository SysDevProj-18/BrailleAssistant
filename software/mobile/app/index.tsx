import { Link, Stack } from 'expo-router';
import * as React from 'react';
import { Pressable, View } from 'react-native';
import { FlatList } from 'react-native-reanimated/lib/typescript/Animated';
import { Button } from '~/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '~/components/ui/card';
import { Text } from '~/components/ui/text';
import { H1, H3 } from '~/components/ui/typography';


export default function Screen() {
  return (
    <View className='flex-1 gap-5 p-6'>
      <Stack.Screen
        options={{
          headerTitle: 'Home',
          title: 'index'
        }}
      />
      <H3>Welcome back</H3>
      <View className='flex gap-5'>
        <View className='flex flex-row gap-5'>

          <Link className='flex-1' href='/camera' asChild>
            <Pressable>
              <Card className=''
              >
                <CardHeader>
                  <CardTitle>Scan document</CardTitle>
                </CardHeader>
                <CardContent>
                  <Text>and add it to the BrailleEd display</Text>
                </CardContent>
              </Card>
            </Pressable>

          </Link>
          <Card className='flex-1'>
            <CardHeader>
              <CardTitle>Card Title</CardTitle>
            </CardHeader>
            <CardContent>
              <Text>Card Content</Text>
            </CardContent>
          </Card>
        </View>
        <View className='flex flex-row gap-5'>
          <Card className='flex-1'>
            <CardHeader>
              <CardTitle>Card Title</CardTitle>
            </CardHeader>
            <CardContent>
              <Text>Card Content</Text>
            </CardContent>
          </Card>
          <Card className='flex-1'>
            <CardHeader>
              <CardTitle>Card Title</CardTitle>
            </CardHeader>
            <CardContent>
              <Text>Card Content</Text>
            </CardContent>
          </Card>
        </View>
      </View>

    </View >
  );
}
