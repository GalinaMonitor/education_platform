import React from 'react';
import {Card, Row} from "antd";
import RegisterForm from "../components/RegisterForm";
import {Link} from "react-router-dom";

const Register = () => {
    return (
        <Row justify="center" align="middle" className="h100">
            <Card>
                <RegisterForm/>
                <Link to="/login">Войти</Link>
            </Card>
        </Row>
    );
};

export default Register;