import React, {FC} from 'react';
import Navbar from "../components/Navbar";
import {Col, Row} from "antd";
import ProgramList from "../components/CourseList";
import '../App.css'
import Card from '../components/UI/Card';
import {Link, useParams} from "react-router-dom";
import Chat from "../components/Chat";
import ThemeList from "../components/ThemeList";
import {RouteNames} from "../router";

const CourseChat: FC = () => {
    const {id} = useParams();

    return (
        <>
            <Card className={'ml-10 mt-10 mr-10'} text={''}>
                <Navbar/>
            </Card>
            <Row>
                <Col span={6}>
                    <Card style={{height: '400px'}} className={'ml-10 mr-2.5 mt-5 mb-2.5'}
                          text={'ПРОГРАММЫ ДЛЯ ИЗУЧЕНИЯ'}>
                        <ProgramList/>
                    </Card>
                    <Card style={{height: '190px'}} className={'ml-10 mr-2.5 mb-5'}>
                        <Link to={RouteNames.MAIN}>Куратор Елизавета</Link>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card style={{height: '600px'}} className={'mr-2.5 mt-5 mb-5'} text={'СТРУКТУРА ОБУЧЕНИЯ'}>
                        <ThemeList course_chapter_id={id}/>
                    </Card>
                </Col>
                <Col span={12}>
                    <Card style={{height: '600px'}} className={'mt-5 mr-10 mb-5'} text={'ЧАТ С ПЛАТФОРМОЙ'}>
                        <Chat course_chapter_id={id}/>
                    </Card>
                </Col>
            </Row>
        </>
    );
};

export default CourseChat;