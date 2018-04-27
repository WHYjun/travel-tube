import React from 'react'
import VideoListItem from './VideoListItem'
import _ from 'lodash'
import { List } from 'semantic-ui-react'

const VideoList = (props) => {

  const onVideoSelect = (video) => {
    console.log('video clicked')
    window.open(`https://www.youtube.com/watch?v=${video.video_id}`, '_blank')
  }


  const videoItems = _.map(props.videos, (video) => {
    // we pass key prop to list so that react can quickly grab individual items to update
    // instead of updating the entire list
    return (
      <VideoListItem
        onVideoSelect={onVideoSelect}
        video={video}
        key={video.video_id}
      />
    )
  })

  return (
    <List items={videoItems}/>
  );
}

export default VideoList;
