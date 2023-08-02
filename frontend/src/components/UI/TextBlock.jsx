import React from "react";

const TextBlock = ({ smallText, bigText, className }) => {
  return (
    <div className={`${className} my-3`}>
      <p className={"title-s my-1.5"}>{smallText}</p>
      <p className={"title-l m-0"}>{bigText}</p>
    </div>
  );
};

export default TextBlock;
