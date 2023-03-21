import {Avatar, Button, Row} from 'antd';
import React, {FC} from 'react';
import TextBlock from "./UI/TextBlock";
import useUserStore from "../store";

const Navbar: FC = () => {
    const {user} = useUserStore()

    return (
        <Row justify={'space-around'} align={'middle'}>
            <p>КУ.ПОМОГУ</p>
            <Avatar size={64}/>
            <TextBlock small_text={'Фамилия и имя'} big_text={user.fullname}/>
            <TextBlock small_text={'Статус'} big_text={'Изучаю всё'}/>
            <TextBlock small_text={'Период подписки'} big_text={user.end_of_subscription}/>
            <Button>Настройки</Button>
            <Button>Оплатить подписку</Button>
        </Row>
    );
};

export default Navbar;