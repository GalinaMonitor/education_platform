import React from "react";
import { Image, Layout } from "antd";

const MobileBlock = () => {
  return (
    <Layout
      className={
        "h-full flex flex-col flex-wrap items-center justify-center p-5 pt-10"
      }
    >
      <p className={"title-s text-center pb-5 brand-color"}>
        Мы осознанно отказались <br />
        от мобильной версии
      </p>
      <p className={"text-center pb-5"}>
        Мы хотим, чтобы вы сразу приступили к повторению за действиями
        наставника и быстро интегрировали услышанное и увиденное в работу.
      </p>
      <Image src={"/mobile-block.svg"} preview={false} width={300} />
    </Layout>
  );
};

export default MobileBlock;
