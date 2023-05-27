import React from 'react';
import {Image, Layout, Row} from "antd";
import RegisterForm from "../components/RegisterForm";


const Register = () => {
    return (
        <Layout className={'h-full bg-white flex flex-col justify-center'}>
            <Row justify="center" align="middle"><Image width={382} src={'/ku-logo.svg'} preview={false}/></Row>
            <Row justify="center" align="middle" className={"mt-32"}>
                <RegisterForm/>
            </Row>
        </Layout>
    );
};

export default Register;