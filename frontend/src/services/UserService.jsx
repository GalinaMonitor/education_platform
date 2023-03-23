import $api from "../api";

export default class UserService {
    static async get_messages(limit, page) {
        return $api.get(`/user/messages?size=${limit}&page=${page}`)
    }
}