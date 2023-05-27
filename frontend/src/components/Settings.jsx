import React, {useState} from 'react';
import {Avatar, message, Upload} from "antd";
import Divider from "./UI/Divider";
import useUserStore from "../store/useUserStore";
import {useFetching} from "../hooks/useFetching";
import UserService from "../services/UserService";
import {LoadingOutlined, PlusOutlined} from "@ant-design/icons";
import Paragraph from "antd/lib/typography/Paragraph";
import EditableStringSvg from "./UI/EditableStringSVG";
import Card from "./UI/Card";

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
            getBase64(info.file.originFileObj, (url) => {
                setLoading(false);
                setImageUrl(url);
            });
        }
    };

    const [uploadPhoto, photoIsLoading, photoError] = useFetching(async (photo) => {
        const response = await UserService.update_avatar(photo)
        setImageUrl(response.data)
        await checkAuth()
    })

    const [patchUser, isLoading, error] = useFetching(async (data) => {
        const response = await UserService.patch(data)
    })

    const uploadPhotoFunc = (e) => {
        const formData = new FormData();
        formData.append("photo", e)
        uploadPhoto(formData)
    }

    const changeFullname = (value) => {
        patchUser({fullname: value})
    }

    const changeCompany = (value) => {
        patchUser({company: value})
    }

    const changeJob = (value) => {
        patchUser({job: value})
    }

    return (
        <Card text={"Профиль"}>
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
                <p className={'text-xs m-1 text-gray-400'}>Имя</p>
                <Paragraph editable={{onChange: changeFullname, icon: <EditableStringSvg/>}}>{user.fullname}</Paragraph>
                <Divider/>
                <p className={'text-xs m-1 text-gray-400'}>Компания</p>
                <Paragraph editable={{onChange: changeCompany, icon: <EditableStringSvg/>}}>{user.company}</Paragraph>
                <Divider/>
                <p className={'text-xs m-1 text-gray-400'}>Должность</p>
                <Paragraph editable={{onChange: changeJob, icon: <EditableStringSvg/>,}}>{user.joby}</Paragraph>
                <Divider/>
            </div>
        </Card>
    );
};

export default Settings;