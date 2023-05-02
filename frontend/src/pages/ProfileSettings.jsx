import React, {FC} from 'react';
import Navbar from "../components/Navbar";
import {Button, Col, Image, Row} from "antd";
import '../App.css'
import Card from '../components/UI/Card';
import CourseChat from "../components/CourseChat";
import Settings from "../components/Settings";
import {Link} from "react-router-dom";
import {RouteNames} from "../router";
import BaseChat from "../components/BaseChat";

const ProfileSettings: FC = () => {
    return (
        <div>
            <Card className={'ml-10 mt-10 mr-10'} text={''}>
                <Navbar/>
            </Card>
            <Row className={'h-fit'}>

                <Col span={8}>
                    <div className={"relative"}>
                        <div className={"absolute z-10 right-7 top-5"}>
                            <Link to={RouteNames.MAIN}><Image preview={false} src={"/close.svg"}></Image></Link>
                        </div>
                        <Card style={{height: '600px'}} className={'ml-10 mr-2.5 mt-5 mb-5'}
                              text={'ПРОФИЛЬ'}>
                            <Settings/>
                        </Card>
                    </div>
                </Col>
                <Col span={16}>
                    <Card style={{height: '600px'}} className={'mt-5 mr-10 mb-5'} text={'ЧАТ С ПЛАТФОРМОЙ'}>
                        <BaseChat/>
                    </Card>
                </Col>
            </Row>

        </div>
    )
        ;
};

export default ProfileSettings;