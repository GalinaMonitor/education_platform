import "./App.css";
import React, { Fragment, useEffect, useState } from "react";
import useUserStore from "./store/useUserStore";
import UserService from "./services/UserService";
import Media from "react-media";
import { BrowserRouter } from "react-router-dom";
import { ConfigProvider, Layout } from "antd";
import AppRouter from "./components/AppRouter";
import MobileBlock from "./components/MobileBlock";

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
          <Media
            queries={{
              small: "(max-width: 599px)",
              medium: "(min-width: 600px) and (max-width: 1199px)",
              large: "(min-width: 1200px)",
            }}
          >
            {(matches) => (
              <Fragment>
                {(matches.small || matches.medium) && <MobileBlock />}
                {matches.large && <AppRouter />}
              </Fragment>
            )}
          </Media>
        </Layout>
      </ConfigProvider>
    </BrowserRouter>
  );
};

export default App;
