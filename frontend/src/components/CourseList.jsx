import React, {FC, useEffect, useState} from 'react';
import TextBlock from "./UI/TextBlock";
import CourseService from "../services/CourseService";
import {useFetching} from "../hooks/useFetching";
import {Button, Divider, Dropdown, Modal, Select} from "antd";
import {Link} from "react-router-dom";
import {RouteNames} from "../router";
import {timeOptions} from "../utils/constants";

const CourseList: FC = () => {
    const [courses, setCourses] = useState([])
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [modalCourseId, setModalCourseId] = useState(null)
    const [modalReceiveTime, setModalReceiveTime] = useState('10:00')

    const showModal = (course_id) => {
        setModalCourseId(course_id)
        setIsModalOpen(true);
    };

    const handleTimeChange = (value) => {
        setModalReceiveTime(value)
    }

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const [fetchCourses, isLoading, error] = useFetching(async () => {
        const response = await CourseService.get()
        setCourses([...response.data])
    })

    const [updateReceiveTime, TimeIsLoading, TimeError] = useFetching(async () => {
        await CourseService.set_receive_time(modalCourseId, modalReceiveTime)
    })

    const handleOk = () => {
        updateReceiveTime()
        setIsModalOpen(false);
        setTimeout(fetchCourses, 100);
    };

    useEffect(() => {
        fetchCourses()
    }, [])

    return (
        <>
            {courses.map((course, index) =>
                <>
                    <Dropdown menu={{
                        items:
                            course.coursechapters.map((item) => {
                                return {
                                    key: item.id,
                                    label: (
                                        <Link to={`${RouteNames.COURSE_CHAT}/${item.id}`}>{item.name}</Link>
                                    ),
                                }
                            })
                    }} placement="top">
                        <Button>Уровень</Button>
                    </Dropdown>
                    <Button onClick={() => {
                        showModal(course.id)
                    }}>{course.receive_time}</Button>
                    <TextBlock key={course.id} big_text={course.name}/>
                    <Divider/>
                </>
            )}
            <Modal open={isModalOpen} onCancel={handleCancel} footer={[]}>
                <p className={'text-center'}>Во сколько Вам будет удобно получать обучающий материал?</p>
                <div>
                    <Select defaultValue="10:00" options={timeOptions} onChange={handleTimeChange}/>
                    <Button onClick={handleOk}>ОК</Button>
                </div>
            </Modal>
        </>
    )
}

export default CourseList;