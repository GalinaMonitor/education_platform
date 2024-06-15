import React from "react";
import TextMessage from "./messages/TextMessage";
import VideoMessage from "./messages/VideoMessage";
import ButtonMessage from "./messages/ButtonMessage";
import ImageMessage from "./messages/ImageMessage";

const Message = ({ text, type, time, className }) => {
  let message;
  switch (type) {
    case "TEXT":
      message = <TextMessage text={text} time={time} />;
      break;
    case "IMAGE":
      message = <ImageMessage link={text} time={time} />;
      break;
    case "VIDEO":
      message = <VideoMessage videoId={text} time={time} />;
      break;
    case "BUTTON":
      const data = JSON.parse(text);
      message = (
        <ButtonMessage
          text={data.text}
          time={time}
          buttonText={data.buttonText}
          buttonUrl={data.buttonUrl}
        />
      );
      break;
    default:
      message = <TextMessage text={text} time={time} />;
      break;
  }
  return message;
};

export default Message;
