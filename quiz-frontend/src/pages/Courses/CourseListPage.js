import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';
import './CourseListPage.css';

const CourseListPage = () => {
  const { user } = useAuth();
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get('/api/courses/');
        setCourses(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching courses:', error);
        setError('Failed to load courses');
        setLoading(false);
      }
    };

    fetchCourses();
  }, []);

  if (loading) {
    return (
      <div className="course-list-loading">
        <div className="loading-spinner"></div>
        <p>Loading courses...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="course-list-error">
        <p>{error}</p>
        <button onClick={() => window.location.reload()}>Retry</button>
      </div>
    );
  }

  return (
    <div className="course-list-page">
      <div className="course-list-header">
        <h1>Available Courses</h1>
        <p>Explore our comprehensive learning courses</p>
      </div>

      {courses.length === 0 ? (
        <div className="no-courses">
          <p>No courses available at the moment.</p>
          <p>Check back later for new courses!</p>
        </div>
      ) : (
        <div className="course-grid">
          {courses.map((course) => (
            <div key={course.id} className="course-card">
              <div className="course-image">
                <img 
                  src={course.image || '/default-course.jpg'} 
                  alt={course.title}
                  onError={(e) => {
                    e.target.src = '/default-course.jpg';
                  }}
                />
              </div>
              <div className="course-content">
                <h3>{course.title}</h3>
                <p className="course-description">{course.description}</p>
                <div className="course-meta">
                  <span className="course-duration">
                    {course.lessons_count || 0} lessons
                  </span>
                  <span className="course-level">{course.level}</span>
                </div>
                <div className="course-actions">
                  <Link 
                    to={`/courses/${course.slug}`} 
                    className="course-link"
                  >
                    View Course
                  </Link>
                  {course.is_enrolled ? (
                    <span className="enrolled-badge">Enrolled</span>
                  ) : (
                    <button className="enroll-button">
                      Enroll Now
                    </button>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default CourseListPage; 