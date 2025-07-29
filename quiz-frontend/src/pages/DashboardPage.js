import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { fetchData } from '../api/data'; // Use mock or real service
import LoadingSpinner from '../components/LoadingSpinner';
import './DashboardPage.css';

const DashboardPage = () => {
  const { user } = useAuth();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const getData = async () => {
      const token = localStorage.getItem("access_token");

      if (!token) {
        setError("You are not logged in. Please log in to view your dashboard.");
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        const result = await fetchData(token);
        setData(result);
      } catch (err) {
        if (err.message === '401 Unauthorized') {
          setError("Session expired or unauthorized. Please log in again.");
        } else {
          setError("Failed to fetch data. Please try again later.");
        }
        console.error("Error fetching data:", err);
      } finally {
        setLoading(false);
      }
    };

    getData();
  }, []);

  return (
    <div className="dashboard-container">
      <h1>Welcome to your Dashboard{user?.username ? `, ${user.username}` : ''}!</h1>
      <p>This is where you can view and manage your application data.</p>

      <section className="data-section">
        <h2>My Data List</h2>
        {loading ? (
          <LoadingSpinner />
        ) : error ? (
          <p className="error-message">{error}</p>
        ) : data.length > 0 ? (
          <ul className="data-list">
            {data.map((item) => (
              <li key={item.id} className="data-item">
                <h3>{item.title}</h3>
                <p>{item.description}</p>
                <div className="data-actions">
                  <button className="edit-button">Edit</button>
                  <button className="delete-button">Delete</button>
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <p>No data available. Add some data!</p>
        )}
      </section>
    </div>
  );
};

export default DashboardPage;

