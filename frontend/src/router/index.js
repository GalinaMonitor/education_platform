import Login from "../pages/Login";
import Main from "../pages/Main";
import Register from "../pages/Register";
import ProfileSettings from "../pages/ProfileSettings";
import Subscription from "../pages/Subscription";
import CourseChatPage from "../pages/CourseChatPage";
import Welcome from "../pages/Welcome";

export const RouteNames = {
    LOGIN: '/login',
    REGISTER: '/register',
    MAIN: '/',
    WELCOME: '/welcome',
    COURSE_CHAT: '/chat',
    SETTINGS: '/settings',
    SUBSCRIBE: '/subscribe'
}

export const publicRoutes = [
    {path: RouteNames.LOGIN, component: Login},
    {path: RouteNames.REGISTER, component: Register},
]

export const privateRoutes = [
    {path: RouteNames.MAIN, component: Main},
    {path: RouteNames.WELCOME, component: Welcome},
    {path: `${RouteNames.COURSE_CHAT}/:id`, component: CourseChatPage},
    {path: RouteNames.SETTINGS, component: ProfileSettings},
    {path: RouteNames.SUBSCRIBE, component: Subscription}
]