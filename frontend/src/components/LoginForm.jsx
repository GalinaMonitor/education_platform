import React, {FC, useState} from 'react';
import {Button, Form, Input} from "antd";
import {rules} from "../utils/rules";
import useUserStore from "../store";
import {Link} from "react-router-dom";

const LoginForm: FC = () => {
    const {isLoading, error, login} = useUserStore()
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')

    const submit = () => {
        login(email, password)
    }

    return (
        <Form
            onFinish={submit}
            layout="vertical"
        >
            {error && <div style={{color: 'red'}}>
                {error}
            </div>}
            <Form.Item
                label='Ваша почта'
                name='email'
                rules={[
                    rules.required('Введите email')
                ]}
            >
                <Input value={email} onChange={e => setEmail(e.target.value)}/>
            </Form.Item>
            <Form.Item
                label='Пароль'
                name='password'
                rules={[
                    rules.required('Введите пароль')
                ]}
            >
                <Input type='password' value={password} onChange={e => setPassword(e.target.value)}/>
            </Form.Item>
            <Form.Item className={"mb-2"}>
                <Button style={{width: "100%"}} type={"primary"} htmlType='submit' loading={isLoading}>
                    Войти
                </Button>
            </Form.Item>
        </Form>
    );
};

export default LoginForm;