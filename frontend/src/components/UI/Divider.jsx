import React from "react";

const Divider = ({ color = null, selected = false }) => {
  if (!color) {
    color = "#F2F2F2";
  }
  let width;
  if (selected) {
    width = "5px";
  } else {
    width = "1px";
  }
  return (
    <hr
      style={{
        borderTop: `${width} solid ${color}`,
        borderRadius: 5,
        margin: 0,
      }}
    />
  );
};

export default Divider;
