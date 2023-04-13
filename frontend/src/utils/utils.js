export const format_datetime = (date_str) => {
    const date = new Date(date_str);
    return date.toLocaleString();
}

export const format_time = (time_str) => {
    const time_list = time_str.split(':')
    if (time_list.length === 3) {
        time_list.pop()
    }
    return time_list.join(':')
}