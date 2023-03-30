import $api from "../api";

export default class CourseChapterService {
    static async get_messages(id, limit, page) {
        return $api.get(`/course_chapter/${id}/messages?size=${limit}&page=${page}`)
    }
}