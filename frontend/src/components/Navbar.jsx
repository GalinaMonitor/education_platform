import {Avatar, Button, Row, Image} from 'antd';
import React, {FC} from 'react';
import TextBlock from "./UI/TextBlock";
import useUserStore from "../store/useUserStore";
import {Link} from "react-router-dom";
import {RouteNames} from "../router";
import {LogoutOutlined, UserOutlined} from "@ant-design/icons";
import DefaultIconSvg from "./UI/DefaultIconSVG";
import useInterfaceStore from "../store/useInterfaceStore";
import Card from "./UI/Card";

const Navbar: FC = ({className}) => {
    const {user, logout} = useUserStore()
    const {openCloseSettings} = useInterfaceStore()

    return (
        <Card className={className}>
            <Row justify={'space-around'} align={'middle'}>
                <div>
                    <Image src={'/ku-logo.svg'} preview={false} width={'250px'}/>
                </div>
                <Row justify={'space-around'} align={'middle'}>
                    <Avatar icon={<DefaultIconSvg/>} size={90} src={user.avatar} style={{marginRight: '25px'}}/>
                    <TextBlock small_text={'Фамилия и имя'} big_text={user.fullname ? user.fullname : user.email}/>
                </Row>
                <TextBlock small_text={'CТАТУС'} big_text={'Изучаю всё'}/>
                {
                    user.end_of_subscription ?
                        <TextBlock small_text={'ПЕРИОД ПОДПИСКИ И ОБУЧЕНИЯ'} big_text={user.end_of_subscription}/>
                        :
                        <TextBlock small_text={'ПЕРИОД ПОДПИСКИ И ОБУЧЕНИЯ'} big_text={"Нет подписки"}/>

                }
                <Row justify={'space-around'} align={'middle'}>
                    <Button className={"medium-button mr-5"} onClick={openCloseSettings}>Настройки</Button>
                    <Link to={RouteNames.SUBSCRIBE} className={"mr-5"}><Button className={"medium-button"}
                                                                               type={"primary"}>
                        Подписка</Button></Link>
                    <Button type={"primary"} icon={<LogoutOutlined/>} onClick={() => {
                        logout()
                    }}/>
                </Row>
            </Row>
        </Card>
    );
};

export default Navbar;