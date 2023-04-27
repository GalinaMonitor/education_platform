import React from 'react';
import {Button, Card, Image} from "antd";
import {Link} from "react-router-dom";
import {RouteNames} from "../router";
import useUserStore from "../store";

const Subscription = () => {
    const {user} = useUserStore()

    return (
        <div className={"h-full"}>
            <Link to={RouteNames.MAIN} className={"absolute flex flex-row items-center top-4 left-4"}>
                <Image width={"30px"} src={"/arrow.svg"} preview={false}/>
                <p className={"ml-2"}>Вернуться назад</p>
            </Link>
            <div className={"flex flex-row justify-center items-center align-middle pl-60 pr-60 m-auto h-full"}>
                <div style={{height: "fit-content"}}>
                    <Image width={"100px"} src={"/lizbet-reversed.svg"} preview={false}/>
                    <p className={"pt-5"}>{`${user.fullname}, на какой период времени`}</p>
                    <p>вы хотите приобрести доступ</p>
                    <p className={"pb-5"}>к платформе Ку.Помогу?</p>
                    <Button>Оплатить с расчетного счета</Button>
                </div>
                <Card style={{height: "fit-content"}} className={"text-center p-10 content m-10"}>
                    <p className={"mb-2"}>1 мес.</p>
                    <p className={"text-3xl m-0 mb-5"}>5 000 р.</p>
                    <Button type={"primary"}>Оплатить подписку</Button>
                </Card>
                <Card style={{height: "fit-content"}} className={"text-center p-10 content"}>
                    <p className={"mb-2"}>3 мес.</p>
                    <p className={"text-3xl m-0 mb-5"}>12 000 р.</p>
                    <Button type={"primary"}>Оплатить подписку</Button>
                </Card>
            </div>
        </div>

    );
};

export default Subscription;