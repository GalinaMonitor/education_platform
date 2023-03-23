import $api from "../api";

export default class ChatService {
    static async get(id, limit, page) {
        return $api.get(`/chat/${id}/messages?size=${limit}&page=${page}`)
    }
}