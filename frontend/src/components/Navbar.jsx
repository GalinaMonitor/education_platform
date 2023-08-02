import { Avatar, Button, Row, Image } from "antd";
import React, { useState } from "react";
import TextBlock from "./UI/TextBlock";
import useUserStore from "../store/useUserStore";
import { Link } from "react-router-dom";
import { LogoutOutlined } from "@ant-design/icons";
import DefaultIconSvg from "./UI/DefaultIconSVG";
import useInterfaceStore from "../store/useInterfaceStore";
import Card from "./UI/Card";
import SubscriptionModal from "./Modals/SubscriptionModal";
import { formatDate } from "../utils/utils";

const Navbar = ({ className }) => {
  const { user, logout } = useUserStore();
  const { openCloseSettings } = useInterfaceStore();
  const [isSubscriptionModalOpen, setIsSubscriptionModalOpen] = useState(false);

  const handleCancel = async () => {
    setIsSubscriptionModalOpen(false);
  };

  return (
    <Card className={className}>
      <Row justify={"space-around"} align={"middle"}>
        <div>
          <Image src={"/ku-logo.svg"} preview={false} width={"250px"} />
        </div>
        <Row justify={"space-around"} align={"middle"}>
          <Avatar
            onClick={openCloseSettings}
            icon={<DefaultIconSvg />}
            size={90}
            src={user.avatar}
            style={{ marginRight: "25px", cursor: "pointer" }}
          />
          <TextBlock
            smallText={"ФАМИЛИЯ И ИМЯ"}
            bigText={user.fullname ? user.fullname : user.email}
          />
        </Row>
        <TextBlock smallText={"ПОДПИСКА"} bigText={user.subscription_type} />

        {user.subscription_type === "Нет подписки" ? (
          <TextBlock
            smallText={"ДАТА ОКОНЧАНИЯ ПОДПИСКИ"}
            bigText={"Нет подписки"}
          />
        ) : (
          <TextBlock
            smallText={"ДАТА ОКОНЧАНИЯ ПОДПИСКИ"}
            bigText={formatDate(user.end_of_subscription)}
          />
        )}
        <Row justify={"space-around"} align={"middle"}>
          <Link to={"mailto:support@ku-pomogu.ru"}>
            <Button className={"medium-button mr-5"}>ТЕХ.ПОДДЕРЖКА</Button>
          </Link>
          <Button
            className={"medium-button mr-5"}
            type={"primary"}
            onClick={() => {
              setIsSubscriptionModalOpen(true);
            }}
          >
            ПОДПИСКА
          </Button>
          <Button
            className={"medium-button"}
            type={"primary"}
            icon={<LogoutOutlined />}
            onClick={() => {
              logout();
            }}
          />
        </Row>
      </Row>
      <SubscriptionModal
        isModalOpen={isSubscriptionModalOpen}
        handleCancel={handleCancel}
      />
    </Card>
  );
};

export default Navbar;
