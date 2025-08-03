// src/pages/Dashboard/AdminDashboard.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Line, Bar, Doughnut } from 'react-chartjs-2';
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

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalUsers: 0,
    activeUsers: 0,
    totalQuizzes: 0,
    totalAttempts: 0,
    averageScore: 0,
    certificatesIssued: 0,
  });
  const [recentActivity, setRecentActivity] = useState([]);
  const [topQuizzes, setTopQuizzes] = useState([]);
  const [systemHealth, setSystemHealth] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      // Simulate API calls - replace with actual API endpoints
      const mockStats = {
        totalUsers: 1247,
        activeUsers: 892,
        totalQuizzes: 45,
        totalAttempts: 3420,
        averageScore: 76.8,
        certificatesIssued: 156,
      };

      const mockRecentActivity = [
        {
          id: 1,
          type: 'user_registered',
          user: 'john_doe',
          details: 'New user registration',
          timestamp: '2024-01-15T10:30:00Z',
        },
        {
          id: 2,
          type: 'quiz_completed',
          user: 'sarah_jones',
          details: 'React Fundamentals - 92%',
          timestamp: '2024-01-15T09:45:00Z',
        },
        {
          id: 3,
          type: 'certificate_issued',
          user: 'mike_wilson',
          details: 'JavaScript Advanced Certificate',
          timestamp: '2024-01-15T08:20:00Z',
        },
        {
          id: 4,
          type: 'quiz_created',
          user: 'admin',
          details: 'New quiz: Python Data Structures',
          timestamp: '2024-01-15T07:15:00Z',
        },
      ];

      const mockTopQuizzes = [
        {
          id: 1,
          title: 'React Fundamentals',
          attempts: 245,
          averageScore: 82.5,
          completionRate: 94.2,
        },
        {
          id: 2,
          title: 'JavaScript Basics',
          attempts: 198,
          averageScore: 78.3,
          completionRate: 91.8,
        },
        {
          id: 3,
          title: 'Python Introduction',
          attempts: 156,
          averageScore: 85.7,
          completionRate: 96.1,
        },
        {
          id: 4,
          title: 'Node.js Backend',
          attempts: 134,
          averageScore: 73.9,
          completionRate: 88.5,
        },
      ];

      const mockSystemHealth = {
        serverStatus: 'healthy',
        databaseStatus: 'healthy',
        redisStatus: 'healthy',
        uptime: '99.8%',
        activeConnections: 156,
        memoryUsage: 68,
        cpuUsage: 42,
      };

      setStats(mockStats);
      setRecentActivity(mockRecentActivity);
      setTopQuizzes(mockTopQuizzes);
      setSystemHealth(mockSystemHealth);
    } catch (error) {
      console.error('Error fetching admin data:', error);
    } finally {
      setLoading(false);
    }
  };

  const userGrowthData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'New Users',
        data: [45, 52, 68, 74, 89, 92],
        borderColor: 'rgb(59, 130, 246)',
        backgroundColor: 'rgba(59, 130, 246, 0.1)',
        tension: 0.4,
      },
      {
        label: 'Active Users',
        data: [120, 135, 142, 156, 168, 175],
        borderColor: 'rgb(34, 197, 94)',
        backgroundColor: 'rgba(34, 197, 94, 0.1)',
        tension: 0.4,
      },
    ],
  };

  const quizPerformanceData = {
    labels: ['React', 'JavaScript', 'Python', 'Node.js', 'Database'],
    datasets: [
      {
        label: 'Average Score',
        data: [82.5, 78.3, 85.7, 73.9, 79.2],
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

  const systemUsageData = {
    labels: ['CPU', 'Memory', 'Storage', 'Network'],
    datasets: [
      {
        data: [42, 68, 35, 28],
        backgroundColor: [
          'rgba(59, 130, 246, 0.8)',
          'rgba(34, 197, 94, 0.8)',
          'rgba(245, 158, 11, 0.8)',
          'rgba(239, 68, 68, 0.8)',
        ],
        borderWidth: 2,
        borderColor: '#ffffff',
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
        ticks: {
          callback: function (value) {
            return value;
          },
        },
      },
    },
  };

  const getStatusColor = (status) => {
    return status === 'healthy' ? 'text-success-600' : 'text-danger-600';
  };

  const getStatusIcon = (status) => {
    return status === 'healthy' ? '🟢' : '🔴';
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
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-display font-bold text-secondary-900 mb-2">
            Admin Dashboard 🛠️
          </h1>
          <p className="text-secondary-600 text-lg">
            System overview and analytics for {user?.username}
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Total Users</p>
                <p className="text-3xl font-bold text-secondary-900">{stats.totalUsers.toLocaleString()}</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">👥</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-success-600">
                <span className="mr-1">↗</span>
                <span>{stats.activeUsers} active</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Total Quizzes</p>
                <p className="text-3xl font-bold text-secondary-900">{stats.totalQuizzes}</p>
              </div>
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">📚</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-success-600">
                <span className="mr-1">📊</span>
                <span>{stats.totalAttempts} attempts</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Avg Score</p>
                <p className="text-3xl font-bold text-secondary-900">{stats.averageScore}%</p>
              </div>
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-warning-600">
                <span className="mr-1">📈</span>
                <span>Platform average</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Certificates</p>
                <p className="text-3xl font-bold text-secondary-900">{stats.certificatesIssued}</p>
              </div>
              <div className="w-12 h-12 bg-secondary-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🏆</span>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex items-center text-sm text-secondary-600">
                <span className="mr-1">✨</span>
                <span>Issued this month</span>
              </div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* User Growth */}
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              User Growth
            </h3>
            <div className="h-64">
              <Line data={userGrowthData} options={lineChartOptions} />
            </div>
          </div>

          {/* System Usage */}
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              System Usage
            </h3>
            <div className="h-64">
              <Doughnut data={systemUsageData} options={chartOptions} />
            </div>
          </div>
        </div>

        {/* System Health and Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* System Health */}
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              System Health
            </h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{getStatusIcon(systemHealth.serverStatus)}</span>
                  <span className="font-medium text-secondary-900">Server</span>
                </div>
                <span className={`font-medium ${getStatusColor(systemHealth.serverStatus)}`}>
                  {systemHealth.serverStatus}
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{getStatusIcon(systemHealth.databaseStatus)}</span>
                  <span className="font-medium text-secondary-900">Database</span>
                </div>
                <span className={`font-medium ${getStatusColor(systemHealth.databaseStatus)}`}>
                  {systemHealth.databaseStatus}
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-secondary-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-lg">{getStatusIcon(systemHealth.redisStatus)}</span>
                  <span className="font-medium text-secondary-900">Redis</span>
                </div>
                <span className={`font-medium ${getStatusColor(systemHealth.redisStatus)}`}>
                  {systemHealth.redisStatus}
                </span>
              </div>
              
              <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                <div className="text-center">
                  <p className="text-2xl font-bold text-secondary-900">{systemHealth.uptime}</p>
                  <p className="text-sm text-secondary-500">Uptime</p>
                </div>
                <div className="text-center">
                  <p className="text-2xl font-bold text-secondary-900">{systemHealth.activeConnections}</p>
                  <p className="text-sm text-secondary-500">Active Connections</p>
                </div>
              </div>
            </div>
          </div>

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
                      {activity.type === 'user_registered' ? '👤' : 
                       activity.type === 'quiz_completed' ? '✅' : 
                       activity.type === 'certificate_issued' ? '🏆' : '📝'}
                    </span>
                  </div>
                  <div className="flex-1">
                    <p className="font-medium text-secondary-900">{activity.user}</p>
                    <p className="text-sm text-secondary-500">{activity.details}</p>
                    <p className="text-xs text-secondary-400">
                      {new Date(activity.timestamp).toLocaleString()}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Top Quizzes */}
        <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-secondary-900">
              Top Performing Quizzes
            </h3>
            <Link
              to="/admin/quizzes"
              className="px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors text-sm font-medium"
            >
              View All
            </Link>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-secondary-700">Quiz</th>
                  <th className="text-center py-3 px-4 font-medium text-secondary-700">Attempts</th>
                  <th className="text-center py-3 px-4 font-medium text-secondary-700">Avg Score</th>
                  <th className="text-center py-3 px-4 font-medium text-secondary-700">Completion Rate</th>
                  <th className="text-center py-3 px-4 font-medium text-secondary-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {topQuizzes.map((quiz) => (
                  <tr key={quiz.id} className="border-b border-gray-100 hover:bg-secondary-50">
                    <td className="py-4 px-4">
                      <div>
                        <p className="font-medium text-secondary-900">{quiz.title}</p>
                        <p className="text-sm text-secondary-500">ID: {quiz.id}</p>
                      </div>
                    </td>
                    <td className="py-4 px-4 text-center">
                      <span className="font-medium text-secondary-900">{quiz.attempts}</span>
                    </td>
                    <td className="py-4 px-4 text-center">
                      <span className={`font-medium ${
                        quiz.averageScore >= 80 ? 'text-success-600' :
                        quiz.averageScore >= 70 ? 'text-warning-600' : 'text-danger-600'
                      }`}>
                        {quiz.averageScore}%
                      </span>
                    </td>
                    <td className="py-4 px-4 text-center">
                      <span className="font-medium text-secondary-900">{quiz.completionRate}%</span>
                    </td>
                    <td className="py-4 px-4 text-center">
                      <Link
                        to={`/admin/quizzes/${quiz.id}`}
                        className="text-primary-600 hover:text-primary-700 font-medium text-sm"
                      >
                        View Details
                      </Link>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            to="/admin/quizzes/create"
            className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100 text-center group"
          >
            <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-primary-200 transition-colors">
              <span className="text-2xl">📝</span>
            </div>
            <h4 className="font-semibold text-secondary-900 mb-2">Create Quiz</h4>
            <p className="text-sm text-secondary-500">Add new quiz with questions</p>
          </Link>

          <Link
            to="/admin/users"
            className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100 text-center group"
          >
            <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-success-200 transition-colors">
              <span className="text-2xl">👥</span>
            </div>
            <h4 className="font-semibold text-secondary-900 mb-2">Manage Users</h4>
            <p className="text-sm text-secondary-500">View and manage user accounts</p>
          </Link>

          <Link
            to="/admin/results"
            className="bg-white rounded-xl p-6 shadow-soft hover:shadow-medium transition-all duration-300 border border-gray-100 text-center group"
          >
            <div className="w-16 h-16 bg-warning-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-warning-200 transition-colors">
              <span className="text-2xl">📊</span>
            </div>
            <h4 className="font-semibold text-secondary-900 mb-2">Analytics</h4>
            <p className="text-sm text-secondary-500">Detailed reports and insights</p>
          </Link>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;