import React from 'react';
import TextMessage from "./messages/TextMessage";
import VideoMessage from "./messages/VideoMessage";

const Message = ({text, type, time, className}) => {
    let message;
    switch (type) {
        case 0:
            message = <TextMessage text={text} time={time}/>
            break;
        case 1:
            message = <VideoMessage video_id={text} time={time}/>
            break;
        default:
            message = <TextMessage text={text} time={time}/>
            break;
    }
    return message
};

export default Message;