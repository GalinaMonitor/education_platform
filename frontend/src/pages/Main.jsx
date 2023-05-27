import React, {FC, useEffect} from 'react';
import ProgramList from "../components/CourseList";
import '../App.css'
import BaseChat from "../components/BaseChat";
import {RouteNames} from "../router";
import {useNavigate} from "react-router-dom";
import useUserStore from "../store/useUserStore";
import useInterfaceStore from "../store/useInterfaceStore";
import Settings from "../components/Settings";
import LayoutTwoBlocks from "../components/UI/LayoutTwoBlocks";
import TimeOnPlatformCard from "../components/TimeOnPlatformCard";

const Main: FC = () => {
    const {user} = useUserStore()
    const {isOpenSettings} = useInterfaceStore()

    const navigate = useNavigate();
    useEffect(() => !user.passed_welcome_page ? navigate(RouteNames.WELCOME) : undefined, [])
    return (
        <LayoutTwoBlocks>
            {
                isOpenSettings ?
                    <>
                        <Settings/>
                        <TimeOnPlatformCard className={"mt-5"}/>
                    </> :
                    <ProgramList/>
            }
            <BaseChat/>
        </LayoutTwoBlocks>

    );
};

export default Main;