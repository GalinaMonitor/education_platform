import React, {FC, useEffect, useState} from 'react';
import TextBlock from "./UI/TextBlock";
import CourseService from "../services/CourseService";
import {useFetching} from "../hooks/useFetching";
import {Button, Divider} from "antd";
import {format_time} from "../utils/utils";
import VectorSVG from "./UI/VectorSVG";
import Card from "./UI/Card";
import ChooseLevel from "./Modals/ChooseLevel";
import ChooseTime from "./Modals/ChooseTime";
import CourseChapterService from "../services/CourseChapterService";

const CourseList: FC = ({course_chapter_id = null}) => {
    const [courses, setCourses] = useState([])
    const [course, setCourse] = useState(null)
    const [courseChapter, setCourseChapter] = useState({})
    const [isTimeModalOpen, setIsTimeModalOpen] = useState(false);
    const [isCourseModalOpen, setIsCourseModalOpen] = useState(false);
    const [modalCourseId, setModalCourseId] = useState(null)

    const showTimeModal = (course_id, time) => {
        setModalCourseId(course_id)
        setIsTimeModalOpen(true)
    };

    const showCourseModal = (course) => {
        setCourse(course)
        setIsCourseModalOpen(true);
    };

    const handleCancel = async () => {
        setIsTimeModalOpen(false);
        setIsCourseModalOpen(false);
        await fetchCourses()
    };

    const [fetchCourses, isLoading, error] = useFetching(async () => {
        const response = await CourseService.get()
        setCourses([...response.data])
    })

    const [fetchCourseChapter] = useFetching(async (course_chapter_id) => {
        const response = await CourseChapterService.retrieve({id: course_chapter_id})
        setCourseChapter(response.data)
    })

    useEffect(() => {
        fetchCourses()
        if (course_chapter_id) {
            fetchCourseChapter(course_chapter_id)
        }
    }, [])

    return (
        <Card text={'ПРОГРАММЫ ДЛЯ ИЗУЧЕНИЯ'}>
            {courses.map((course, index) => {
                return <div key={course.id}>
                    <Button className={"mr-1.5 p-0 small-button"} shape={"round"} onClick={() => {
                        showCourseModal(course)
                    }}>
                        {courseChapter.course_id === course.id ? courseChapter.name : "Уровень"}
                    </Button>
                    <Button className={"p-0 small-button"} shape={"round"} onClick={() =>
                        showTimeModal(course.id, format_time(course.receive_time))
                    }>{format_time(course.receive_time)}</Button>
                    <div className={"flex flex-row items-center"}>
                        <VectorSVG color={course.color}/>
                        <TextBlock className={"ml-1.5"} key={course.id} big_text={course.name}/>
                    </div>
                    <Divider/>
                </div>
            })}
            <ChooseTime isModalOpen={isTimeModalOpen} handleCancel={handleCancel} modalCourseId={modalCourseId}/>
            <ChooseLevel isModalOpen={isCourseModalOpen} course={course} handleCancel={handleCancel}/>
        </Card>
    )
}

export default CourseList;