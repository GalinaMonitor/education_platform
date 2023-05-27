import {Avatar, Button, Row, Image} from 'antd';
import React, {FC} from 'react';
import TextBlock from "./UI/TextBlock";
import useUserStore from "../store";
import {Link} from "react-router-dom";
import {RouteNames} from "../router";
import {LogoutOutlined, UserOutlined} from "@ant-design/icons";
import DefaultIconSvg from "./UI/DefaultIconSVG";

const Navbar: FC = ({className}) => {
    const {user, logout} = useUserStore()

    return (
        <Row className={`${className}`} justify={'space-around'} align={'middle'}>
            <div>
                <Image src={'/ku-logo.svg'} preview={false} width={'250px'}/>
                <p className={"pl-8 mt-0 mb-0 ant-btn-primary"} style={{color: '#FF7D1F'}}>Платформа</p>
            </div>
            <Row justify={'space-around'} align={'middle'}>
                <Avatar icon={<DefaultIconSvg />} size={90} src={user.avatar} style={{marginRight: '25px'}}/>
                <TextBlock small_text={'Фамилия и имя'} big_text={user.fullname ? user.fullname : "Пользователь"}/>
            </Row>
            <TextBlock small_text={'Статус'} big_text={'Изучаю всё'}/>
            {
                user.end_of_subscription ?
                    <TextBlock small_text={'Период подписки'} big_text={user.end_of_subscription}/>
                    :
                    <TextBlock small_text={'Период подписки'} big_text={"Нет подписки"}/>

            }
            <Row justify={'space-around'} align={'middle'}>
                <Link to={RouteNames.SETTINGS} style={{marginRight: '25px'}}><Button>Настройки</Button></Link>
                <Link to={RouteNames.SUBSCRIBE}><Button type={"primary"} style={{marginRight: '25px'}}>Оплатить
                    подписку</Button></Link>
                <Button type={"primary"} icon={<LogoutOutlined/>} onClick={() => {
                    logout()
                }}/>
            </Row>
        </Row>
    );
};

export default Navbar;