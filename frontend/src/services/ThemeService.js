import $api from "../api";

export default class ThemeService {
    static async get(id) {
        return $api.get(`/course_chapter/${id}/themes/`)
    }
}