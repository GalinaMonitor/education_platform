import {Avatar, Button, Row, Image} from 'antd';
import React, {FC} from 'react';
import TextBlock from "./UI/TextBlock";
import useUserStore from "../store";
import {Link} from "react-router-dom";
import {RouteNames} from "../router";
import {LogoutOutlined} from "@ant-design/icons";

const Navbar: FC = () => {
    const {user, logout} = useUserStore()

    return (
        <Row justify={'space-around'} align={'middle'}>
            <Image src={'/ku-logo.svg'} preview={false} width={'250px'}/>
            <Row justify={'space-around'} align={'middle'}>
                <Avatar size={64} src={user.avatar} style={{marginRight: '25px'}}/>
                <TextBlock small_text={'Фамилия и имя'} big_text={user.fullname}/>
            </Row>
            <TextBlock small_text={'Статус'} big_text={'Изучаю всё'}/>
            <TextBlock small_text={'Период подписки'} big_text={user.end_of_subscription}/>
            <Row justify={'space-around'} align={'middle'}>
                <Link to={RouteNames.SETTINGS} style={{marginRight: '25px'}}><Button>Настройки</Button></Link>
                <Button style={{marginRight: '25px'}}>Оплатить подписку</Button >
                <Button icon={<LogoutOutlined/>} onClick={() => {logout()}}/>
            </Row>
        </Row>
    );
};

export default Navbar;