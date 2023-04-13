import React from 'react';
import useUserStore from "../store";
import {Button, Form, Input} from "antd";
import {rules} from "../utils/rules";

const EmailForm = ({handleFormData, onSubmit = null}) => {
    const {isLoading, error} = useUserStore()

    const submit = (values) => {
        handleFormData(values)
        if (onSubmit) {
            onSubmit()
        }
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
                label='Email'
                name='email'
                rules={[
                    rules.required('Введите email')
                ]}
            >
                <Input/>
            </Form.Item>
            <Form.Item className={"mb-2"}>
                <Button style={{width: "100%"}} htmlType='submit' loading={isLoading}>
                    Отправить
                </Button>
            </Form.Item>
        </Form>
    );
};

export default EmailForm;