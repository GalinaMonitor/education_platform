export const formatDatetime = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString([], {
    hour: "2-digit",
    minute: "2-digit",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
};

export const formatDate = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString([], {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
};

export const formatTime = (timeStr) => {
  if (!timeStr) {
    return "Не выбрано";
  }
  const timeList = timeStr.split(":");
  if (timeList.length === 3) {
    timeList.pop();
  }
  return timeList.join(":");
};
