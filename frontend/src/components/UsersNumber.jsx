import React, { useEffect, useState } from "react";
import { Image } from "antd";
import { useFetching } from "../hooks/useFetching";
import UserService from "../services/UserService";

const UsersNumber = ({ className }) => {
  const [totalUsers, setTotalUsers] = useState(0);
  const [fetchTotalUsers, isLoading, error] = useFetching(async () => {
    const response = await UserService.get_total_users();
    setTotalUsers(response.data);
  });

  useEffect(() => {
    fetchTotalUsers();
  }, []);
  return (
    <div
      className={`${className} flex flex-row align-middle justify-around items-center`}
    >
      <p className={"mr-3"}>{totalUsers}</p>
      <Image src={"/people.svg"} preview={false} width={37} />
      <p className={"ml-5"}>КОЛ-ВО ЛЮДЕЙ НА ПЛАТФОРМЕ КУ.ПОМОГУ</p>
    </div>
  );
};

export default UsersNumber;
