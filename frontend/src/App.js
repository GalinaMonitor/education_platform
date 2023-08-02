import "./App.css";
import { ConfigProvider, Layout } from "antd";
import AppRouter from "./components/AppRouter";
import { BrowserRouter } from "react-router-dom";
import React, { useEffect, useState } from "react";
import useUserStore from "./store/useUserStore";
import UserService from "./services/UserService";

const App = () => {
  const { checkAuth, setTimeOnPlatform, timeOnPlatform } = useUserStore();

  const [delay, setDelay] = useState(timeOnPlatform);

  useEffect(() => {
    const timer = setInterval(async () => {
      setDelay(delay + 1);
      setTimeOnPlatform(delay);
      await UserService.patch({ time_on_platform: delay });
    }, 60000);

    return () => {
      clearInterval(timer);
    };
  });

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <BrowserRouter>
      <ConfigProvider
        theme={{
          token: {
            colorPrimary: "#FF7D1F",
            colorInfo: "#FF7D1F",
            fontFamily: "Unbounded",
            borderRadius: 10,
            fontSize: 12,
            controlHeight: 40,
            colorLink: "#FF7D1F",
            colorLinkActive: "#FF7D1F",
            colorLinkHover: "#FF7D1F",
            colorPrimaryHover: "#FF7D1F",
          },
        }}
      >
        <Layout className={"h-full relative"}>
          <AppRouter />
        </Layout>
      </ConfigProvider>
    </BrowserRouter>
  );
};

export default App;
