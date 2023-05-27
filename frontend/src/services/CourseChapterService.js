import $api from "../api";

export default class CourseChapterService {
    static async retrieve({id}) {
        return $api.get(`/course_chapter/${id}`)
    }

    static async get_messages({id, limit, lastNext = null, lastPrevious = null, theme_id = null}) {
        let request_url = `/course_chapter/${id}/messages?limit=${limit}`
        if (lastNext) {
            request_url += `&after=${lastNext}`
        }
        if (lastPrevious) {
            request_url += `&before=${lastPrevious}`
        }
        if (theme_id) {
            request_url += `&theme=${theme_id}`
        }
        return $api.get(request_url)
    }
}