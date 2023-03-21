import {Avatar, Button, Row} from 'antd';
import React, {FC} from 'react';
import TextBlock from "./UI/TextBlock";
import useUserStore from "../store";
import {Link} from "react-router-dom";
import {RouteNames} from "../router";

const Navbar: FC = () => {
    const {user} = useUserStore()

    return (
        <Row justify={'space-around'} align={'middle'}>
            <p>КУ.ПОМОГУ</p>
            <Avatar size={64}/>
            <TextBlock small_text={'Фамилия и имя'} big_text={user.fullname}/>
            <TextBlock small_text={'Статус'} big_text={'Изучаю всё'}/>
            <TextBlock small_text={'Период подписки'} big_text={user.end_of_subscription}/>
            <Link to={RouteNames.SETTINGS}><Button>Настройки</Button></Link>
            <Button>Оплатить подписку</Button>
        </Row>
    );
};

export default Navbar;