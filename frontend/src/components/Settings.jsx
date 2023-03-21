import React from 'react';
import {Avatar, Input} from "antd";

const Settings = () => {
    return (
        <div>
            <Avatar size={128}/>
            <div className={'mt-3 mb-3'}>
                <p className={'text-xs'} style={{'color': 'grey'}}>{'small_text'}</p>
                <Input placeholder="Basic usage"/>
                <p className={'text-xs'} style={{'color': 'grey'}}>{'small_text'}</p>
                <Input placeholder="Basic usage"/>
                <p className={'text-xs'} style={{'color': 'grey'}}>{'small_text'}</p>
                <Input placeholder="Basic usage"/>
            </div>
        </div>
    );
};

export default Settings;