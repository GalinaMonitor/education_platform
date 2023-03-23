import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import Message from "./UI/Message";
import InfiniteScroll from "react-infinite-scroll-component";
import {Divider, List, Skeleton} from "antd";
import CourseChapterService from "../services/CourseChapterService";
import UserService from "../services/UserService";

const Chat = ({course_chapter_id = null}) => {
    const [messages, setMessages] = useState([])
    const [limit, setLimit] = useState(10);
    const [hasMore, setHasMore] = useState(true)
    const [page, setPage] = useState(1);

    const [fetchMessages, isLoading, error] = useFetching(async (limit, page) => {
        let response;
        if (!course_chapter_id) {
            response = await UserService.get_messages(limit, page)
        } else {
            response = await CourseChapterService.get_messages(course_chapter_id, limit, page)
        }
        const new_messages = response.data.items
        new_messages.reverse()
        if (page === 1) {
            setMessages([...new_messages])
        } else {
            setMessages([...new_messages, ...messages])
        }
        if (new_messages.length < limit) {
            setHasMore(false)
        }
    })

    useEffect(() => {
        fetchMessages(limit, page)
    }, [course_chapter_id, limit, page])

    return (
        <div
            id="scrollableDiv"
            style={{
                paddingTop: '50px',
                height: '500px',
                overflow: 'auto',
                overflowAnchor: 'none',
                display: 'flex',
                flexDirection: 'column-reverse',
            }}
        >
            <InfiniteScroll
                dataLength={messages.length}
                next={() => {
                    setPage(page + 1)
                }}
                style={{display: 'flex', flexDirection: 'column-reverse'}}
                inverse={true}
                hasMore={hasMore}
                loader={
                    <Skeleton
                        paragraph={{
                            rows: 1,
                        }}
                        active
                    />
                }

                endMessage={<Divider plain>It is all, nothing more 🤐</Divider>}
                scrollableTarget="scrollableDiv"
            >
                <List
                    dataSource={messages}
                    renderItem={(item) => (
                        <Message key={item.id} text={item.content} time={item.datetime}
                                 type={item.content_type}/>
                    )}
                />
            </InfiniteScroll>
        </div>
    );
};

export default Chat;