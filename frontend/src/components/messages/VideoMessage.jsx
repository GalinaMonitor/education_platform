import React from "react";
import { formatDatetime } from "../../utils/utils";

const VideoMessage = ({ videoId, time = null }) => {
  const playerCode = `<iframe class="rounded-xl" style="display:block; width:100%; height: 100%" src="${videoId}" allow="autoplay; fullscreen; picture-in-picture; encrypted-media;" frameborder="0" allowfullscreen></iframe>`;
  const video = (
    <div className={"h-96"} dangerouslySetInnerHTML={{ __html: playerCode }} />
  );
  return (
    <div
      className={`bg-black border-solid border-2 border-orange-500 rounded-2xl relative m-10`}
    >
      <div className={"top-0 left-0 text-left"}>{video}</div>
      {time ? (
        <div className={"absolute bottom-0 right-2 text-right text-gray-50"}>
          <p>{formatDatetime(time)}</p>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
};

export default VideoMessage;
