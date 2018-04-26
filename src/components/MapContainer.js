import React, { Component } from 'react'
import Map from './Map'

class MapContainer extends Component {

  render() {
    return (
      <Map
        coords={this.props.coords}
        onMapClick={this.props.onMapClick}
      />
    );
  }
}

export default MapContainer;
