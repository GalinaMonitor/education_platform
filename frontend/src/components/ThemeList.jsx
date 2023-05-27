import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import TextBlock from "./UI/TextBlock";
import ThemeService from "../services/ThemeService";
import Card from "./UI/Card";
import Divider from "./UI/Divider";

const ThemeList = ({course_chapter_id, setThemeId, color}) => {
    const [themes, setThemes] = useState([])
    const [fetchThemes, isLoading, error] = useFetching(async () => {
        const response = await ThemeService.get(course_chapter_id)
        setThemes([...response.data])
    })

    useEffect(() => {
        fetchThemes()
    }, [course_chapter_id])

    return (
        <Card text={'БЛОКИ ОБУЧЕНИЯ'}>
            {themes.map((theme, index) =>
                <div key={theme.id} onClick={() => setThemeId(theme.id)}>
                    <TextBlock key={theme.id} big_text={theme.name} small_text={`Задача №${index + 1}`}/>
                    <Divider color={color}/>
                </div>
            )}
        </Card>
    )
};

export default ThemeList;