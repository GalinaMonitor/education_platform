import $api from "../api";

export default class CourseChapterService {
  static async retrieve(id) {
    return $api.get(`/course_chapter/${id}`);
  }

  static async get_messages({
    id,
    limit,
    lastNext = null,
    lastPrevious = null,
    themeId = null,
  }) {
    let requestUrl = `/course_chapter/${id}/messages?limit=${limit}`;
    if (lastNext) {
      requestUrl += `&after=${lastNext}`;
    }
    if (lastPrevious) {
      requestUrl += `&before=${lastPrevious}`;
    }
    if (themeId) {
      requestUrl += `&theme_id=${themeId}`;
    }
    return $api.get(requestUrl);
  }

  static async activate({ id }) {
    return $api.post(`/course_chapter/${id}/activate`);
  }
}
