import React from "react";
import { formatDatetime } from "../../utils/utils";

const TextMessage = ({ text, time = null }) => {
  const parsedText = <p dangerouslySetInnerHTML={{ __html: text }} />;
  return (
    <div
      className={`border-2 border-solid rounded-2xl relative p-6 m-10`}
      style={{ borderColor: "#ff7d1f" }}
    >
      <div className={"top-0 left-0 text-left title-md whitespace-pre-line"}>
        {parsedText}
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

export default TextMessage;
