import React from "react";
import Navbar from "../Navbar";
import { Row } from "antd";
import Notifications from "../Notifications";

const BaseLayout = ({ children }) => {
  return (
    <div className={"h-full"}>
      <div className={"h-1/6 pt-5"}>
        <Navbar className={"ml-5 mr-5"} />
      </div>
      <div className={"h-4/6 pt-5"}>
        <Row className={"ml-5 mr-5 h-full"}>{children}</Row>
      </div>
      <div className={"h-1/6 pt-5"}>
        <Notifications className={"ml-5 mr-5"} />
      </div>
    </div>
  );
};

export default BaseLayout;
