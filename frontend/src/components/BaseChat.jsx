import React, { useEffect, useState } from "react";
import { useFetching } from "../hooks/useFetching";
import InfiniteScroll from "react-infinite-scroll-component";
import { Avatar, List, Row, Skeleton } from "antd";
import Divider from "./UI/Divider";
import UserService from "../services/UserService";
import Message from "./Message";
import TextBlock from "./UI/TextBlock";
import Card from "./UI/Card";

const BaseChat = () => {
  const [messages, setMessages] = useState([]);
  const [limit, setLimit] = useState(10);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(1);

  const [fetchMessages, isLoading, error] = useFetching(async (limit, page) => {
    const response = await UserService.get_messages(limit, page);

    const newMessages = response.data.items;
    newMessages.reverse();
    if (page === 1) {
      setMessages([...newMessages]);
    } else {
      setMessages([...newMessages, ...messages]);
    }
    if (newMessages.length < limit) {
      setHasMore(false);
    }
  });

  useEffect(() => {
    fetchMessages(limit, page);
  }, [limit, page]);

  return (
    <Card className={"relative h-full"} text={"ЧАТ С ПЛАТФОРМОЙ"}>
      <div
        id="scrollableDiv"
        className={`w-full pt-5 overflow-auto flex flex-col-reverse`}
        style={{
          overflowAnchor: "none",
          height: "80%",
        }}
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
          dataLength={messages.length}
          next={() => {
            setPage(page + 1);
          }}
          style={{ display: "flex", flexDirection: "column-reverse" }}
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
          endMessage={
            <Divider plain>
              <p className={"text-gray-400"}>Начало переписки</p>
            </Divider>
          }
          scrollableTarget="scrollableDiv"
        >
          <List
            dataSource={messages}
            renderItem={(item) => (
              <Message
                key={item.id}
                text={item.content}
                time={item.datetime}
                type={item.content_type}
              />
            )}
          />
        </InfiniteScroll>
      </div>
      <Row className={"absolute bottom-5"}>
        <Avatar size={70} src={"/tolya.svg"} />
        <TextBlock
          className={"ml-5"}
          bigText={"Робот Анатолий"}
          smallText={"Куратор"}
        />
      </Row>
    </Card>
  );
};

export default BaseChat;
