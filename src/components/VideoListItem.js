import React from 'react';

const VideoListItem = (props) => {
  // grab video
  const { video, onVideoSelect } = props
  const imageUrl = video.image_url.url


  return (
    <li onClick={() => onVideoSelect(video)} className="list-group-item">
      <div className="video-list media">
        <div className="media-left">
          <img className="media-object" src={imageUrl} alt={"video_thumbnail"}/>
        </div>

        <div className="media-body">
          <div className="media-heading">
            {video.title}
          </div>
        </div>
      </div>

    </li>
  )
}

export default VideoListItem
