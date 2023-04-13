import React from 'react';
import {Button, Card, Image, Layout, Row} from "antd";
import LoginForm from "../components/LoginForm";
import {Link} from "react-router-dom";

const Login = () => {
    return (
        <Layout className={'h-full bg-white flex flex-col justify-center'}>
            <Row justify="center" align="middle"><Image width={80} src={'/lizbet.svg'} preview={false}/></Row>
            <Row justify="center" align="middle"><Image width={300} src={'/ku-logo.svg'} preview={false}/></Row>
            <Row justify="center" align="middle" className={"mt-10"}>
                <Card style={{background: "#F1F1F1", paddingRight: "50px", paddingLeft: "50px"}}>
                    <LoginForm/>
                    <Link to="/register"><Button style={{width: "100%"}}>Регистрация</Button></Link>
                </Card>
            </Row>
        </Layout>
    );
};

export default Login;