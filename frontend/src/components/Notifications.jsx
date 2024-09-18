import React from "react";
import { Col, Row } from "antd";
import TelegramIconSVG from "./UI/TelegramIconSVG";
import ShareIconSVG from "./UI/ShareIconSVG";
import Card from "./UI/Card";
import { Link } from "react-router-dom";

const notifications = [
  {
    text: "Подписывайтесь на наш ТГ-канал и смотрите еще больше видеоуроков",
    color: "#687982",
    button_icon: <TelegramIconSVG />,
    button_text: "ПОДПИСАТЬСЯ",
    button_link: "https://t.me/ku_pomogu",
  },
  {
    text: "Оставьте отзыв и получите шаблон инфографики в подарок",
    color: "#FC954A",
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
            className={"relative mr-3"}
            style={{
              backgroundColor: item.color,
              paddingTop: "20px",
              paddingBottom: "20px",
            }}
          >
            <p className={"title-md mb-2"} style={{ color: "#FFFFFF" }}>
              {item.text}
            </p>
            <Link to={item.button_link}>
              <div
                className={"rounded-xl inline-flex items-center py-3 px-5"}
                style={{ backgroundColor: "#FFFFFF", color: item.color }}
              >
                {item.button_icon}
                <p className={"ml-2"}>{item.button_text}</p>
              </div>
            </Link>
          </Card>
        </Col>
      ))}
    </Row>
  );
};

export default Notifications;
