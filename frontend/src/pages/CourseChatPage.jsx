import React, {FC, useEffect, useState} from 'react';
import Navbar from "../components/Navbar";
import {Col, Row, Image} from "antd";
import ProgramList from "../components/CourseList";
import '../App.css'
import Card from '../components/UI/Card';
import {Link, useParams} from "react-router-dom";
import ThemeList from "../components/ThemeList";
import {RouteNames} from "../router";
import TextBlock from "../components/UI/TextBlock";
import {useFetching} from "../hooks/useFetching";
import CourseService from "../services/CourseService";
import CourseChat from "../components/CourseChat";

const CourseChatPage: FC = () => {
    const {id} = useParams();
    const [course, setCourse] = useState({})
    const [fetchCourse, isLoading, error] = useFetching(async () => {
        const response = await CourseService.retrieve(id)
        setCourse(response.data)
    })
    const [themeId, setThemeId] = useState(null)
    useEffect(() => {
        fetchCourse()
    }, [])

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
                        <Row justify={'space-around'} align={'middle'} className={"h-full"}>
                            <TextBlock small_text={'Куратор'} big_text={'Елизавета'}/>
                            <Link to={RouteNames.MAIN}>
                                <Image src={'/lizbet.svg'} preview={false}/>
                            </Link>
                        </Row>
                    </Card>
                </Col>
                <Col span={6}>
                    <Card style={{height: '600px'}} className={'mr-2.5 mt-5 mb-5'} text={'СТРУКТУРА ОБУЧЕНИЯ'}>
                        <ThemeList course_chapter_id={id} setThemeId={setThemeId}/>
                    </Card>
                </Col>
                <Col span={12}>
                    <Card style={{height: '600px'}} className={'mt-5 mr-10 mb-5'}
                          text={`ЧАТ С НАСТАВНИКОМ ${course.name}`}>
                        <CourseChat course_chapter_id={id} theme_id={themeId}/>
                    </Card>
                </Col>
            </Row>
        </>
    );
};

export default CourseChatPage;