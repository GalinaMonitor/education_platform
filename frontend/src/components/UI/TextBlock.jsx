import React from 'react';

const TextBlock = ({small_text, big_text}) => {
    return (
        <div className={'mt-3 mb-3'}>
            <p className={'text-xs'} style={{'color': 'grey'}}>{small_text}</p>
            <p>{big_text}</p>
        </div>
    );
};

export default TextBlock;