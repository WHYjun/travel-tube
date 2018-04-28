import React, { Component } from 'react'
import MapContainer from '../components/MapContainer'
import VideoList from '../components/VideoList'
import EventList from '../components/EventList'
import { Header, Button } from 'semantic-ui-react'
import axios from 'axios'

class Tour extends Component {

  constructor(props) {
    super(props)
    this.state = {
      coords: {
        lat: 42.34892444910906,
        lng: -71.10514202833048,
      },
      city: '',
      videos: [],
      events: [],
    }
  }

  async componentDidMount() {
    try {
      const { lat, lng } = this.state.coords
      // get data from heroku backend
      let response = await axios({method:'POST',url:'http://localhost:5000/search_result', data: { lat:lat, lng:lng }})
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

  async shouldComponentUpdate(){
    try {
      const { lat, lng } = this.state.coords
      // get data from heroku backend
      let response = await axios({method:'POST',url:'http://localhost:5000/search_result', data: { lat:lat, lng:lng }})
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
    console.log(coords)
    // update state and consequentially marker
    this.setState({ coords:coords })
  }

  // user pressed logout button
  logoutPressed = () => {
    // remove username from state
    window.open("http://localhost:5000/logout","_self");
  }

  logoutButton = () => {
    return (
      <Button onClick={() => this.logoutPressed()}> Logout </Button>
    )
  }

  showMap = () => {
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
          {this.logoutButton()}
          {this.showMap()}
        </div>
      </div>


    )
  }
}

export default Tour
