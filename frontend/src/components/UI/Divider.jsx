import React from 'react';

const Divider = ({color = null}) => {
    if (!color) {
        color = "#d9d9d9"
    }
    return (
        <hr style={{borderTop: `1px solid ${color}`, borderRadius: 5}}/>
    );
};

export default Divider;