import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';

const CourseDetailPage = () => {
  const { slug } = useParams();
  const { user } = useAuth();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const response = await api.get(`/api/courses/${slug}/`);
        setCourse(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching course:', error);
        setLoading(false);
      }
    };

    fetchCourse();
  }, [slug]);

  if (loading) {
    return <div>Loading course...</div>;
  }

  if (!course) {
    return <div>Course not found</div>;
  }

  return (
    <div className="course-detail-page">
      <h1>{course.title}</h1>
      <p>{course.description}</p>
      <div className="course-meta">
        <span>Level: {course.level}</span>
        <span>Lessons: {course.lessons_count || 0}</span>
      </div>
    </div>
  );
};

export default CourseDetailPage; 