import React, { useState } from "react";
import { Button } from "antd";
import { formatTime } from "../utils/utils";
import VectorSVG from "./UI/VectorSVG";
import TextBlock from "./UI/TextBlock";
import Divider from "./UI/Divider";
import ChooseTimeModal from "./Modals/ChooseTimeModal";
import ChooseLevelModal from "./Modals/ChooseLevelModal";

const CourseCard = ({ course, courseChapter = null }) => {
  const [isTimeModalOpen, setIsTimeModalOpen] = useState(false);
  const [isCourseModalOpen, setIsCourseModalOpen] = useState(false);
  const [courseBase, setCourseBase] = useState(course);
  const [time, setTime] = useState(course.receive_time);

  const showTimeModal = () => {
    setIsTimeModalOpen(true);
  };

  const showCourseModal = () => {
    setIsCourseModalOpen(true);
  };

  const handleCancelTimeModal = async () => {
    setIsTimeModalOpen(false);
  };

  const handleCancelCourseModal = async () => {
    setIsCourseModalOpen(false);
  };

  return (
    <div>
      {courseBase.is_active ? (
        <div key={courseBase.id} className={"mb-5"}>
          <Button
            className={"mr-1.5 p-0 small-button"}
            shape={"round"}
            onClick={() => {
              showCourseModal();
            }}
          >
            {courseChapter && courseChapter.course_id === course.id
              ? courseChapter.name
              : "Уровень"}
          </Button>
          <Button
            className={"p-0 small-button"}
            shape={"round"}
            onClick={() => showTimeModal()}
          >
            {formatTime(time)}
          </Button>
          <div className={"flex flex-row items-center"}>
            <VectorSVG color={courseBase.color} />
            <TextBlock
              className={"ml-1.5"}
              key={courseBase.id}
              bigText={courseBase.name}
            />
          </div>
          <Divider />
        </div>
      ) : (
        <div
          key={courseBase.id}
          className={"mb-5"}
          style={{ cursor: "pointer" }}
          onClick={() => {
            showTimeModal();
            showCourseModal();
          }}
        >
          <Button
            className={"mr-1.5 p-0 small-button"}
            disabled={true}
            shape={"round"}
          >
            Уровень
          </Button>
          <Button
            className={"p-0 small-button"}
            disabled={true}
            shape={"round"}
          >
            {formatTime(time)}
          </Button>
          <div className={"flex flex-row items-center"}>
            <VectorSVG color={courseBase.color} />
            <TextBlock
              className={"ml-1.5"}
              key={courseBase.id}
              bigText={courseBase.name}
            />
          </div>
          <Divider />
        </div>
      )}
      <ChooseTimeModal
        isModalOpen={isTimeModalOpen}
        handleCancel={handleCancelTimeModal}
        modalCourseId={courseBase.id}
        setTime={setTime}
      />
      <ChooseLevelModal
        isModalOpen={isCourseModalOpen}
        course={courseBase}
        handleCancel={handleCancelCourseModal}
        setCourse={setCourseBase}
      />
    </div>
  );
};

export default CourseCard;
