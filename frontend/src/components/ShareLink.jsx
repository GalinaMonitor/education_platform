import React from 'react';
import {Image} from "antd";
import {Link} from "react-router-dom";

const ShareLink = ({className}) => {
    return (
        <div className={`${className} flex flex-row align-middle justify-around items-center`}>
            <Image src={"/share.svg"} preview={false} width={20}/>
            <Link className={"ml-3"} to={"/"}>РАССКАЗАТЬ О ПЛАТФОРМЕ</Link>
        </div>
    );
};

export default ShareLink;