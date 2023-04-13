import React from 'react';
import {format_datetime} from "../../utils/utils";

const VideoMessage = ({video_id, time = null}) => {
    const player_code = `<iframe class="rounded-xl" style="display:block; width:100%; height: 100%" src="${video_id}" allow="autoplay; fullscreen; picture-in-picture; encrypted-media;" frameborder="0" allowfullscreen></iframe>`
    const video = <div className={"h-96"}  dangerouslySetInnerHTML={{__html: player_code}}/>
    return (
        <div className={`bg-black border-solid border-2 border-orange-500 rounded-2xl relative m-10`}>
            <div className={'top-0 left-0 text-left'}>
                {video}
            </div>
            {time ?
                <div className={'absolute bottom-0 right-2 text-right text-gray-50'}>
                    <p>{format_datetime(time)}</p>
                </div>
                :
                <></>}
        </div>
    );
};

export default VideoMessage;