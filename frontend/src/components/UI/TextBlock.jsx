import React from 'react';

const TextBlock = ({small_text, big_text}) => {
    return (
        <div className={'mt-3 mb-3'}>
            <p className={'text-xs m-0 text-gray-400'}>{small_text}</p>
            <p className={'text-lg m-0'}>{big_text}</p>
        </div>
    );
};

export default TextBlock;