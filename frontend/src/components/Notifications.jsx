import React from "react";
import { Button, Card, Col, Row } from "antd";
import TelegramIconSVG from "./UI/TelegramIconSVG";
import ShareIconSVG from "./UI/ShareIconSVG";

const notifications = [
  {
    text: "Подписывайтесь на наш ТГ-канал и смотрите еще больше видеоуроков",
    color: "#455A64",
    button_icon: <TelegramIconSVG />,
    button_text: "ПОДПИСАТЬСЯ",
    button_link: "https://t.me/ku_pomogu",
  },
  {
    text: "Оставьте отзыв и получите шаблон инфографики в подарок",
    color: "#FF7D1F",
    button_icon: <ShareIconSVG />,
    button_text: "ОСТАВИТЬ ОТЗЫВ",
    button_link: "https://ku-pomogu.ru/for-users",
  },
];

const Notifications = ({ className }) => {
  return (
    <Row className={`${className}`}>
      {notifications.map((item, index) => (
        <Col span={6} className={"h-full"} key={index}>
          <Card
            className={"relative mr-5"}
            style={{ backgroundColor: item.color }}
          >
            <p className={"title-md mb-2"} style={{ color: "#FFFFFF" }}>
              {item.text}
            </p>
            <Button
              style={{ backgroundColor: "#FFFFFF", color: item.color }}
              className={"medium-button"}
              type="primary"
              icon={item.button_icon}
              href={item.button_link}
            >
              {item.button_text}
            </Button>
          </Card>
        </Col>
      ))}
    </Row>
  );
};

export default Notifications;
