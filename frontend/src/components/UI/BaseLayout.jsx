import React from "react";
import Card from "./Card";
import Navbar from "../Navbar";
import { Row } from "antd";

const BaseLayout = ({ children }) => {
  return (
    <div className={"h-full"}>
      <div className={"ml-16 mt-16 mr-16"}>
        <Navbar className={"h-1/6"} />
      </div>
      <Row className={"ml-16 mr-16 h-4/6 mt-5"}>{children}</Row>
    </div>
  );
};

export default BaseLayout;
