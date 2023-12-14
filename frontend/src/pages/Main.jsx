import React, { useEffect } from "react";
import CourseList from "../components/CourseList";
import "../App.css";
import BaseChat from "../components/BaseChat";
import { useNavigate } from "react-router-dom";
import useUserStore from "../store/useUserStore";
import useInterfaceStore from "../store/useInterfaceStore";
import Settings from "../components/Settings";
import LayoutTwoBlocks from "../components/UI/LayoutTwoBlocks";
import ShareLink from "../components/ShareLink";
import { RouteNames } from "../router";
import { useFetching } from "../hooks/useFetching";
import UserService from "../services/UserService";
import LinksBlock from "../components/UI/LinksBlock";

const Main = () => {
  const { user, checkAuth } = useUserStore();
  const { isOpenSettings } = useInterfaceStore();
  const navigate = useNavigate();

  const [patchUser, userIsLoading, userError] = useFetching(async (data) => {
    await UserService.patch(data);
    await checkAuth();
  });

  useEffect(() => {
    if (!user.passed_welcome_page) {
      patchUser({ passed_welcome_page: true });
      navigate(RouteNames.WELCOME);
    }
  }, []);
  return (
    <>
      <LayoutTwoBlocks>
        {isOpenSettings ? <Settings /> : <CourseList />}
        <BaseChat />
      </LayoutTwoBlocks>
      <LinksBlock className={"absolute bottom-5 right-16"} />
      <ShareLink className={"absolute bottom-5 left-16"} />
    </>
  );
};

export default Main;
