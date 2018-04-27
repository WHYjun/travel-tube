import React from 'react'
import EventListItem from './EventListItem'
import _ from 'lodash'
import { List } from 'semantic-ui-react'

const EventList = (props) => {

  console.log(props.events)

  const onEventSelect = (event) => {
    console.log('event clicked')
    window.open(event.url, '_blank')
  }


  const eventItems = _.map(props.events, (event) => {
    // we pass key prop to list so that react can quickly grab individual items to update
    // instead of updating the entire list
    return (
      <EventListItem
        onEventSelect={onEventSelect}
        event={event}
        key={event.id}
      />
    )
  })

  return (
    <List items={eventItems} />
  );
}

export default EventList;
