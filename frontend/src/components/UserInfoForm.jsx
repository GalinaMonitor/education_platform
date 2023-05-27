import React, {FC, useState} from 'react';
import {Button, Form, Input} from "antd";
import {rules} from "../utils/rules";
import useUserStore from "../store";
import {useFetching} from "../hooks/useFetching";
import UserService from "../services/UserService";
import {Link, useNavigate} from "react-router-dom";
import {RouteNames} from "../router";

const UserInfoForm: FC = ({handleFormData, onSubmit = null}) => {
    const {isLoading, checkAuth} = useUserStore()
    const {user} = useUserStore()
    const navigate = useNavigate();
    const [fullname, setFullname] = useState('')
    const [company, setCompany] = useState('')
    const [job, setJob] = useState('')

    const [patchUser, userIsLoading, userError] = useFetching(async (data) => {
        const response = await UserService.patch(data)
    })

    const submit = () => {
        patchUser({fullname, company, job, passed_welcome_page: true})
        checkAuth()
        navigate(RouteNames.MAIN)
    }

    const rejection = () => {
        patchUser({passed_welcome_page: true})
        checkAuth()
        navigate(RouteNames.MAIN)
    }

    return (
        <div className={"w-96"}>
            <Form
                onFinish={submit}
                layout="vertical"
            >
                <Form.Item
                    name='fullname'
                >
                    <Input className={"big-button"} style={{width: "100%"}} placeholder={"Как вас зовут?"}/>
                </Form.Item>
                <Form.Item
                    name='company'
                >
                    <Input className={"big-button"} style={{width: "100%"}} placeholder={"В какой компании вы работаете?"}/>
                </Form.Item>
                <Form.Item
                    name='job'
                >
                    <Input className={"big-button"} style={{width: "100%"}} placeholder={"Кем вы работаете?"}/>
                </Form.Item>
                <Form.Item className={"mb-2"}>
                    <Button className={"big-button"} style={{width: "100%"}} type={"primary"} htmlType={'submit'} loading={isLoading}>
                        <p className={"font-semibold"}>ПОЗНАКОМИТЬСЯ</p>
                    </Button>
                </Form.Item>
            </Form>
            <Link to="/register">
                <Button className={"big-button"} style={{width: "100%"}} type={"default"} htmlType={'submit'} loading={isLoading} onClick={rejection}>
                    <p className={"font-semibold"}>НЕ ХОЧУ</p>
                </Button>
            </Link>
        </div>
    );
};

export default UserInfoForm;