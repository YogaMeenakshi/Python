import * as React from 'react';
import { ImageBackground, Button, View, Text, StyleSheet, ScrollView } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { ListItem, Icon } from 'react-native-elements'
import Swiper from 'react-native-swiper'


const styles = StyleSheet.create({
  wrapper:{},
  text: {
    color: 'black',
    fontSize: 60,
    fontWeight: 'bold'
  },
  imgBackground: {
    width: '100%',
    height: '100%',
    flex: 1,
    opacity: 0.9
  },
  container: {
    flex: 1,
  },
  btn: {
    justifyContent: 'center',
    position: 'absolute',
    bottom: 80
  }
})


function HomeScreen({ navigation }) {
  return (
    <View style={styles.container}>
      <ImageBackground style={styles.imgBackground}
        resizeMode='cover'
        source={require('./assets/cover.png')}
        blurRadius={20}>
        <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
          <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center', top: -100 }}>
            <Text style={styles.text} >Bagavat Gita</Text>
          </View>
          <View style={styles.btn}>
            <Button
              title="Start reading"
              onPress={() => navigation.navigate('Contents')}
            />
          </View>
        </View>
      </ImageBackground>
    </View>
  );
}

function DetailsScreen({ navigation }) {
  const list = [
    {
      title: 'Chapter 1 - Arjuna Visada Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 2 - Sankhya Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 3 - Karma Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 4 - Jnana Karma Sanyasa Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 5 - Karma Sanyasa Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 6 - Dhyana Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 7 - Gyaan Vigyana Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 8 - Akshara Brahma Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 9 - Raja Vidya Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 10 - Vibhooti Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 11 - Vishwaroopa Darshana Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 12 - Bhakti Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 13 - Ksetra Ksetrajna Vibhaaga Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 14 - Gunatraya Vibhaga Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 15 - Purushottama Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 16 - Daivasura Sampad Vibhaga Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 17 - Sraddhatraya Vibhaga Yoga',
      icon: 'festival'
    },
    {
      title: 'Chapter 18 - Moksha Sanyaas Yoga',
      icon: 'festival'
    },
  ]
  return (
    <View>
      <ScrollView>
        {
          list.map((item, i) => (
            <ListItem key={i} bottomDivider onPress={() => navigation.navigate({ name: 'Chapters', params: { chapter_no: i + 1 }})}>
              <Icon name={item.icon} />
              <ListItem.Content>
                <ListItem.Title >{item.title}</ListItem.Title>
              </ListItem.Content>
              {/* <ListItem.Chevron /> */}
            </ListItem>
          ))
        }
      </ScrollView>
    </View>


  );
}


function ChaptersScreen({ navigation, route }) {
  const name = './assets/chapters.json'
  const Data = require(name)

  return (
    <View>
      <Text style={{ height: "8%", width: "100%", color: 'black', fontSize: 40, fontWeight: 'bold', paddingTop: 5 }}>
        {"Chapter " + route.params.chapter_no}
      </Text>
      <ScrollView>
        {
          Data.map((item, i) => (
            item.chapter_no == route.params.chapter_no
              ? (
                <ListItem key={i} bottomDivider onPress={() => navigation.navigate({ name:'Explanation', params: { chapter_no: item.chapter_no, verse_no : item.sutra_no}})}>
                  {/* <Icon name='festival'/> */}
                  <ListItem.Content>
                    <ListItem.Subtitle style={{ fontWeight: 'bold' }}>Verse {item.sutra_no}</ListItem.Subtitle>
                    <ListItem.Title style={{ paddingTop: 10 }}>{item.sutra}</ListItem.Title>
                  </ListItem.Content>
                  {/* <ListItem.Chevron /> */}
                </ListItem>
              ) : null
          ))
        }
      </ScrollView>
    </View>
  );
}

function ExplanationScreen({ navigation, route }) {
  const name = './assets/chapters.json'
  const data = require(name)
  const item_ = data.find(item => item.sutra_no === route.params.verse_no && item.chapter_no === route.params.chapter_no)

  return (
    <Swiper style={styles.wrapper} showsButtons={false} >
    <View>

      <View style = {{height: "45%", width: "100%"}}>
      <Text style={{ color: 'black', fontSize: 15, fontWeight: 'bold', paddingTop: 5, marginLeft: 10}}>
        {"Verse " + route.params.verse_no + "\n"}
      </Text>
      <Text style={{ color: 'black', fontSize: 17, paddingTop: 0 , flex: 1, flexWrap: 'wrap', marginLeft: 10}}>
        { item_.sutra }
      </Text>
      </View>
      
      <ScrollView>
      
        {
          data.map((item, i) => (
            item.chapter_no == route.params.chapter_no & item.sutra_no == route.params.verse_no
              ? (
                <ListItem key={i} bottomDivider>
                  <ListItem.Content>
                    <ListItem.Subtitle style={{ fontWeight: 'bold' }}>Explanation</ListItem.Subtitle>
                    <ListItem.Title style={{ paddingTop: 10 }}>{item.sutra}</ListItem.Title>
                  </ListItem.Content>
                </ListItem>
              ) : null
          ))
        }
        
      </ScrollView>
      
    </View>
    </Swiper>
  );
}

const Stack = createNativeStackNavigator();

function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} />
        <Stack.Screen name="Contents" component={DetailsScreen} />
        <Stack.Screen name="Chapters" component={ChaptersScreen} />
        <Stack.Screen name="Explanation" component={ExplanationScreen} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


export default App;
