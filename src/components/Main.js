import React, { Component } from 'react'
import MapContainer from './MapContainer'
import VideoList from './VideoList'
import EventList from './EventList'
import Login from './Login'
import { Segment, Header, Container, Button } from 'semantic-ui-react'
import axios from 'axios'
import { Route } from 'react-router'

class Main extends Component {

  constructor(props) {
    super(props)
    this.state = {
      username: 'test',
      coords: {
        lat: 42.350214,
        lng: -71.126877,
      },
      city: '',
      videos: [],
      events: [],
    }
  }

  async componentDidMount() {
    try {
      // get data from heroku backend
      let response = await axios.post('https://quiet-gorge-15205.herokuapp.com/fake_result')
      // extract data from http response
      const data = response.data
      // update state with data
      this.setState({
        city: data.city_name,
        videos: data.videos,
        events: data.events,
      })
    } catch(err) {
      console.log(err)
    }
  }

  // function to handle click on map
  onMapClick = (e) => {
    // get coordinates from map object and create object to update state with
    // mapClick returns an object with functions to get latitude longitude :)
    const coords = {
      lat: e.latLng.lat(),
      lng: e.latLng.lng()
    }
    // update state and consequentially marker
    this.setState({ coords })
  }

  // user pressed login button
  async loginPressed() {
    console.log('login pressed')
    window.open('http://127.0.0.1:5000/login')
    // this.setState({ username: 'test' })

  }

  // user pressed logout button
  logoutPressed = () => {
    // remove username from state
    this.setState({ username: null })
  }

  loginButton = () => {
    // if there is no token = fail case
    if (!this.state.username) {
      return (
        <Button onClick={() => this.loginPressed()}> Login with Twitter </Button>
      )
    }
    // if there is a token
    return (
      <Button onClick={() => this.logoutPressed()}> Logout </Button>
    )
  }

  showMap = () => {
    // if no token
    if (!this.state.username) {
      return <h3> Please login to use app </h3>
    }
    // if there is a token
    return (
      <div style={{ marginTop: 20 }}>
        <MapContainer
          coords={this.state.coords}
          onMapClick={this.onMapClick}
        />
        <EventList events={this.state.events}/>
        <VideoList videos={this.state.videos}/>
      </div>
    )
  }



  render() {
    return (
      <div style={{ textAlign:'center' }}>
        <Header style={{ textAlign:'center' }} as='h1'> TravelTube </Header>
        <div style={{ textAlign:'center' }}>
          {this.loginButton()}
          {this.showMap()}
        </div>
      </div>


    )
    /*
    return (
      <Segment.Group horizontal>
        <Segment>
        <MapContainer
          coords={this.state.coords}
          onMapClick={this.onMapClick}
        />
        </Segment>
        <Segment>
          <EventList events={this.state.events}/>
        </Segment>
        <Segment>
          <VideoList videos={this.state.videos}/>
        </Segment>
      </Segment.Group>
    );
    */
  }
}

export default Main
