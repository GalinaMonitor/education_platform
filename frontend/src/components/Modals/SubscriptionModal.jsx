import React from "react";
import { Button, Card, Image, Modal, Row } from "antd";
import { Link } from "react-router-dom";

const SubscriptionModal = ({ isModalOpen, handleCancel }) => {
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
        <p className={"text-lg my-5"}>
          НА КАКОЙ ПЕРИОД ВЫ ХОТИТЕ
          <br />
          ПРИОБРЕСТИ ДОСТУП К ПЛАТФОРМЕ?
        </p>
        <Row
          justify={"space-around"}
          align={"middle"}
          className={"mb-5 w-screen items justify-center"}
        >
          <Card
            style={{ height: "fit-content" }}
            className={"text-center p-10 content m-5"}
          >
            <p className={"mb-2"}>1 МЕС.</p>
            <p className={"text-3xl m-0 mb-5"}>5 000 р.</p>
            <Button type={"primary"}>Оплатить подписку</Button>
          </Card>
          <Card
            style={{ height: "fit-content" }}
            className={"text-center p-10 content"}
          >
            <p className={"mb-2"}>3 МЕС.</p>
            <p className={"text-3xl m-0 mb-5"}>12 000 р.</p>
            <Button type={"primary"}>Оплатить подписку</Button>
          </Card>
        </Row>
        <Link to={"https://ku-pomogu.ru/ooo"}>
          <p>БЕЗНАЛИЧНЫЙ РАСЧЁТ</p>
        </Link>
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

export default SubscriptionModal;
