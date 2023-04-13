import React, {FC, useEffect, useState} from 'react';
import TextBlock from "./UI/TextBlock";
import CourseService from "../services/CourseService";
import {useFetching} from "../hooks/useFetching";
import {Button, Divider, Image, Modal, Row, Select} from "antd";
import {Link, useNavigate} from "react-router-dom";
import {RouteNames} from "../router";
import {timeOptions} from "../utils/constants";
import {format_time} from "../utils/utils";

const CourseList: FC = () => {
    const navigate = useNavigate();
    const [courses, setCourses] = useState([])
    const [courseChapters, setCourseChapters] = useState([])
    const [isTimeModalOpen, setIsTimeModalOpen] = useState(false);
    const [isCourseModalOpen, setIsCourseModalOpen] = useState(false);
    const [modalCourseId, setModalCourseId] = useState(null)
    const [timeModalReceiveTime, setTimeModalReceiveTime] = useState('10:00')

    const showTimeModal = (course_id) => {
        setModalCourseId(course_id)
        setIsTimeModalOpen(true);
    };

    const showCourseModal = (coursechapters) => {
        setCourseChapters(coursechapters)
        setIsCourseModalOpen(true);
    };

    const handleTimeChange = (value) => {
        setTimeModalReceiveTime(value)
    }

    const handleCancel = () => {
        setIsTimeModalOpen(false);
        setIsCourseModalOpen(false);
    };

    const [fetchCourses, isLoading, error] = useFetching(async () => {
        const response = await CourseService.get()
        setCourses([...response.data])
    })

    const [updateReceiveTime, TimeIsLoading, TimeError] = useFetching(async () => {
        await CourseService.set_receive_time(modalCourseId, timeModalReceiveTime)
    })

    const handleOk = () => {
        updateReceiveTime()
        setTimeModalReceiveTime('10:00');
        setIsTimeModalOpen(false);
        setTimeout(fetchCourses, 100);
    };

    const previewImages = [
        {level: "Базовый", image: "/base-level.svg"},
        {level: "Продвинутый", image: "/medium-level.svg"},
        {level: "Эксперт", image: "/expert-level.svg"},
    ]

    useEffect(() => {
        fetchCourses()
    }, [])

    return (
        <>
            {courses.map((course, index) =>
                <>
                    <Button className={'mr-2'} shape={"round"} onClick={() =>
                        showTimeModal(course.id)
                    }>{format_time(course.receive_time)}</Button>
                    <Button shape={"round"} onClick={() => {
                        showCourseModal(course.coursechapters)
                    }}>
                        Уровень
                    </Button>
                    <TextBlock key={course.id} big_text={course.name}/>
                    <Divider/>
                </>
            )}
            <Modal open={isTimeModalOpen} onCancel={handleCancel} footer={[]}>
                <p className={'text-center'}>Во сколько Вам будет удобно получать обучающий материал?</p>
                <div>
                    <Select value={timeModalReceiveTime} options={timeOptions} onChange={handleTimeChange}/>
                    <Button onClick={handleOk}>ОК</Button>
                </div>
            </Modal>
            <Modal open={isCourseModalOpen} onCancel={handleCancel} footer={[]} width={'700px'}>
                <p className={'text-center'}>Какой уровень Вас интересует</p>
                <Row justify={'space-around'} align={'middle'}>
                    {courseChapters.map((item, index) =>
                        <Image key={item.id} src={previewImages[index].image} preview={false} onClick={() => {
                            navigate(`${RouteNames.COURSE_CHAT}/${item.id}`)
                            handleCancel()
                        }}/>
                    )}
                </Row>
                <Link to={"/"}><p className={'text-center'}>Изучить структуру обучения</p></Link>
            </Modal>
        </>
    )
}

export default CourseList;