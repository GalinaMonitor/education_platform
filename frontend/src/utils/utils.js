export const formatDatetime = (dateStr) => {
  const date = new Date(dateStr);
  return date.toLocaleString();
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
