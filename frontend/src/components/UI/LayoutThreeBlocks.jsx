import React from "react";
import BaseLayout from "./BaseLayout";
import { Col } from "antd";

const LayoutThreeBlocks = ({ children }) => {
  return (
    <BaseLayout>
      <Col span={6} className={"h-full"}>
        <div className={"h-full mr-5"}>{children[0]}</div>
      </Col>
      <Col span={6} className={"h-full"}>
        <div className={"h-full mr-5"}>{children[1]}</div>
      </Col>
      <Col span={12} className={"h-full"}>
        <div className={"h-full"}>{children[2]}</div>
      </Col>
    </BaseLayout>
  );
};

export default LayoutThreeBlocks;
