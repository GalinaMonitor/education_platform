import React, { useState } from "react";
import { Button, Form, Input, theme } from "antd";
import { rules } from "../utils/rules";
import useUserStore from "../store/useUserStore";
import { Link } from "react-router-dom";

const LoginForm = () => {
  const { isLoading, error, login } = useUserStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = () => {
    login(email, password);
  };

  return (
    <div className={"w-96"}>
      <Form onFinish={submit} layout="vertical">
        <Form.Item
          label={<p className={"text-md font-semibold"}>ВАША ПОЧТА</p>}
          name="email"
          rules={[rules.required("Введите email")]}
        >
          <Input
            className={"big-button"}
            style={{ width: "100%" }}
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </Form.Item>
        <Form.Item
          label={<p className={"text-md font-semibold"}>ПАРОЛЬ</p>}
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
        <Form.Item className={"mb-2"}>
          <Button
            className={"big-button"}
            style={{ width: "100%" }}
            type={"primary"}
            htmlType="submit"
            loading={isLoading}
          >
            <p className={"font-semibold"}>ВОЙТИ</p>
          </Button>
        </Form.Item>
      </Form>
      <Link to="/register">
        <Button
          className={"big-button"}
          style={{ width: "100%" }}
          type={"default"}
          htmlType="submit"
          loading={isLoading}
        >
          <p className={"font-semibold"}>ЗАРЕГИСТРИРОВАТЬСЯ</p>
        </Button>
      </Link>
    </div>
  );
};

export default LoginForm;
