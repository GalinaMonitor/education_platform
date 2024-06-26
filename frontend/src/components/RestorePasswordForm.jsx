import React, { useState } from "react";
import { Button, Form, Input } from "antd";
import { rules } from "../utils/rules";
import useUserStore from "../store/useUserStore";
import { Link, useNavigate } from "react-router-dom";
import { RouteNames } from "../router";

const RestorePasswordForm = ({ email, uuid }) => {
  const { isLoading, error, restorePassword } = useUserStore();
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const submit = () => {
    restorePassword(email, password, uuid);
    navigate(RouteNames.LOGIN);
  };

  return (
    <div style={{ width: 460 }}>
      <Form onFinish={submit} layout="vertical">
        <Form.Item
          label={<p className={"title-s font-semibold"}>ПАРОЛЬ</p>}
          name="password"
          rules={[rules.required("Введите пароль")]}
        >
          <Input.Password
            className={"big-button"}
            style={{ width: "100%" }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Item>
        <Form.Item className={"mb-2 mt-5"}>
          <Button
            className={"big-button"}
            style={{ width: "100%" }}
            type={"primary"}
            htmlType="submit"
            loading={isLoading}
          >
            <p className={"font-semibold"}>ВОССТАНОВИТЬ</p>
          </Button>
        </Form.Item>
      </Form>
      <Link to="/login">
        <Button
          className={"big-button"}
          style={{ width: "100%" }}
          type={"default"}
          htmlType="submit"
          loading={isLoading}
        >
          <p className={"font-semibold"}>ВОЙТИ</p>
        </Button>
      </Link>
    </div>
  );
};

export default RestorePasswordForm;
