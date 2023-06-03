import React from "react";
import { Image, Modal, Row } from "antd";
import { RouteNames } from "../../router";
import { Link, useNavigate } from "react-router-dom";
import BaseLevelSvg from "../UI/BaseLevelSVG";
import MediumLevelSvg from "../UI/MediumLevelSVG";
import ExpertLevelSvg from "../UI/ExpertLevelSVG";
import { useFetching } from "../../hooks/useFetching";
import CourseChapterService from "../../services/CourseChapterService";

const ChooseLevelModal = ({ isModalOpen, handleCancel, course, setCourse }) => {
  const navigate = useNavigate();
  const previewImages = [
    { level: "БАЗОВЫЙ", image: BaseLevelSvg },
    { level: "ПРОДВИНУТЫЙ", image: MediumLevelSvg },
    { level: "ЭКСПЕРТ", image: ExpertLevelSvg },
  ];

  const [updateActiveCourse, isLoading, error] = useFetching(async (id) => {
    await CourseChapterService.activate({ id });
    setCourse({ ...course, is_active: true });
  });

  return (
    <Modal
      open={isModalOpen}
      onCancel={handleCancel}
      footer={[]}
      width={"100%"}
      bodyStyle={{ height: "100%" }}
    >
      <div
        className={"h-full flex flex-col flex-wrap items-center justify-center"}
      >
        <Image src={"/lizbet.svg"} width={120} preview={false} />
        <p className={"text-lg my-5"}>КАКОЙ УРОВЕНЬ ВАС ИНТЕРЕСУЕТ</p>
        <Link to={"/"}>
          <p className={"mb-10"}>ИЗУЧИТЬ СТРУКТУРУ ОБУЧЕНИЯ</p>
        </Link>
        <Row
          justify={"space-around"}
          align={"middle"}
          className={"mb-10 w-screen items justify-around"}
        >
          {course
            ? course.coursechapters.map((item, index) => {
                const Elem = previewImages[index].image;
                return (
                  <div
                    className={"text-center"}
                    key={item.id}
                    onClick={() => {
                      updateActiveCourse(item.id);
                      navigate(`${RouteNames.COURSE_CHAT}/${item.id}`);
                      handleCancel();
                    }}
                  >
                    <Elem color={course.color} />
                    <p className={"mt-5 font-semibold text-lg"}>
                      {previewImages[index].level}
                    </p>
                  </div>
                );
              })
            : null}
        </Row>
        <Link
          to={""}
          onClick={handleCancel}
          className={"text-center absolute bottom-5"}
        >
          <Image width={"30px"} src={"/arrow.svg"} preview={false} />
          <p className={"mt-5"}>ВЕРНУТЬСЯ НАЗАД</p>
        </Link>
      </div>
    </Modal>
  );
};

export default ChooseLevelModal;
