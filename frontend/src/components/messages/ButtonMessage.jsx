import React from "react";
import { formatDatetime } from "../../utils/utils";
import { Button } from "antd";
import { Link } from "react-router-dom";

const ButtonMessage = ({ text, time = null, buttonText, buttonUrl }) => {
  const parsedText = <p dangerouslySetInnerHTML={{ __html: text }} />;
  return (
    <>
      <div
        className={`border-2 rounded-t-2xl rounded-b-md relative p-6 mx-10 mt-10 mb-0`}
        style={{ backgroundColor: "#ff7d1f" }}
      >
        <div className={"top-0 left-0 text-left text-white"}>{parsedText}</div>
        {time ? (
          <div className={"absolute bottom-0 right-2 text-right"}>
            <p className={"title-xs text-white"}>{formatDatetime(time)}</p>
          </div>
        ) : (
          <></>
        )}
      </div>

      <div className={`relative mx-10 mb-10 mt-0`}>
        <Link to={buttonUrl}>
          <Button
            className={
              "border-2 rounded-b-2xl rounded-t-md w-full medium-button"
            }
          >
            {buttonText}
          </Button>
        </Link>
      </div>
    </>
  );
};

export default ButtonMessage;
