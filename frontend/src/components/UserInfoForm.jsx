import React, { useState } from "react";
import { Button, Form, Input } from "antd";
import useUserStore from "../store/useUserStore";
import { useFetching } from "../hooks/useFetching";
import UserService from "../services/UserService";
import { useNavigate } from "react-router-dom";
import { RouteNames } from "../router";

const UserInfoForm = () => {
  const { isLoading, checkAuth } = useUserStore();
  const { user } = useUserStore();
  const navigate = useNavigate();
  const [fullname, setFullname] = useState("");
  const [company, setCompany] = useState("");
  const [job, setJob] = useState("");

  const [patchUser, userIsLoading, userError] = useFetching(async (data) => {
    await UserService.patch(data);
    await checkAuth();
  });

  const submit = () => {
    patchUser({ fullname, company, job, passed_welcome_page: true });
    setTimeout(navigate, 500, RouteNames.MAIN);
  };

  const rejection = () => {
    patchUser({ passed_welcome_page: true });
    setTimeout(navigate, 500, RouteNames.MAIN);
  };

  return (
    <div style={{ width: 460 }}>
      <Form onFinish={submit} layout="vertical">
        <Form.Item name="fullname">
          <Input
            className={"big-button"}
            style={{ width: "100%" }}
            placeholder={"Как вас зовут?"}
          />
        </Form.Item>
        <Form.Item name="company">
          <Input
            className={"big-button"}
            style={{ width: "100%" }}
            placeholder={"В какой компании вы работаете?"}
          />
        </Form.Item>
        <Form.Item name="job">
          <Input
            className={"big-button"}
            style={{ width: "100%" }}
            placeholder={"Кем вы работаете?"}
          />
        </Form.Item>
        <Form.Item className={"mb-2"}>
          <Button
            className={"big-button"}
            style={{ width: "100%" }}
            type={"primary"}
            htmlType={"submit"}
            loading={isLoading}
          >
            <p className={"font-semibold"}>ПОЗНАКОМИТЬСЯ</p>
          </Button>
        </Form.Item>
      </Form>
      <Button
        className={"big-button"}
        style={{ width: "100%" }}
        type={"default"}
        htmlType={"submit"}
        loading={isLoading}
        onClick={rejection}
      >
        <p className={"font-semibold"}>НЕ ХОЧУ</p>
      </Button>
    </div>
  );
};

export default UserInfoForm;
