import React, { useEffect, useState } from "react";
import CourseService from "../services/CourseService";
import { useFetching } from "../hooks/useFetching";
import Card from "./UI/Card";
import CourseCard from "./CourseCard";

const CourseList = () => {
  const [courses, setCourses] = useState([]);

  const [fetchCourses, isLoading, error] = useFetching(async () => {
    const response = await CourseService.get();
    setCourses([...response.data]);
  });

  useEffect(() => {
    fetchCourses();
  }, []);

  return (
    <Card text={"ПРОГРАММЫ ДЛЯ ИЗУЧЕНИЯ"} style={{ height: "90%" }}>
      <div style={{ height: "95%", overflow: "auto" }}>
        {courses.map((course, index) => (
          <CourseCard key={course.id} course={course} refresh={fetchCourses} />
        ))}
      </div>
    </Card>
  );
};

export default CourseList;
