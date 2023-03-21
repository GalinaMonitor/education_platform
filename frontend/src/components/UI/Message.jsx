import React from 'react';

const Message = ({text, type, time, className}) => {

    let content
    if (type === 0) {
        content = <p>{text}</p>
    } else if (type === 1) {
        const player_code = `<iframe src="${text}" allow="autoplay; fullscreen; picture-in-picture; encrypted-media;" frameborder="0" allowfullscreen width="560" height="315"></iframe>`
        content = <div dangerouslySetInnerHTML={{__html: player_code}}/>
    } else {
        content = ''
    }
    return (
        <div className={`${className} border-solid border-2 border-orange-500 rounded-2xl relative p-6 m-10`}>
            <div className={'top-0 left-0 text-left'}>
                {content}
            </div>
            {time ?
                <div className={'absolute bottom-0 right-0 text-right'}>
                    {time}
                </div>
                :
                <></>}
        </div>
    );
};

export default Message;