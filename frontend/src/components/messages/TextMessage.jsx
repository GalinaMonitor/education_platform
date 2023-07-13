import React from "react";
import { formatDatetime } from "../../utils/utils";

const TextMessage = ({ text, time = null }) => {
  const parsedText = <p dangerouslySetInnerHTML={{ __html: text }} />;
  return (
    <div
      className={`border-solid border-2 border-orange-500 rounded-2xl relative p-6 m-10`}
    >
      <div className={"top-0 left-0 text-left"}>{parsedText}</div>
      {time ? (
        <div className={"absolute bottom-0 right-2 text-right"}>
          <p>{formatDatetime(time)}</p>
        </div>
      ) : (
        <></>
      )}
    </div>
  );
};

export default TextMessage;
