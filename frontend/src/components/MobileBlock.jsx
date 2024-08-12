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
        Нужно активировать аккаунт через компьютер
      </p>
      <p className={"text-center pb-5"}>Мобильная версия сейчас недоступна</p>
      <Image src={"/mobile-block.svg"} preview={false} width={300} />
    </Layout>
  );
};

export default MobileBlock;
