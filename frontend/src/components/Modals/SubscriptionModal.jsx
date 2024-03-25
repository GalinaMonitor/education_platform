import React from "react";
import { Button, Card, Image, Modal, Row } from "antd";
import { Link } from "react-router-dom";
import { useFetching } from "../../hooks/useFetching";
import PaymentService from "../../services/PaymentService";

const SubscriptionModal = ({ isModalOpen, handleCancel }) => {
  const [fetchMonthPayment, isLoadingMonthPayment, errorMonthPayment] =
    useFetching(async () => {
      const paymentLink = await PaymentService.create_payment_link("month");
      window.location = paymentLink.data;
    });

  const [fetchQuarterPayment, isLoadingQuarterPayment, errorQuarterPayment] =
    useFetching(async () => {
      const paymentLink = await PaymentService.create_payment_link("quarter");
      window.location = paymentLink.data;
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
            <p className={"title-l m-0"}>5 000 ₽ / 1 польз.</p>
            <Button
              loading={isLoadingMonthPayment}
              type={"primary"}
              className={"big-button mt-5"}
              onClick={fetchMonthPayment}
            >
              Оплатить подписку
            </Button>
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
            <p className={"title-l m-0"}>12 000 ₽ / 1 польз.</p>
            <Button
              loading={isLoadingQuarterPayment}
              type={"primary"}
              className={"big-button mt-5"}
              onClick={fetchQuarterPayment}
            >
              Оплатить подписку
            </Button>
          </Card>
        </Row>
        <Link to={"https://ku-pomogu.ru/for-companies"}>
          <p>БЕЗНАЛИЧНЫЙ РАСЧЁТ</p>
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
