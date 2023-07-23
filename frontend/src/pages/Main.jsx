import React, { useEffect } from "react";
import CourseList from "../components/CourseList";
import "../App.css";
import BaseChat from "../components/BaseChat";
import { RouteNames } from "../router";
import { useNavigate } from "react-router-dom";
import useUserStore from "../store/useUserStore";
import useInterfaceStore from "../store/useInterfaceStore";
import Settings from "../components/Settings";
import LayoutTwoBlocks from "../components/UI/LayoutTwoBlocks";
import TimeOnPlatformCard from "../components/TimeOnPlatformCard";
import UsersNumber from "../components/UsersNumber";
import ShareLink from "../components/ShareLink";

const Main = () => {
  const { user } = useUserStore();
  const { isOpenSettings } = useInterfaceStore();

  const navigate = useNavigate();
  useEffect(
    () =>
      !user.passed_welcome_page ? navigate(RouteNames.WELCOME) : undefined,
    []
  );
  return (
    <>
      <LayoutTwoBlocks>
        {isOpenSettings ? (
          <>
            <Settings />
            <TimeOnPlatformCard className={"mt-5"} />
          </>
        ) : (
          <CourseList />
        )}
        <BaseChat />
      </LayoutTwoBlocks>
      <UsersNumber className={"absolute bottom-5 right-16"} />
      <ShareLink className={"absolute bottom-5 left-16"} />
    </>
  );
};

export default Main;
