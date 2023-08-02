import React from "react";
import { Button, Form, Image, Modal, Select } from "antd";
import { timeOptions } from "../../utils/constants";
import { rules } from "../../utils/rules";
import { useFetching } from "../../hooks/useFetching";
import CourseService from "../../services/CourseService";
import { Link } from "react-router-dom";

const ChooseTimeModal = ({ isModalOpen, handleCancel, modalCourseId }) => {
  const [updateReceiveTime, isLoading, error] = useFetching(async (time) => {
    await CourseService.set_receive_time(modalCourseId, time);
  });
  const formRef = React.useRef(null);
  const submit = async (data) => {
    await updateReceiveTime(data.time);
    formRef.current?.resetFields();
    handleCancel();
  };

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
        <Image src={"/tolya.svg"} width={120} preview={false} />
        <p className={"title-l text-center mt-5 mb-10"}>
          ВО СКОЛЬКО ВАМ БУДЕТ УДОБНО ПОЛУЧАТЬ
          <br />
          ОБУЧАЮЩИЙ МАТЕРИАЛ?
        </p>
        <Form
          ref={formRef}
          style={{ width: 460 }}
          onFinish={submit}
          layout="vertical"
        >
          <Form.Item
            label={<p className={"title-l"}>ВРЕМЯ</p>}
            name="time"
            rules={[rules.required("Введите время")]}
          >
            <Select size={"large"} value={"10:00"} options={timeOptions} />
          </Form.Item>
          <Form.Item className={"mb-2"}>
            <Button
              className={"big-button"}
              style={{ width: "100%" }}
              type={"primary"}
              htmlType="submit"
              loading={isLoading}
            >
              <p className={"title-l"}>СТАРТ</p>
            </Button>
          </Form.Item>
        </Form>
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

export default ChooseTimeModal;
