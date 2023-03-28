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
            <Form.Item>
                <Button htmlType='submit' loading={isLoading}>
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default EmailForm;