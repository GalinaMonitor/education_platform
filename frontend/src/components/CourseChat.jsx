import React, { useEffect, useState } from "react";
import { useFetching } from "../hooks/useFetching";
import { Skeleton } from "antd";
import CourseChapterService from "../services/CourseChapterService";
import UserService from "../services/UserService";
import Message from "./Message";
import InfiniteScroll from "./UI/InfiniteScroll";
import Card from "./UI/Card";

const CourseChat = ({ courseName, courseChapterId = null, themeId = null }) => {
  const [messages, setMessages] = useState([]);
  const [limit, setLimit] = useState(10);
  const [lastNext, setLastNext] = useState(0);
  const [lastPrevious, setLastPrevious] = useState(0);
  const [hasMoreNext, setHasMoreNext] = useState(true);
  const [hasMorePrevious, setHasMorePrevious] = useState(true);
  const [page, setPage] = useState(1);
  const [reverseColumn, setReverseColumn] = useState(false);

  const [fetchThemeMessages, isLoadingTheme, errorTheme] = useFetching(
    async () => {
      const response = await CourseChapterService.get_messages({
        id: courseChapterId,
        limit,
        themeId,
      });
      const newMessages = response.data;

      if (newMessages.length) {
        newMessages.reverse();
        setHasMorePrevious(true);
        setHasMoreNext(true);
        setLastNext(newMessages[newMessages.length - 1].id);
        setLastPrevious(newMessages[0].id);
        setMessages([...newMessages]);
        setReverseColumn(true);
      }
    }
  );

  useEffect(() => {
    fetchThemeMessages();
  }, [themeId, courseChapterId]);

  const [fetchMessagesNext, isLoadingNext, errorNext] = useFetching(
    async () => {
      const response = await CourseChapterService.get_messages({
        id: courseChapterId,
        limit,
        lastNext,
      });
      const newMessages = response.data;
      if (newMessages.length < limit) {
        setHasMoreNext(false);
      }
      if (newMessages.length) {
        newMessages.reverse();
        setLastNext(newMessages[newMessages.length - 1].id);
        setMessages([...messages, ...newMessages]);
      }
    }
  );

  const [fetchMessagesPrevious, isLoadingPrevious, errorPrevious] = useFetching(
    async () => {
      let response;
      if (!courseChapterId) {
        response = await UserService.get_messages(limit, page);
      } else {
        response = await CourseChapterService.get_messages({
          id: courseChapterId,
          limit,
          lastPrevious,
        });
      }
      const newMessages = response.data;
      if (newMessages.length < limit) {
        setHasMorePrevious(false);
      }
      if (newMessages.length) {
        newMessages.reverse();
        setLastPrevious(newMessages[0].id);
        setMessages([...newMessages, ...messages]);
      }
    }
  );
  return (
    <Card text={`ЧАТ С НАСТАВНИКОМ ${courseName}`} style={{ height: "90%" }}>
      <div className={`h-full`}>
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
            <Message
              key={item.id}
              text={item.content}
              time={item.datetime}
              type={item.content_type}
            />
          ))}
        </InfiniteScroll>
      </div>
    </Card>
  );
};

export default CourseChat;
