import React from "react";
import { formatDatetime } from "../../utils/utils";
import { Image } from "antd";

const ImageMessage = ({ link, time = null }) => {
  return (
    <div
      className={`bg-white border-solid border-2 rounded-2xl relative m-10`}
      style={{ borderColor: "#ff7d1f" }}
    >
      <div className={"top-0 left-0 text-left"}>
        <Image className={"rounded-xl"} src={link} />
      </div>
      {time ? (
        <div className={"absolute bottom-1 right-2 text-right"}>
          <p className={"title-xs"}>{formatDatetime(time)}</p>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
};

export default ImageMessage;
