import React, {useEffect} from 'react';
import {Card, Row} from "antd";
import {Link} from "react-router-dom";
import UserInfoForm from "../components/UserInfoForm";
import EmailForm from "../components/EmailForm";
import {useFetching} from "../hooks/useFetching";
import useUserStore from "../store";


const {useState} = React;


const Register = () => {
    const {register} = useUserStore()
    const [current, setCurrent] = useState(0);
    const [formValues, setFormValues] = useState({})
    const [registerUser, isLoading, error] = useFetching(async () => {
        if (
            formValues.hasOwnProperty('email') &&
            formValues.hasOwnProperty('job') &&
            formValues.hasOwnProperty('fullname') &&
            formValues.hasOwnProperty('company')
        ) {
            register(formValues)
        }
    })

    useEffect(() => {
        registerUser()
    }, [formValues])

    const next = () => {
        const last_step = 2
        if (current !== last_step) {
            setCurrent(current + 1);
        }
    };

    const handleInputData = (values_obj) => {
        setFormValues({
            ...formValues,
            ...values_obj
        });
    }

    const steps = [
        {
            title: 'Введите почту',
            content: <UserInfoForm handleFormData={handleInputData} onSubmit={next}/>,
        },
        {
            title: 'Введите ваши данные',
            content: <EmailForm handleFormData={handleInputData} onSubmit={next}/>,
        },
        {
            title: '',
            content: <p>Пароль на почте</p>
        }
    ];

    return (
        <Row justify="center" align="middle" className="h100">
            <Card>
                <>
                    <h2>{steps[current].title}</h2>
                    <div>{steps[current].content}</div>
                </>
                <Link to="/login">Войти</Link>
            </Card>
        </Row>
    );
};

export default Register;