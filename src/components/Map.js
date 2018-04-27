import React from 'react'
import { compose, withProps } from "recompose"
import { withScriptjs, withGoogleMap, GoogleMap, Marker } from "react-google-maps"

// render google map using react-google-maps
const Map = compose(
  withProps({
    googleMapURL: "https://maps.googleapis.com/maps/api/js?key=AIzaSyB_61nxewfNdBvUiTl1cT6gYcg4qehhSOQ&v=3.exp&libraries=geometry,drawing,places",
    loadingElement: <div style={{ height: `100%` }} />,
    containerElement: <div style={{ height: `500px` }} />,
    mapElement: <div style={{ height: `100%`, width: '50%' }} />,
  }),
  withScriptjs,
  withGoogleMap
)((props) =>
  <GoogleMap
    defaultZoom={8}
    defaultCenter={props.coords}
    onClick={props.onMapClick}
  >
    <Marker
      position={props.coords}
      onClick={props.onMarkerClick}
    />
  </GoogleMap>
)

export default Map
