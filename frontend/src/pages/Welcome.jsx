import React from "react";
import { Layout, Row, Image } from "antd";
import UserInfoForm from "../components/UserInfoForm";

const Welcome = () => {
  return (
    <Layout className={"h-full bg-white flex flex-col justify-center"}>
      <Row justify="center" align="middle">
        <Image width={185} src={"/tolya-big.svg"} preview={false} />
      </Row>
      <Row justify="center">
        <p className={"text-xl my-10"}>Здравствуйте!</p>
      </Row>
      <Row justify="center">
        <p className={"text-md text-center"}>
          МЕНЯ ЗОВУТ АНАТОЛИЙ, Я КУРАТОР
          <br />
          ПЛАТФОРМЫ КУ-ПОМОГУ
        </p>
      </Row>
      <Row justify="center" align="middle" className={"mt-10"}>
        <UserInfoForm />
      </Row>
    </Layout>
  );
};

export default Welcome;
