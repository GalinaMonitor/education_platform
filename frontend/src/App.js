import "./App.css";
import React, { Fragment, useEffect, useState } from "react";
import useUserStore from "./store/useUserStore";
import UserService from "./services/UserService";
import Media from "react-media";
import { BrowserRouter } from "react-router-dom";
import { ConfigProvider, Layout } from "antd";
import AppRouter from "./components/AppRouter";
import MobileBlock from "./components/MobileBlock";
import "./fonts/GraphikLCG-Bold.ttf";
import "./fonts/GraphikLCG-Regular.ttf";
import "./fonts/GraphikLCG-Semibold.ttf";
import "./fonts/GraphikLCG-Medium.ttf";
import Snowfall from "react-snowfall";

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
            colorPrimary: "#FF3300",
            colorInfo: "#FF3300",
            fontFamily: "Semibold",
            borderRadius: 10,
            fontSize: 12,
            controlHeight: 40,
            colorLink: "#FF3300",
            colorLinkActive: "#FF3300",
            colorLinkHover: "#FF3300",
            colorPrimaryHover: "#FF3300",
          },
        }}
      >
        <Layout className={"h-full relative"}>
          <Snowfall style={{ zIndex: 100 }} />
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
