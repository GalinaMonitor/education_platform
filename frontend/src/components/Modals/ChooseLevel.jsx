import React from 'react';
import {Image, Modal, Row} from "antd";
import {RouteNames} from "../../router";
import {Link, useNavigate} from "react-router-dom";
import BaseLevelSvg from "../UI/BaseLevelSVG";
import MediumLevelSvg from "../UI/MediumLevelSVG";
import ExpertLevelSvg from "../UI/ExpertLevelSVG";

const ChooseLevel = ({isModalOpen, handleCancel, course}) => {
    const navigate = useNavigate();
        const previewImages = [
        {level: "БАЗОВЫЙ", image: BaseLevelSvg},
        {level: "ПРОДВИНУТЫЙ", image: MediumLevelSvg},
        {level: "ЭКСПЕРТ", image: ExpertLevelSvg},
    ]
    return (
        <Modal open={isModalOpen} onCancel={handleCancel} footer={[]} width={'100%'} bodyStyle={{height: '100%'}}>
            <div className={'h-full flex flex-col flex-wrap items-center justify-center'}>
                <Image src={'/lizbet.svg'} width={120} preview={false}/>
                <p className={'text-lg my-5'}>КАКОЙ УРОВЕНЬ ВАС ИНТЕРЕСУЕТ</p>
                <Link to={"/"}><p className={'mb-10'}>ИЗУЧИТЬ СТРУКТУРУ ОБУЧЕНИЯ</p></Link>
                <Row justify={'space-around'} align={'middle'} className={'mb-10 w-screen items justify-around'}>
                    {course ? course.coursechapters.map((item, index) => {
                            let Elem = previewImages[index].image;
                            return <div className={'text-center'} key={item.id} onClick={() => {
                                navigate(`${RouteNames.COURSE_CHAT}/${item.id}`)
                                handleCancel()
                            }}>
                                <Elem color={course.color}/>
                                <p className={'mt-5 font-semibold text-lg'}>{previewImages[index].level}</p>
                            </div>
                        }
                    ) : null}
                </Row>
                <Link to={""} onClick={handleCancel} className={'text-center'}>
                    <Image width={"30px"} src={"/arrow.svg"} preview={false}/>
                    <p className={'mt-5'}>ВЕРНУТЬСЯ НАЗАД</p>
                </Link>
            </div>
        </Modal>
    );
};

export default ChooseLevel;