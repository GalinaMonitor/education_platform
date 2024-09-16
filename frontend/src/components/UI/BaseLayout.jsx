import React from "react";
import Navbar from "../Navbar";
import { Row } from "antd";
import Notifications from "../Notifications";

const BaseLayout = ({ children }) => {
  return (
    <div className={"h-full"}>
      <div className={"h-1/6 pt-3"}>
        <Navbar className={"ml-3 mr-3"} />
      </div>
      <div className={"h-4/6 pt-3"}>
        <Row className={"ml-3 mr-3 h-full"}>{children}</Row>
      </div>
      <div className={"h-1/6 pt-3"}>
        <Notifications className={"ml-3 mr-3"} />
      </div>
    </div>
  );
};

export default BaseLayout;
