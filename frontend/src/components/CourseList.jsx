import React, { useEffect, useState } from "react";
import CourseService from "../services/CourseService";
import { useFetching } from "../hooks/useFetching";
import Card from "./UI/Card";
import CourseChapterService from "../services/CourseChapterService";
import CourseCard from "./CourseCard";

const CourseList = ({ courseChapterId = null }) => {
  const [courses, setCourses] = useState([]);
  const [courseChapter, setCourseChapter] = useState({});

  const [fetchCourses, isLoading, error] = useFetching(async () => {
    const response = await CourseService.get();
    setCourses([...response.data]);
  });

  const [fetchCourseChapter] = useFetching(async (courseChapterId) => {
    const response = await CourseChapterService.retrieve(courseChapterId);
    setCourseChapter(response.data);
  });

  useEffect(() => {
    fetchCourses();
    if (courseChapterId) {
      fetchCourseChapter(courseChapterId);
    }
  }, [courseChapterId]);

  return (
    <Card text={"ПРОГРАММЫ ДЛЯ ИЗУЧЕНИЯ"}>
      {courses.map((course, index) => (
        <CourseCard
          key={course.id}
          course={course}
          courseChapter={
            courseChapter && courseChapter.course_id === course.id
              ? courseChapter
              : null
          }
        />
      ))}
    </Card>
  );
};

export default CourseList;
