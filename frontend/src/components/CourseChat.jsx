import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import {Image, Row, Skeleton} from "antd";
import CourseChapterService from "../services/CourseChapterService";
import UserService from "../services/UserService";
import Message from "./Message";
import InfiniteScroll from "./UI/InfiniteScroll";
import Card from "./UI/Card";

const CourseChat = ({course_name, course_chapter_id = null, theme_id = null}) => {
    const [messages, setMessages] = useState([])
    const [limit, setLimit] = useState(10);
    const [lastNext, setLastNext] = useState(0);
    const [lastPrevious, setLastPrevious] = useState(0);
    const [hasMoreNext, setHasMoreNext] = useState(true)
    const [hasMorePrevious, setHasMorePrevious] = useState(true)
    const [page, setPage] = useState(1);
    const [reverseColumn, setReverseColumn] = useState(false)

    const [fetchThemeMessages, isLoadingTheme, errorTheme] = useFetching(async () => {
        let response;
        response = await CourseChapterService.get_messages({id: course_chapter_id, limit, theme_id})
        const new_messages = response.data

        if (new_messages.length) {
            new_messages.reverse()
            setHasMorePrevious(true)
            setHasMoreNext(true)
            setLastNext(new_messages[new_messages.length - 1].id)
            setLastPrevious(new_messages[0].id)
            setMessages([...new_messages])
            setReverseColumn(true)
        }
    })

    useEffect(() => {
        fetchThemeMessages()
    }, [theme_id])

    const [fetchMessagesNext, isLoadingNext, errorNext] = useFetching(async () => {
        let response;
        response = await CourseChapterService.get_messages({id: course_chapter_id, limit, lastNext})
        const new_messages = response.data
        if (new_messages.length < limit) {
            setHasMoreNext(false)
        }
        if (new_messages.length) {
            new_messages.reverse()
            setLastNext(new_messages[new_messages.length - 1].id)
            setMessages([...messages, ...new_messages])
        }
    })

    const [fetchMessagesPrevious, isLoadingPrevious, errorPrevious] = useFetching(async () => {
        let response;
        if (!course_chapter_id) {
            response = await UserService.get_messages(limit, page)
        } else {
            response = await CourseChapterService.get_messages({id: course_chapter_id, limit, lastPrevious})
        }
        const new_messages = response.data
        if (new_messages.length < limit) {
            setHasMorePrevious(false)
        }
        if (new_messages.length) {
            new_messages.reverse()
            setLastPrevious(new_messages[0].id)
            setMessages([...new_messages, ...messages])
        }

    })
    return (
        <Card text={`ЧАТ С НАСТАВНИКОМ ${course_name}`} style={{height: "90%"}}>
            <div
                className={`h-full`}
            >
                <InfiniteScroll
                    loadingComponent={
                        <Skeleton
                            paragraph={{
                                rows: 1,
                            }}
                            active
                        />
                    }
                    nextDataFn={() => fetchMessagesNext()}
                    nextEnd={!hasMoreNext}
                    nextLoading={isLoadingNext}
                    previousDataFn={() => fetchMessagesPrevious()}
                    previousEnd={!hasMorePrevious}
                    previousLoading={isLoadingPrevious}
                    initialReverse={reverseColumn}
                >
                    {messages.map((item, index) => (
                        <Message key={item.id} text={item.content} time={item.datetime}
                                 type={item.content_type}/>
                    ))}
                </InfiniteScroll>
            </div>
        </Card>

    );
};

export default CourseChat;