import $api from "../api";

export default class CourseService {
    static async get() {
        return $api.get('/course/')
    }
}