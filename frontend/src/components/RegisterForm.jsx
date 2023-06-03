import React, { useState } from "react";
import useUserStore from "../store/useUserStore";
import { Button, Checkbox, Form, Input } from "antd";
import { rules } from "../utils/rules";
import { Link } from "react-router-dom";

const RegisterForm = ({ handleFormData, onSubmit = null }) => {
  const { isLoading } = useUserStore();
  const { register } = useUserStore();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const submit = () => {
    register(email, password);
  };

  return (
    <div className={"w-96"}>
      <Form onFinish={submit} layout="vertical">
        <Form.Item
          label={<p className={"text-md font-semibold"}>ВВЕДИТЕ ПОЧТУ</p>}
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
          name="password"
          label={<p className={"text-md font-semibold"}>ПРИДУМАЙТЕ ПАРОЛЬ</p>}
          rules={[
            {
              required: true,
              message: "Введите пароль",
            },
          ]}
          hasFeedback
        >
          <Input.Password className={"big-button"} style={{ width: "100%" }} />
        </Form.Item>
        <Form.Item
          name="confirm"
          label={<p className={"text-md font-semibold"}>ПОВТОРИТЕ ПАРОЛЬ</p>}
          dependencies={["password"]}
          rules={[
            {
              required: true,
              message: "Please confirm your password!",
            },
            ({ getFieldValue }) => ({
              validator(_, value) {
                if (!value || getFieldValue("password") === value) {
                  return Promise.resolve();
                }
                return Promise.reject(new Error("Пароли не совпадают"));
              },
            }),
          ]}
          hasFeedback
        >
          <Input.Password
            className={"big-button"}
            style={{ width: "100%" }}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </Form.Item>
        <Form.Item
          name="agreement"
          rules={[
            {
              validator: (_, checked) =>
                checked
                  ? Promise.resolve()
                  : Promise.reject(
                      new Error(
                        "Вам нужно согласиться с пользовательским соглашением"
                      )
                    ),
            },
          ]}
          valuePropName="checked"
        >
          <Checkbox>
            <p style={{ whiteSpace: "nowrap" }}>
              я согласен(а) с <a href={"/"}>политикой конфиденциальности</a>
            </p>
          </Checkbox>
        </Form.Item>
        <Form.Item className={"mb-2"}>
          <Button
            className={"big-button"}
            style={{ width: "100%" }}
            type={"primary"}
            htmlType="submit"
            loading={isLoading}
          >
            <p className={"font-semibold"}>ЗАРЕГИСТРИРОВАТЬСЯ</p>
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

export default RegisterForm;
