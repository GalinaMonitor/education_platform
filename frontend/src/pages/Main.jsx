import React, {FC, useEffect} from 'react';
import Navbar from "../components/Navbar";
import {Col, Row} from "antd";
import ProgramList from "../components/CourseList";
import '../App.css'
import Card from '../components/UI/Card';
import BaseChat from "../components/BaseChat";
import {RouteNames} from "../router";
import {useNavigate} from "react-router-dom";
import useUserStore from "../store";

const Main: FC = () => {
    const {user} = useUserStore()

    const navigate = useNavigate();
    useEffect(() => !user.passed_welcome_page ? navigate(RouteNames.WELCOME) : undefined, [])
    return (
        <div className={'h-full'}>
            <Card className={'ml-10 mt-10 mr-10'} text={''}>
                <Navbar/>
            </Card>
            <Row className={'h-4/6'}>
                <Col span={6}>
                    <Card className={'h-full ml-10 mr-2.5 mt-5 mb-5'}
                          text={'ПРОГРАММЫ ДЛЯ ИЗУЧЕНИЯ'}>
                        <ProgramList/>
                    </Card>
                </Col>
                <Col span={18}>
                    <Card className={'mt-5 mr-10 mb-5v h-full'} text={'ЧАТ С ПЛАТФОРМОЙ'}>
                        <BaseChat/>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Main;