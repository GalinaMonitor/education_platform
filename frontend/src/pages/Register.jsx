import React, {useEffect} from 'react';
import {Button, Card, Image, Layout, Row} from "antd";
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
        <Layout className={'h-full bg-white flex flex-col justify-center'}>
            <Row justify="center" align="middle"><Image width={80} src={'/lizbet.svg'} preview={false}/></Row>
            <Row justify="center" align="middle"><Image width={300} src={'/ku-logo.svg'} preview={false}/></Row>
            <Row justify="center" align="middle" className={"mt-10"}>
                <Card style={{background: "#F1F1F1", paddingRight: "50px", paddingLeft: "50px"}}>
                    <>
                        <h2>{steps[current].title}</h2>
                        <div>{steps[current].content}</div>
                    </>
                    <Link to="/login"><Button type={"primary"} style={{width: "100%"}}>Войти</Button></Link>
                </Card>
            </Row>
        </Layout>
    );
};

export default Register;