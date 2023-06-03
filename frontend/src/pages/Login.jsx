import React from "react";
import { Image, Layout, Row, theme } from "antd";
import LoginForm from "../components/LoginForm";

const Login = () => {
  return (
    <Layout className={"h-full bg-white flex flex-col justify-center"}>
      <Row justify="center" align="middle">
        <Image width={382} src={"/ku-logo.svg"} preview={false} />
      </Row>
      <Row justify="center" align="middle" className={"mt-32"}>
        <LoginForm />
      </Row>
    </Layout>
  );
};

export default Login;
