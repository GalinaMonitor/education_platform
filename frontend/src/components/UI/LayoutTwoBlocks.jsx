import React from "react";
import { Col } from "antd";
import BaseLayout from "./BaseLayout";

const LayoutTwoBlocks = ({ children }) => {
  return (
    <BaseLayout>
      <Col span={6} className={"h-full"}>
        <div className={"h-full mr-5"}>{children[0]}</div>
      </Col>
      <Col span={18} className={"h-full"}>
        <div className={"h-full"}>{children[1]}</div>
      </Col>
    </BaseLayout>
  );
};

export default LayoutTwoBlocks;
