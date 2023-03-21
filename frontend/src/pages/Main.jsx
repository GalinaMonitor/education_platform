import React, {FC} from 'react';
import Navbar from "../components/Navbar";
import {Col, Row} from "antd";
import ProgramList from "../components/CourseList";
import '../App.css'
import Card from '../components/UI/Card';
import Chat from "../components/Chat";

const Main: FC = () => {
    return (
        <>
            <Card className={'ml-10 mt-10 mr-10'} text={''}>
                <Navbar/>
            </Card>
            <Row className={'h-fit'}>
                <Col span={8}>
                    <Card style={{height: '600px'}} className={'ml-10 mr-2.5 mt-5 mb-5'}
                          text={'ПРОГРАММЫ ДЛЯ ИЗУЧЕНИЯ'}>
                        <ProgramList/>
                    </Card>
                </Col>
                <Col span={16}>
                    <Card style={{height: '600px'}} className={'mt-5 mr-10 mb-5'} text={'ЧАТ С ПЛАТФОРМОЙ'}>
                        <Chat course_chapter_id={1}/>
                    </Card>
                </Col>
            </Row>
        </>
    );
};

export default Main;