import React, { useEffect, useState } from "react";
import CourseList from "../components/CourseList";
import "../App.css";
import { useParams } from "react-router-dom";
import ThemeList from "../components/ThemeList";
import { useFetching } from "../hooks/useFetching";
import CourseService from "../services/CourseService";
import CourseChat from "../components/CourseChat";
import useInterfaceStore from "../store/useInterfaceStore";
import Settings from "../components/Settings";
import LayoutThreeBlocks from "../components/UI/LayoutThreeBlocks";
import CourseChapterService from "../services/CourseChapterService";
import ShareLink from "../components/ShareLink";
import LinksBlock from "../components/UI/LinksBlock";

const CourseChatPage = () => {
  const { id } = useParams();
  const [course, setCourse] = useState({});
  const [fetchCourse, isLoading, error] = useFetching(async () => {
    const courseChapterResponse = await CourseChapterService.retrieve(id);
    const courseResponse = await CourseService.retrieve(
      courseChapterResponse.data.course_id
    );
    setCourse(courseResponse.data);
  });
  const [themeId, setThemeId] = useState(null);
  const { isOpenSettings } = useInterfaceStore();

  useEffect(() => {
    fetchCourse();
  }, [id]);

  return (
    <>
      <LayoutThreeBlocks>
        {isOpenSettings ? (
          <Settings />
        ) : (
          <>
            <CourseList courseChapterId={id} />
          </>
        )}
        <ThemeList
          courseChapterId={id}
          setThemeId={setThemeId}
          color={course.color}
        />
        <CourseChat
          courseName={course.name}
          courseChapterId={id}
          themeId={themeId}
        />
      </LayoutThreeBlocks>
      <LinksBlock className={"absolute bottom-5 right-16"} />
      <ShareLink className={"absolute bottom-5 left-16"} />
    </>
  );
};

export default CourseChatPage;
