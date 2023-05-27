import React from 'react';

const Divider = ({color = null}) => {
    if (!color) {
        color = "#F2F2F2"
    }
    return (
        <hr style={{borderTop: `1px solid ${color}`, borderRadius: 5, margin: 0}}/>
    );
};

export default Divider;