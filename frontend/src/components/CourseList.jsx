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

    const showModal = (course_id) => {
        console.log(course_id)
        setIsModalOpen(true);
    };

    const handleOk = () => {
        setIsModalOpen(false);
    };

    const handleCancel = () => {
        setIsModalOpen(false);
    };

    const [fetchCourses, isLoading, error] = useFetching(async () => {
        const response = await CourseService.get()
        setCourses([...response.data])
    })

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
                    }}>Время</Button>
                    <TextBlock key={course.id} big_text={course.name}/>
                    <Divider/>
                </>
            )}
            <Modal open={isModalOpen} onCancel={handleCancel} footer={[]}>
                <p className={'text-center'}>Во сколько Вам будет удобно получать обучающий материал?</p>
                <div>
                    <Select defaultValue="10:00" options={timeOptions}/>
                    <Button onClick={handleOk}>ОК</Button>
                </div>
            </Modal>
        </>
    )
}

export default CourseList;