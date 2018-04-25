import React, { Component } from 'react'
import Map from './Map'

class Main extends Component {

  constructor(props) {
    super(props)
    this.state = {
      coords: {
        lat: 42.350214,
        lng: -71.126877
      }
    }
  }

  // function to handle click on map
  mapClicked = (e) => {
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
      <Map
        coords={this.state.coords}
        onMapClick={this.mapClicked}
      />
    );
  }
}

export default Main;
