import React, { useEffect } from "react";
import { Button } from "antd";
import useUserStore from "../store/useUserStore";
import { Link } from "react-router-dom";

const ActivateUserForm = ({ email, uuid }) => {
  const { isLoading, error, activateUser } = useUserStore();

  useEffect(() => {
    activateUser(email, uuid);
  }, []);

  return (
    <div style={{ width: 460 }}>
      <p className={"text-lg text-center my-5"}>
        Ваша учетная запись активирована
      </p>
      <Link to="/login">
        <Button
          className={"big-button"}
          style={{ width: "100%" }}
          type={"primary"}
          htmlType="submit"
          loading={isLoading}
        >
          <p className={"font-semibold"}>ВОЙТИ</p>
        </Button>
      </Link>
    </div>
  );
};

export default ActivateUserForm;
