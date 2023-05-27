import React from 'react';

const VectorSvg = ({color = ""}) => {
    return (
        <svg width="19" height="19" viewBox="0 0 19 19" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M-1.18065e-06 10.6875L14.4519 10.6875L7.81969 17.3197L9.5 19L19 9.5L9.5 1.07683e-06L7.81969 1.68031L14.4519 8.3125L-9.73018e-07 8.3125L-1.18065e-06 10.6875Z"
                fill={color}/>
        </svg>
    );
};

export default VectorSvg;