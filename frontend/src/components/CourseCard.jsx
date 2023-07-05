import React, { useEffect, useState } from "react";
import { Button } from "antd";
import { formatTime } from "../utils/utils";
import VectorSVG from "./UI/VectorSVG";
import TextBlock from "./UI/TextBlock";
import Divider from "./UI/Divider";
import ChooseTimeModal from "./Modals/ChooseTimeModal";
import ChooseLevelModal from "./Modals/ChooseLevelModal";
import { RouteNames } from "../router";
import { useNavigate } from "react-router-dom";
import { useFetching } from "../hooks/useFetching";
import CourseChapterService from "../services/CourseChapterService";

const CourseCard = ({ course, refresh }) => {
  const [isTimeModalOpen, setIsTimeModalOpen] = useState(false);
  const [isCourseModalOpen, setIsCourseModalOpen] = useState(false);
  const [courseChapter, setCourseChapter] = useState(null);
  const navigate = useNavigate();

  const [fetchCourseChapter, isLoading, error] = useFetching(async () => {
    const response = await CourseChapterService.retrieve(
      course.course_chapter_id
    );
    setCourseChapter(response.data);
  });

  useEffect(() => {
    if (course.course_chapter_id) {
      fetchCourseChapter();
    }
  }, [course]);

  const showTimeModal = () => {
    setIsTimeModalOpen(true);
  };

  const showCourseModal = () => {
    setIsCourseModalOpen(true);
  };

  const handleCancelTimeModal = async () => {
    setIsTimeModalOpen(false);
    setTimeout(refresh, 500);
  };

  const handleCancelCourseModal = async () => {
    setIsCourseModalOpen(false);
    setTimeout(refresh, 500);
    navigate(`${RouteNames.MAIN}`);
  };

  return (
    <div>
      <div key={courseChapter?.id} className={"mb-5"}>
        <Button
          className={"mr-1.5 p-0 small-button"}
          disabled={!course.is_active}
          shape={"round"}
          onClick={() => {
            showCourseModal();
          }}
        >
          {courseChapter ? courseChapter.name : "Уровень"}
        </Button>
        <Button
          className={"p-0 small-button"}
          disabled={!course.is_active}
          shape={"round"}
          onClick={() => showTimeModal()}
        >
          {formatTime(course.receive_time)}
        </Button>
        {course.is_active ? (
          <div
            className={"flex flex-row items-center justify-between"}
            style={{ cursor: "pointer" }}
            onClick={() => {
              navigate(`${RouteNames.COURSE_CHAT}/${courseChapter?.id}`);
            }}
          >
            <div className={"flex flex-row items-center"}>
              <VectorSVG color={course.color} />
              <TextBlock
                className={"ml-1.5"}
                key={course.id}
                bigText={course.name}
              />
            </div>

            <p className={"text-md"} style={{ color: course.color }}>
              {courseChapter?.messages_amount
                ? "+" + courseChapter.messages_amount
                : ""}
            </p>
          </div>
        ) : (
          <div
            className={"flex flex-row items-center"}
            style={{ cursor: "pointer" }}
            onClick={() => {
              showTimeModal();
              showCourseModal();
            }}
          >
            <VectorSVG color={course.color} />
            <TextBlock
              className={"ml-1.5"}
              key={course.id}
              bigText={course.name}
            />
          </div>
        )}
        <Divider />
      </div>
      <ChooseTimeModal
        isModalOpen={isTimeModalOpen}
        handleCancel={handleCancelTimeModal}
        modalCourseId={course.id}
      />
      <ChooseLevelModal
        isModalOpen={isCourseModalOpen}
        course={course}
        handleCancel={handleCancelCourseModal}
      />
    </div>
  );
};

export default CourseCard;
