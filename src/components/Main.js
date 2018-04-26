import React, { Component } from 'react'
import MapContainer from './MapContainer'
import VideoList from './VideoList'
import EventList from './EventList'
import { Segment } from 'semantic-ui-react'
import axios from 'axios'

class Main extends Component {

  constructor(props) {
    super(props)
    this.state = {
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

  render() {
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
  }
}

export default Main
