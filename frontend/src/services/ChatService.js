import $api from "../api";

export default class ChatService {
    static async get(course_chapter_id, limit, page) {
        return $api.get(`/chat/${course_chapter_id}?size=${limit}&page=${page}`)
    }
}