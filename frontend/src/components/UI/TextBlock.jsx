import React from 'react';

const TextBlock = ({small_text, big_text, className}) => {
    return (
        <div className={`${className} my-3`}>
            <p className={'text-sm my-1.5'}>{small_text}</p>
            <p className={'text-lg m-0'}>{big_text}</p>
        </div>
    );
};

export default TextBlock;