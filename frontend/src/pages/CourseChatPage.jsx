import React, {FC, useEffect, useState} from 'react';
import Navbar from "../components/Navbar";
import {Col, Row, Image} from "antd";
import CourseList from "../components/CourseList";
import '../App.css'
import {useParams} from "react-router-dom";
import ThemeList from "../components/ThemeList";
import {useFetching} from "../hooks/useFetching";
import CourseService from "../services/CourseService";
import CourseChat from "../components/CourseChat";
import useInterfaceStore from "../store/useInterfaceStore";
import Settings from "../components/Settings";
import LayoutThreeBlocks from "../components/UI/LayoutThreeBlocks";
import LizbetCard from "../components/LizbetCard";

const CourseChatPage: FC = () => {
    const {id} = useParams();
    const [course, setCourse] = useState({})
    const [fetchCourse, isLoading, error] = useFetching(async () => {
        const response = await CourseService.retrieve(id)
        console.log(response.data)
        setCourse(response.data)
    })
    const [themeId, setThemeId] = useState(null)
    const {isOpenSettings} = useInterfaceStore()

    useEffect(() => {
        fetchCourse()
    }, [])

    return (
        <LayoutThreeBlocks>
            {isOpenSettings ?
                <Settings/> :
                <>
                    <CourseList course_chapter_id={id}/>
                    <LizbetCard classname={"mt-5"}/>
                </>
            }
            <ThemeList course_chapter_id={id} setThemeId={setThemeId} color={course.color}/>
            <CourseChat course_name={course.name} course_chapter_id={id} theme_id={themeId}/>
        </LayoutThreeBlocks>
    );
};

export default CourseChatPage;