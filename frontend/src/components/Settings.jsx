import React from 'react';
import {Avatar, Input} from "antd";
import useUserStore from "../store";
import {useFetching} from "../hooks/useFetching";
import UserService from "../services/UserService";

const Settings = () => {
    const {user, checkAuth} = useUserStore()

    const [patchUser, isLoading, error] = useFetching(async (data) => {
        const response = await UserService.patch(data)
    })

    const changeFullname = (e) => {
        patchUser({fullname: e.target.value})
        checkAuth()
    }

    const changeCompany = (e) => {
        patchUser({company: e.target.value})
    }

    const changeJob = (e) => {
        patchUser({job: e.target.value})
    }

    return (
        <div>
            <Avatar size={128}/>
            <div className={'mt-3 mb-3'}>
                <p className={'text-xs'} style={{'color': 'grey'}}>{'Имя'}</p>
                <Input defaultValue={user.fullname} onPressEnter={changeFullname}/>
                <p className={'text-xs'} style={{'color': 'grey'}}>{'Компания'}</p>
                <Input defaultValue={user.company} onPressEnter={changeCompany}/>
                <p className={'text-xs'} style={{'color': 'grey'}}>{'Должность'}</p>
                <Input defaultValue={user.job} onPressEnter={changeJob}/>
            </div>
        </div>
    );
};

export default Settings;