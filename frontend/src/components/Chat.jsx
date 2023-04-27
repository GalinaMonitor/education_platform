import React, {useEffect, useState} from 'react';
import {useFetching} from "../hooks/useFetching";
import InfiniteScroll from "react-infinite-scroll-component";
import {Divider, Image, List, Row, Skeleton} from "antd";
import CourseChapterService from "../services/CourseChapterService";
import UserService from "../services/UserService";
import Message from "./Message";
import TextBlock from "./UI/TextBlock";

const Chat = ({course_chapter_id = null, show_lizbet = false}) => {
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

    let className = ""
    if (show_lizbet) {
        className += "w-4/5"
    }

    return (
        <div style={{height: "90%"}}>
            <div
                id="scrollableDiv"
                className={`${className} pt-5 overflow-auto flex flex-col-reverse h-full`}
                style={{
                    overflowAnchor: 'none',
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
            {
                show_lizbet && (
                    <div className={'absolute bottom-10 right-24 text-right'}>
                        <Row>
                            <TextBlock big_text={"Елизавета"} small_text={"Куратор"}/>
                            <Image className={'ml-5'} width={"100px"} src={"/lizbet.svg"} preview={false}/>
                        </Row>
                    </div>
                )
            }
        </div>
    );
};

export default Chat;