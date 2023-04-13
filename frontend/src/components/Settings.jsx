import React, {useState} from 'react';
import {Avatar, Divider, Input, message, Upload} from "antd";
import useUserStore from "../store";
import {useFetching} from "../hooks/useFetching";
import UserService from "../services/UserService";
import {LoadingOutlined, PlusOutlined} from "@ant-design/icons";

const getBase64 = (img, callback) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => callback(reader.result));
    reader.readAsDataURL(img);
};
const beforeUpload = (file) => {
    const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
    if (!isJpgOrPng) {
        message.error('You can only upload JPG/PNG file!');
    }
    const isLt2M = file.size / 1024 / 1024 < 2;
    if (!isLt2M) {
        message.error('Image must smaller than 2MB!');
    }
    return isJpgOrPng && isLt2M;
};

const Settings = () => {
    const {user, checkAuth} = useUserStore()
    const [loading, setLoading] = useState(false);
    const [imageUrl, setImageUrl] = useState(user.avatar);
    const handleChange = (info) => {
        if (info.file.status === 'uploading') {
            setLoading(true);
            return;
        }
        if (info.file.status === 'done') {
            // Get this url from response in real world.
            getBase64(info.file.originFileObj, (url) => {
                setLoading(false);
                setImageUrl(url);
            });
        }
    };

    const [uploadPhoto, photoIsLoading, photoError] = useFetching(async (photo) => {
        const response = await UserService.update_avatar(photo)
        setImageUrl(response.data)
    })

    const [patchUser, isLoading, error] = useFetching(async (data) => {
        const response = await UserService.patch(data)
    })

    const uploadPhotoFunc = (e) => {
        const formData = new FormData();
        formData.append("photo", e)
        uploadPhoto(formData)
    }

    const changeFullname = (e) => {
        patchUser({fullname: e.target.value})
        checkAuth()
    }

    const changeCompany = (e) => {
        patchUser({company: e.target.value})
    }

    const changeJob = (e) => {
        patchUser({job: e.target.value})
    }

    return (
        <div>
            <Upload
                name="avatar"
                listType="picture-circle"
                showUploadList={false}
                action={uploadPhotoFunc}
                beforeUpload={beforeUpload}
                onChange={handleChange}
            >
                {imageUrl ? (
                    <Avatar src={imageUrl} size={100}/>
                ) : (
                    <div>
                        <div
                            style={{
                                marginTop: 8,
                            }}
                        >
                            Ваше фото
                        </div>
                        {loading ? <LoadingOutlined/> : <PlusOutlined/>}
                    </div>
                )}
            </Upload>
            <div className={'mt-3 mb-3'}>
                <p className={'text-xs m-0.5'} style={{'color': 'grey'}}>Имя</p>
                <Input defaultValue={user.fullname} onPressEnter={changeFullname}/>
                <Divider/>
                <p className={'text-xs m-0.5'} style={{'color': 'grey'}}>Компания</p>
                <Input defaultValue={user.company} onPressEnter={changeCompany}/>
                <Divider/>
                <p className={'text-xs m-0.5'} style={{'color': 'grey'}}>Должность</p>
                <Input defaultValue={user.job} onPressEnter={changeJob}/>
                <Divider/>
            </div>
        </div>
    );
};

export default Settings;