import React from 'react';


const Card = ({children, className, text, style}) => {
    return (
        <div className={`${className} card`} style={style}>
            {
                text ?
                    <p className={'text-gray-400 text-xs mb-3'}>{text}</p>
                    :
                    <></>
            }
            {children}
        </div>
    );
};

export default Card;