import React, {FC} from 'react';
import Navbar from "../components/Navbar";
import {Col, Row} from "antd";
import ProgramList from "../components/CourseList";
import '../App.css'
import Card from '../components/UI/Card';
import Chat from "../components/Chat";

const Main: FC = () => {
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
                        <Chat show_lizbet={true}/>
                    </Card>
                </Col>
            </Row>
        </div>
    );
};

export default Main;