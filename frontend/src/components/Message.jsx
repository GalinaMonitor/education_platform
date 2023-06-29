import React from "react";
import TextMessage from "./messages/TextMessage";
import VideoMessage from "./messages/VideoMessage";

const Message = ({ text, type, time, className }) => {
  let message;
  switch (type) {
    case "TEXT":
      message = <TextMessage text={text} time={time} />;
      break;
    case "VIDEO":
      message = <VideoMessage videoId={text} time={time} />;
      break;
    default:
      message = <TextMessage text={text} time={time} />;
      break;
  }
  return message;
};

export default Message;
