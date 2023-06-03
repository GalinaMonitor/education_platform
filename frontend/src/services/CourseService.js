import $api from "../api";

export default class CourseService {
  static async get() {
    return $api.get("/course");
  }

  static async retrieve(id) {
    return $api.get(`/course/${id}`);
  }
  static async set_receive_time(id, time) {
    return $api.post(`/course/${id}/change_receive_time`, { time: time });
  }
}
