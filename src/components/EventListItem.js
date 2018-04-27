import React from 'react'
import { Segment, Header, Image } from "semantic-ui-react"

const EventListItem = (props) => {
  // grab video
  const { event, onEventSelect } = props
  const imageUrl = event.image_url


  return (
    <li onClick={() => onEventSelect(event)}>
    <Segment.Group raised>
      <Header as='h5'> {event.name} </Header>
      <Image src={imageUrl} size="mini" circular/>
      <p> {event.start} - {event.end} </p>
      <Header> {event.description} </Header>
    </Segment.Group>
    </li>
  )

  /*
  return (
    <li onClick={() => onEventSelect(event)} className="list-group-item">
      <div className="video-list media">
        <div className="media-left">
          <img className="media-object" src={imageUrl} alt={"event_thumbnail"}/>
        </div>

        <div className="media-body">
          <div className="media-heading">
            {event.title}
          </div>
        </div>
      </div>

    </li>
  )
  */
}

export default EventListItem
