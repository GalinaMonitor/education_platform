import React from "react";
import Card from "./UI/Card";
import TextBlock from "./UI/TextBlock";
import useUserStore from "../store/useUserStore";

const TimeOnPlatformCard = ({ className }) => {
  const { timeOnPlatform } = useUserStore();

  const hours = Math.floor(timeOnPlatform / 60);
  const minutes = Math.floor(timeOnPlatform % 60);

  return (
    <Card className={className}>
      <TextBlock
        className={"mr-10"}
        smallText={"ВРЕМЯ НА ПЛАТФОРМЕ"}
        bigText={`${hours} часов ${minutes} минут`}
      />
    </Card>
  );
};

export default TimeOnPlatformCard;
