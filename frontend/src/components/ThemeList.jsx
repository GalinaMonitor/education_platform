import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import {Divider} from "antd";
import TextBlock from "./UI/TextBlock";
import ThemeService from "../services/ThemeService";

const ThemeList = ({course_chapter_id}) => {
    const [themes, setThemes] = useState([])

    const [fetchThemes, isLoading, error] = useFetching(async () => {
        const response = await ThemeService.get(course_chapter_id)
        setThemes([...response.data])
    })

    useEffect(() => {
        fetchThemes()
    }, [course_chapter_id])

    return (
        <>
            {themes.map((theme, index) =>
                <>
                    <TextBlock key={theme.id} big_text={theme.name} small_text={`Задача №${index + 1}`}/>
                    <Divider/>
                </>
            )}
        </>
    )
};

export default ThemeList;