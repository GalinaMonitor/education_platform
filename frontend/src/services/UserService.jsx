import $api from "../api";

export default class UserService {
    static async get_messages(limit, page) {
        return $api.get(`/user/messages/?size=${limit}&page=${page}`)
    }

    static async patch(data) {
        return $api.patch(`/user/`, data)
    }

    static async update_avatar(photo) {
        return $api.post(`/user/avatar/`, photo)
    }
}