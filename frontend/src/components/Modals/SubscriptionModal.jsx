import React from "react";
import { Card, Image, Modal, Row } from "antd";
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
        <Image src={"/tolya.svg"} width={120} preview={false} />
        <p className={"title-l my-5 text-center"}>
          НА КАКОЙ ПЕРИОД ВЫ ХОТИТЕ
          <br />
          ПРИОБРЕСТИ ДОСТУП К ПЛАТФОРМЕ?
        </p>
        <Row
          justify={"space-around"}
          align={"middle"}
          className={"mb-5 items justify-center"}
        >
          <Card
            style={{ height: "fit-content", borderColor: "#FF7D1F" }}
            className={"text-center p-10 content m-5"}
          >
            <p className={"title-l m-0 brand-color"}>Месячная</p>
            <p className={"m-5"}>
              Доступ ко всем программам и уровням <br />
              на 30 дней
            </p>
            <p className={"title-l m-0"}>2 500 ₽ / 1 польз.</p>
            <p className={"title-l m-0 brand-color"}>
              <strike>5 000 ₽ / 1 польз.</strike>
            </p>
            {/* <Button type={"primary"} className={"big-button"}>*/}
            {/*  Оплатить подписку*/}
            {/* </Button>*/}
          </Card>
          <Card
            style={{ height: "fit-content", borderColor: "#FF7D1F" }}
            className={"text-center p-10 content m-5"}
          >
            <p className={"title-l m-0 brand-color"}>Квартальная</p>
            <p className={"m-5"}>
              Доступ ко всем программам и уровням <br />
              на 90 дней
            </p>
            <p className={"title-l m-0"}>6 000 ₽ / 1 польз.</p>
            <p className={"title-l m-0 brand-color"}>
              <strike>12 000 ₽ / 1 польз.</strike>
            </p>
            {/* <Button type={"primary"} className={"big-button"}>*/}
            {/*  Оплатить подписку*/}
            {/* </Button>*/}
          </Card>
        </Row>
        <Link to={"https://ku-pomogu.ru/for-companies"}>
          {/* <p>БЕЗНАЛИЧНЫЙ РАСЧЁТ</p>*/}
          <p>ОПЛАТИТЬ ПОДПИСКУ</p>
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
