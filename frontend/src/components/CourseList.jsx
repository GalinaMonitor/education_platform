import React, {FC, useEffect, useState} from 'react';
import TextBlock from "./UI/TextBlock";
import CourseService from "../services/CourseService";
import {useFetching} from "../hooks/useFetching";
import {Button} from "antd";
import Divider from "./UI/Divider";
import {format_time} from "../utils/utils";
import VectorSVG from "./UI/VectorSVG";
import Card from "./UI/Card";
import ChooseLevelModal from "./Modals/ChooseLevelModal";
import ChooseTimeModal from "./Modals/ChooseTimeModal";
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
        const response = await CourseChapterService.retrieve(course_chapter_id)
        setCourseChapter(response.data)
    })

    useEffect(() => {
        fetchCourses()
        if (course_chapter_id) {
            fetchCourseChapter(course_chapter_id)
        }
    }, [course_chapter_id])

    return (
        <Card text={'ПРОГРАММЫ ДЛЯ ИЗУЧЕНИЯ'}>
            {courses.map((course, index) => <div key={course.id} className={"mb-5"}>
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
            )}
            <ChooseTimeModal isModalOpen={isTimeModalOpen} handleCancel={handleCancel} modalCourseId={modalCourseId}/>
            <ChooseLevelModal isModalOpen={isCourseModalOpen} course={course} handleCancel={handleCancel}/>
        </Card>
    )
}

export default CourseList;