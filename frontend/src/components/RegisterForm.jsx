import React, {FC, useState} from 'react';
import {Button, Form, Input} from "antd";
import {rules} from "../utils/rules";
import useUserStore from "../store";

const RegisterForm: FC = () => {
    const {isLoading, error} = useUserStore()
    const [email, setEmail] = useState('')

    const submit = () => {}

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
            <Form.Item>
                <Button htmlType='submit' loading={isLoading}>
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default RegisterForm;