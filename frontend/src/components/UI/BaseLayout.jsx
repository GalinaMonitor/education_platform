import React from 'react';
import Card from "./Card";
import Navbar from "../Navbar";
import {Row} from "antd";

const BaseLayout = ({children}) => {
    return (
        <div className={"h-full"}>
            <div className={'ml-16 mt-16 mr-16 h-1/6'}>
                <Navbar/>
            </div>
            <Row className={'ml-16 mr-16 h-4/6'}>
                {children}
            </Row>
        </div>
    );
};

export default BaseLayout;