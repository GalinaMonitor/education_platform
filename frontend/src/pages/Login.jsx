import React from 'react';
import {Card, Row} from "antd";
import LoginForm from "../components/LoginForm";
import {Link} from "react-router-dom";

const Login = () => {
    return (
        <Row justify="center" align="middle" className="h100">
            <Card>
                <LoginForm/>
                <Link to="/register">Регистрация</Link>
            </Card>
        </Row>
    );
};

export default Login;