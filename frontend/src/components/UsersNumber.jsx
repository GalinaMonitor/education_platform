import React from "react";
import { Image } from "antd";

const UsersNumber = ({ className }) => {
  return (
    <div
      className={`${className} flex flex-row align-middle justify-around items-center`}
    >
      <p className={"mr-3"}>1920</p>
      <Image src={"/people.svg"} preview={false} width={37} />
      <p className={"ml-5"}>КОЛ-ВО ЛЮДЕЙ НА ПЛАТФОРМЕ КУ.ПОМОГУ</p>
    </div>
  );
};

export default UsersNumber;
