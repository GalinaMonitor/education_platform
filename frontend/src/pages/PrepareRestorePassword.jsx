import React from "react";
import { Image, Layout, Row } from "antd";
import { Link } from "react-router-dom";
import PrepareRestorePasswordForm from "../components/PrepareRestorePasswordForm";

const PrepareRestorePassword = () => {
  return (
    <Layout className={"h-full bg-white flex flex-col justify-center"}>
      <Row justify="center" align="middle">
        <Image width={382} src={"/ku-logo.svg"} preview={false} />
      </Row>
      <Row justify="center" align="middle" className={"mt-32"}>
        <PrepareRestorePasswordForm />
      </Row>
      <div
        className={
          "bottom-5 absolute m-auto right-0 left-0 w-2/6 h-5 text-center"
        }
      >
        <Link to={"mailto:support@ku-pomogu.ru"}>
          СВЯЗАТЬСЯ С ТЕХНИЧЕСКОЙ ПОДДЕРЖКОЙ
        </Link>
      </div>
    </Layout>
  );
};

export default PrepareRestorePassword;
