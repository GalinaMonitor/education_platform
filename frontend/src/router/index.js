import Login from "../pages/Login";
import Main from "../pages/Main";
import Register from "../pages/Register";
import Subscription from "../pages/Subscription";
import CourseChatPage from "../pages/CourseChatPage";
import Welcome from "../pages/Welcome";
import PrepareRestorePassword from "../pages/PrepareRestorePassword";
import RestorePassword from "../pages/RestorePassword";

export const RouteNames = {
  LOGIN: "/login",
  REGISTER: "/register",
  PREPARE_RESTORE_PASSWORD: "/prepare_restore_password",
  RESTORE_PASSWORD: "/restore_password",
  MAIN: "/",
  WELCOME: "/welcome",
  COURSE_CHAT: "/chat",
  SUBSCRIBE: "/subscribe",
};

export const publicRoutes = [
  { path: RouteNames.LOGIN, component: Login },
  { path: RouteNames.REGISTER, component: Register },
  {
    path: RouteNames.PREPARE_RESTORE_PASSWORD,
    component: PrepareRestorePassword,
  },
  {
    path: `${RouteNames.RESTORE_PASSWORD}/:email/:uuid`,
    component: RestorePassword,
  },
];

export const privateRoutes = [
  { path: RouteNames.MAIN, component: Main },
  { path: RouteNames.WELCOME, component: Welcome },
  { path: `${RouteNames.COURSE_CHAT}/:id`, component: CourseChatPage },
  { path: RouteNames.SUBSCRIBE, component: Subscription },
];
