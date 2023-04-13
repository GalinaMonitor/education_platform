import React, {FC} from 'react';
import {Button, Form, Input} from "antd";
import {rules} from "../utils/rules";
import useUserStore from "../store";

const UserInfoForm: FC = ({handleFormData, onSubmit = null}) => {
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
                label='Имя'
                name='fullname'
                rules={[
                    rules.required('Введите email')
                ]}
            >
                <Input/>
            </Form.Item>
            <Form.Item
                label='Компания'
                name='company'
                rules={[
                    rules.required('Введите компанию')
                ]}
            >
                <Input/>
            </Form.Item>
            <Form.Item
                label='Должность'
                name='job'
                rules={[
                    rules.required('Введите должность')
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

export default UserInfoForm;