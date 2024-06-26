import { notification } from "antd";

export const success = (text) =>
  notification.success({
    description: text,
    duration: 3,
    placement: "top",
    closeIcon: null,
    style: {
      fontFamily: "Semibold",
      backgroundColor: "#e1ffd6",
    },
  });
export const error = (text) =>
  notification.error({
    description: text,
    duration: 3,
    placement: "top",
    closeIcon: null,
    style: {
      fontFamily: "Semibold",
      backgroundColor: "#ffd6d6",
    },
  });
