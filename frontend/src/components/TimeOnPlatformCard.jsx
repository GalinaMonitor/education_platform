import React from "react";
import Card from "./UI/Card";
import TextBlock from "./UI/TextBlock";

const TimeOnPlatformCard = ({ className }) => {
  return (
    <Card className={className}>
      <TextBlock
        className={"mr-10"}
        smallText={"ВРЕМЯ НА ПЛАТФОРМЕ"}
        bigText={"0 часов 0 минут"}
      />
    </Card>
  );
};

export default TimeOnPlatformCard;
