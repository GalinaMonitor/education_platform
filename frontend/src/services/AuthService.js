import $api from "../api";

export default class AuthService {
    static async login(email, password) {
        return $api.post('/auth/token/', {email, password})
    }

    static async register(values) {
        return $api.post('/auth/users/', values)
    }

    static async get_user() {
        return $api.get('/auth/users/me/')
    }

    static async logout() {
        return $api.post('/logout/')
    }
}