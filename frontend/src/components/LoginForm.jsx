import React, {FC, useState} from 'react';
import {Button, Form, Input} from "antd";
import {rules} from "../utils/rules";
import useUserStore from "../store";

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
        >
            {error && <div style={{color: 'red'}}>
                {error}
            </div>}
            <Form.Item
                label='Email'
                name='email'
                rules={[
                    rules.required('Введите email')
                ]}
            >
                <Input value={email} onChange={e => setEmail(e.target.value)}/>
            </Form.Item>
            <Form.Item
                label='Password'
                name='password'
                rules={[
                    rules.required('Введите пароль')
                ]}
            >
                <Input type='password' value={password} onChange={e => setPassword(e.target.value)}/>

            </Form.Item>
            <Form.Item>
                <Button htmlType='submit' loading={isLoading}>
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default LoginForm;