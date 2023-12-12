import React from "react";
import Card from "./UI/Card";
import { Image } from "antd";
import TextBlock from "./UI/TextBlock";
import { Link } from "react-router-dom";
import { RouteNames } from "../router";

const TolyaCard = ({ classname }) => {
  return (
    <Card className={classname}>
      <div className={"flex flex-row h-full"}>
        <TextBlock
          className={"mr-10"}
          smallText={"КУРАТОР"}
          bigText={"Робот Анатолий"}
        />
        <Link to={RouteNames.MAIN}>
          <Image width={111} src={"/tolya.svg"} preview={false} />
        </Link>
      </div>
    </Card>
  );
};

export default TolyaCard;
