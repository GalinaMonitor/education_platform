import React from "react";

const Card = ({ children, className, text, style }) => {
  return (
    <div className={`${className} card`} style={style}>
      {text ? (
        <p className={"title-s mb-3 whitespace-nowrap"}>{text}</p>
      ) : (
        <></>
      )}
      {children}
    </div>
  );
};

export default Card;
