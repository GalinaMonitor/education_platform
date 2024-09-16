import React from "react";
import { Button, Card, Image, Modal, Row } from "antd";
import { Link } from "react-router-dom";
import { useMockFetching } from "../../hooks/useMockFetching";

const SubscriptionModal = ({ isModalOpen, handleCancel }) => {
  // TODO Раскомментировать, когда подключим платежную систему
  // const [fetchMonthPayment, isLoadingMonthPayment, errorMonthPayment] =
  //   useFetching(async () => {
  //     const paymentLink = await PaymentService.create_payment_link("month");
  //     window.location = paymentLink.data;
  //   });

  // const [fetchQuarterPayment, isLoadingQuarterPayment, errorQuarterPayment] =
  // useFetching(async () => {
  //   const paymentLink = await PaymentService.create_payment_link("quarter");
  //   window.location = paymentLink.data;
  // });
  const [fetchMonthPayment, isLoadingMonthPayment, errorMonthPayment] =
    useMockFetching(
      "Ошибка на стороне платежной системы. Обратитесь в поддержку."
    );
  const [fetchQuarterPayment, isLoadingQuarterPayment, errorQuarterPayment] =
    useMockFetching(
      "Ошибка на стороне платежной системы. Обратитесь в поддержку."
    );

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
          КАКУЮ ПОДПИСКУ ВЫ
          <br />
          ХОТИТЕ ПОДКЛЮЧИТЬ?
        </p>
        <Row
          justify={"space-around"}
          align={"middle"}
          className={"mb-5 items justify-center"}
        >
          <Card
            style={{ height: "fit-content", borderColor: "#FF7D1F" }}
            className={"text-center content m-5"}
          >
            <p className={"title-l m-0"}>30 дней</p>
            <p className={"title-xl mt-5"}>3 599₽</p>
            <div className={"text-left"}>
              <p className={"text-md m-5"}>
                → Одновременно доступны все
                <br />
                программы на выбор;
              </p>
              <p className={"text-md m-5"}>
                → Видеоуроки поступают по 1<br />
                видеоуроку в день;
              </p>
              <p className={"text-md m-5"}>
                → Тренировочный полигон с<br />
                бесплатным контентом в{" "}
                <a href={"https://t.me/ku_pomogu"}>Telegram-канале</a>.
              </p>
            </div>
            <Button
              loading={isLoadingMonthPayment}
              type={"primary"}
              className={"medium-button mt-5"}
              onClick={fetchMonthPayment}
            >
              Оплатить подписку
            </Button>
          </Card>
          <Card
            style={{ height: "fit-content", borderColor: "#FF7D1F" }}
            className={"text-center content m-5"}
          >
            <p className={"title-l m-0"}>90 дней</p>
            <p className={"text-md m-0 brand-color"}>Экономия ≈ 3 000₽</p>
            <p className={"title-xl m-0"}>7 899₽</p>
            <div className={"text-left"}>
              <p className={"text-md m-5"}>
                → Одновременно доступны все
                <br />
                программы на выбор;
              </p>
              <p className={"text-md m-5"}>
                → Видеоуроки поступают по 1<br />
                видеоуроку в день;
              </p>
              <p className={"text-md m-5"}>
                → Тренировочный полигон с<br />
                бесплатным контентом в{" "}
                <a href={"https://t.me/ku_pomogu"}>Telegram-канале</a>.
              </p>
            </div>
            <Button
              loading={isLoadingQuarterPayment}
              type={"primary"}
              className={"medium-button mt-5"}
              onClick={fetchQuarterPayment}
            >
              Оплатить подписку
            </Button>
          </Card>
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

export default SubscriptionModal;
