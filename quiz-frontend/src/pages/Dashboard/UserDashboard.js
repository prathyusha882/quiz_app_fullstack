// quiz-frontend/src/pages/Dashboard/UserDashboard.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Line, Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement
);

const UserDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalQuizzes: 0,
    completedQuizzes: 0,
    averageScore: 0,
    totalTime: 0,
    certificates: 0,
    currentStreak: 0,
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [leaderboard, setLeaderboard] = useState([]);
  const [upcomingQuizzes, setUpcomingQuizzes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Simulate API calls - replace with actual API endpoints
      const mockStats = {
        totalQuizzes: 25,
        completedQuizzes: 18,
        averageScore: 78.5,
        totalTime: 1420, // minutes
        certificates: 12,
        currentStreak: 5,
      };

      const mockRecentActivity = [
        {
          id: 1,
          type: 'quiz_completed',
          title: 'React Fundamentals',
          score: 85,
          date: '2024-01-15T10:30:00Z',
          certificate: true,
        },
        {
          id: 2,
          type: 'certificate_earned',
          title: 'JavaScript Advanced',
          score: 92,
          date: '2024-01-14T14:20:00Z',
          certificate: true,
        },
        {
          id: 3,
          type: 'quiz_started',
          title: 'Python Data Structures',
          score: null,
          date: '2024-01-13T09:15:00Z',
          certificate: false,
        },
      ];

      const mockLeaderboard = [
        { rank: 1, username: 'alex_smith', score: 95, quizzes: 20 },
        { rank: 2, username: 'sarah_jones', score: 92, quizzes: 18 },
        { rank: 3, username: 'mike_wilson', score: 89, quizzes: 22 },
        { rank: 4, username: 'emma_davis', score: 87, quizzes: 16 },
        { rank: 5, username: 'john_doe', score: 85, quizzes: 19 },
      ];

      const mockUpcomingQuizzes = [
        {
          id: 1,
          title: 'Advanced React Patterns',
          difficulty: 'Hard',
          duration: 45,
          questions: 25,
          startDate: '2024-01-20T10:00:00Z',
        },
        {
          id: 2,
          title: 'Node.js Backend Development',
          difficulty: 'Medium',
          duration: 30,
          questions: 20,
          startDate: '2024-01-22T14:00:00Z',
        },
      ];

      setStats(mockStats);
      setRecentActivity(mockRecentActivity);
      setLeaderboard(mockLeaderboard);
      setUpcomingQuizzes(mockUpcomingQuizzes);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const progressData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Average Score',
        data: [65, 70, 75, 78, 82, 78.5],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const scoreDistributionData = {
    labels: ['90-100%', '80-89%', '70-79%', '60-69%', '50-59%'],
    datasets: [
      {
        data: [3, 5, 6, 3, 1],
        backgroundColor: [
          '#22c55e',
          '#3b82f6',
          '#f59e0b',
          '#ef4444',
          '#6b7280',
        ],
        borderWidth: 2,
        borderColor: '#ffffff',
      },
    ],
  };

  const quizTypeData = {
    labels: ['React', 'JavaScript', 'Python', 'Node.js', 'Database'],
    datasets: [
      {
        label: 'Quizzes Completed',
        data: [6, 4, 3, 3, 2],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
          'rgba(139, 92, 246, 0.8)',
        ],
        borderWidth: 0,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          padding: 20,
        },
      },
    },
  };

  const lineChartOptions = {
    ...chartOptions,
    scales: {
      y: {
        beginAtZero: true,
        max: 100,
        ticks: {
          callback: function (value) {
            return value + '%';
          },
        },
      },
    },
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded-lg mb-8 w-1/3"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
              {[...Array(4)].map((_, i) => (
                <div key={i} className="h-32 bg-gray-200 rounded-xl"></div>
              ))}
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              <div className="h-80 bg-gray-200 rounded-xl"></div>
              <div className="h-80 bg-gray-200 rounded-xl"></div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold text-secondary-900 mb-2">
            Welcome back, {user?.username}! 👋
          </h1>
          <p className="text-secondary-600 text-lg">
            Here's your learning progress and recent activity
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Total Quizzes</p>
                <p className="text-3xl font-bold text-secondary-900">{stats.totalQuizzes}</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">📚</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-success-600">
                <span className="mr-1">↗</span>
                <span>{stats.completedQuizzes} completed</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Average Score</p>
                <p className="text-3xl font-bold text-secondary-900">{stats.averageScore}%</p>
              </div>
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-success-600">
                <span className="mr-1">↗</span>
                <span>+5.2% this month</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Certificates</p>
                <p className="text-3xl font-bold text-secondary-900">{stats.certificates}</p>
              </div>
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🏆</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-warning-600">
                <span className="mr-1">🔥</span>
                <span>{stats.currentStreak} day streak</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Study Time</p>
                <p className="text-3xl font-bold text-secondary-900">
                  {Math.floor(stats.totalTime / 60)}h {stats.totalTime % 60}m
                </p>
              </div>
              <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">⏱️</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-secondary-600">
                <span className="mr-1">📈</span>
                <span>This month</span>
              </div>
            </div>
          </div>
        </div>

        {/* Charts and Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Progress Chart */}
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              Progress Over Time
            </h3>
            <div className="h-64">
              <Line data={progressData} options={lineChartOptions} />
            </div>
          </div>

          {/* Score Distribution */}
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              Score Distribution
            </h3>
            <div className="h-64">
              <Doughnut data={scoreDistributionData} options={chartOptions} />
            </div>
          </div>
        </div>

        {/* Recent Activity and Leaderboard */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Recent Activity */}
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              Recent Activity
            </h3>
            <div className="space-y-4">
              {recentActivity.map((activity) => (
                <div
                  key={activity.id}
                  className="flex items-center space-x-4 p-4 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors"
                >
                  <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
                    <span className="text-lg">
                      {activity.type === 'quiz_completed' ? '✅' : 
                       activity.type === 'certificate_earned' ? '🏆' : '🚀'}
                    </span>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{activity.title}</p>
                    <p className="text-sm text-secondary-500">
                      {new Date(activity.date).toLocaleDateString()}
                    </p>
                  </div>
                  {activity.score && (
                    <div className="text-right">
                      <p className="font-semibold text-success-600">{activity.score}%</p>
                      {activity.certificate && (
                        <span className="text-xs text-warning-600">Certificate earned</span>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Leaderboard */}
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              Global Leaderboard
            </h3>
            <div className="space-y-3">
              {leaderboard.map((player, index) => (
                <div
                  key={player.rank}
                  className={`flex items-center space-x-4 p-3 rounded-lg ${
                    index === 0 ? 'bg-warning-50 border border-warning-200' :
                    index === 1 ? 'bg-secondary-50 border border-secondary-200' :
                    index === 2 ? 'bg-orange-50 border border-orange-200' :
                    'bg-secondary-50'
                  }`}
                >
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                    index === 0 ? 'bg-warning-500 text-white' :
                    index === 1 ? 'bg-secondary-500 text-white' :
                    index === 2 ? 'bg-orange-500 text-white' :
                    'bg-secondary-200 text-secondary-700'
                  }`}>
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{player.username}</p>
                    <p className="text-sm text-secondary-500">{player.quizzes} quizzes</p>
                  </div>
                  <div className="text-right">
                    <p className="font-semibold text-secondary-900">{player.score}%</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Upcoming Quizzes */}
        <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
          <h3 className="text-lg font-semibold text-secondary-900 mb-4">
            Upcoming Quizzes
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {upcomingQuizzes.map((quiz) => (
              <div
                key={quiz.id}
                className="p-4 border border-gray-200 rounded-lg hover:border-primary-300 hover:shadow-soft transition-all duration-200"
              >
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-secondary-900">{quiz.title}</h4>
                  <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                    quiz.difficulty === 'Hard' ? 'bg-danger-100 text-danger-700' :
                    quiz.difficulty === 'Medium' ? 'bg-warning-100 text-warning-700' :
                    'bg-success-100 text-success-700'
                  }`}>
                    {quiz.difficulty}
                  </span>
                </div>
                <div className="flex items-center space-x-4 text-sm text-secondary-500 mb-3">
                  <span>⏱️ {quiz.duration} min</span>
                  <span>📝 {quiz.questions} questions</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-secondary-500">
                    Starts {new Date(quiz.startDate).toLocaleDateString()}
                  </span>
                  <Link
                    to={`/quizzes/${quiz.id}`}
                    className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
                  >
                    View Details
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserDashboard;
