// src/pages/Results/UserResultsPage.js
import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { Doughnut, Bar } from 'react-chartjs-2';
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

const UserResultsPage = () => {
  const { user } = useAuth();
  const location = useLocation();
  const [results, setResults] = useState([]);
  const [selectedResult, setSelectedResult] = useState(null);
  const [certificates, setCertificates] = useState([]);
  const [analytics, setAnalytics] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if we have results from quiz completion
    if (location.state?.results) {
      setSelectedResult(location.state.results);
    }
    fetchResults();
  }, [location.state]);

  const fetchResults = async () => {
    try {
      // Simulate API calls - replace with actual API endpoints
      const mockResults = [
        {
          id: 1,
          quizTitle: 'React Fundamentals',
          score: 85,
          totalQuestions: 20,
          correctAnswers: 17,
          timeTaken: 1800, // seconds
          submittedAt: '2024-01-15T10:30:00Z',
          passed: true,
          certificate: {
            id: 'cert_001',
            issuedAt: '2024-01-15T10:35:00Z',
            downloadUrl: '/certificates/cert_001.pdf'
          }
        },
        {
          id: 2,
          quizTitle: 'JavaScript Advanced',
          score: 92,
          totalQuestions: 25,
          correctAnswers: 23,
          timeTaken: 2100,
          submittedAt: '2024-01-14T14:20:00Z',
          passed: true,
          certificate: {
            id: 'cert_002',
            issuedAt: '2024-01-14T14:25:00Z',
            downloadUrl: '/certificates/cert_002.pdf'
          }
        },
        {
          id: 3,
          quizTitle: 'Python Data Structures',
          score: 68,
          totalQuestions: 15,
          correctAnswers: 10,
          timeTaken: 1200,
          submittedAt: '2024-01-13T09:15:00Z',
          passed: false,
          certificate: null
        }
      ];

      const mockCertificates = mockResults.filter(r => r.certificate).map(r => r.certificate);
      const mockAnalytics = {
        totalQuizzes: 15,
        averageScore: 78.5,
        certificatesEarned: 8,
        studyStreak: 5,
        improvementRate: 12.3
      };

      setResults(mockResults);
      setCertificates(mockCertificates);
      setAnalytics(mockAnalytics);
    } catch (error) {
      console.error('Error fetching results:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    }
    return `${minutes}m ${secs}s`;
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-success-600';
    if (score >= 80) return 'text-primary-600';
    if (score >= 70) return 'text-warning-600';
    return 'text-danger-600';
  };

  const getScoreBadge = (score) => {
    if (score >= 90) return { text: 'Excellent', color: 'bg-success-100 text-success-800' };
    if (score >= 80) return { text: 'Good', color: 'bg-primary-100 text-primary-800' };
    if (score >= 70) return { text: 'Pass', color: 'bg-warning-100 text-warning-800' };
    return { text: 'Needs Improvement', color: 'bg-danger-100 text-danger-800' };
  };

  const performanceData = {
    labels: ['90-100%', '80-89%', '70-79%', '60-69%', 'Below 60%'],
    datasets: [
      {
        data: [3, 5, 4, 2, 1],
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

  const timeAnalysisData = {
    labels: ['React', 'JavaScript', 'Python', 'Node.js', 'Database'],
    datasets: [
      {
        label: 'Average Time (minutes)',
        data: [25, 30, 20, 35, 28],
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

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-50 to-secondary-50 pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded-lg mb-8 w-1/3"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {[...Array(3)].map((_, i) => (
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
            My Results 📊
          </h1>
          <p className="text-secondary-600 text-lg">
            Track your progress and view your certificates
          </p>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Total Quizzes</p>
                <p className="text-3xl font-bold text-secondary-900">{analytics.totalQuizzes}</p>
              </div>
              <div className="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">📚</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Average Score</p>
                <p className="text-3xl font-bold text-secondary-900">{analytics.averageScore}%</p>
              </div>
              <div className="w-12 h-12 bg-success-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🎯</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Certificates</p>
                <p className="text-3xl font-bold text-secondary-900">{analytics.certificatesEarned}</p>
              </div>
              <div className="w-12 h-12 bg-warning-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🏆</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-secondary-500 text-sm font-medium">Study Streak</p>
                <p className="text-3xl font-bold text-secondary-900">{analytics.studyStreak} days</p>
              </div>
              <div className="w-12 h-12 bg-danger-100 rounded-lg flex items-center justify-center">
                <span className="text-2xl">🔥</span>
              </div>
            </div>
          </div>
        </div>

        {/* Recent Results */}
        <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100 mb-8">
          <h2 className="text-2xl font-semibold text-secondary-900 mb-6">Recent Results</h2>
          <div className="space-y-4">
            {results.map((result) => (
              <div
                key={result.id}
                className="flex items-center justify-between p-4 bg-secondary-50 rounded-lg hover:bg-secondary-100 transition-colors cursor-pointer"
                onClick={() => setSelectedResult(result)}
              >
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 rounded-full flex items-center justify-center ${
                    result.passed ? 'bg-success-100' : 'bg-danger-100'
                  }`}>
                    <span className="text-xl">
                      {result.passed ? '✅' : '❌'}
                    </span>
                  </div>
                  <div>
                    <h3 className="font-semibold text-secondary-900">{result.quizTitle}</h3>
                    <p className="text-sm text-secondary-500">
                      {new Date(result.submittedAt).toLocaleDateString()} • {formatTime(result.timeTaken)}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <div className={`text-2xl font-bold ${getScoreColor(result.score)}`}>
                    {result.score}%
                  </div>
                  <div className={`text-xs px-2 py-1 rounded-full ${getScoreBadge(result.score).color}`}>
                    {getScoreBadge(result.score).text}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Analytics Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              Score Distribution
            </h3>
            <div className="h-64">
              <Doughnut data={performanceData} options={chartOptions} />
            </div>
          </div>

          <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100">
            <h3 className="text-lg font-semibold text-secondary-900 mb-4">
              Time Analysis by Topic
            </h3>
            <div className="h-64">
              <Bar data={timeAnalysisData} options={chartOptions} />
            </div>
          </div>
        </div>

        {/* Certificates Section */}
        <div className="bg-white rounded-xl p-6 shadow-soft border border-gray-100 mb-8">
          <h2 className="text-2xl font-semibold text-secondary-900 mb-6">My Certificates</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {certificates.map((cert) => (
              <div
                key={cert.id}
                className="bg-gradient-to-br from-warning-50 to-warning-100 rounded-xl p-6 border border-warning-200 hover:shadow-medium transition-all duration-200"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="w-12 h-12 bg-warning-200 rounded-lg flex items-center justify-center">
                    <span className="text-2xl">🏆</span>
                  </div>
                  <span className="text-xs text-warning-600 font-medium">
                    {new Date(cert.issuedAt).toLocaleDateString()}
                  </span>
                </div>
                <h3 className="font-semibold text-secondary-900 mb-2">
                  Certificate of Completion
                </h3>
                <p className="text-sm text-secondary-600 mb-4">
                  Successfully completed the course requirements
                </p>
                <div className="flex space-x-2">
                  <button className="flex-1 px-3 py-2 bg-warning-600 text-white rounded-lg text-sm font-medium hover:bg-warning-700 transition-colors">
                    Download PDF
                  </button>
                  <button className="px-3 py-2 bg-white text-warning-600 rounded-lg text-sm font-medium hover:bg-warning-50 transition-colors border border-warning-200">
                    Share
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Detailed Result Modal */}
        {selectedResult && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-secondary-900">
                  Quiz Result Details
                </h2>
                <button
                  onClick={() => setSelectedResult(null)}
                  className="text-secondary-400 hover:text-secondary-600"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-6">
                <div className="text-center">
                  <div className={`w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-4 ${
                    selectedResult.passed ? 'bg-success-100' : 'bg-danger-100'
                  }`}>
                    <span className="text-4xl">
                      {selectedResult.passed ? '🎉' : '📝'}
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold text-secondary-900 mb-2">
                    {selectedResult.quizTitle}
                  </h3>
                  <div className={`text-4xl font-bold ${getScoreColor(selectedResult.score)}`}>
                    {selectedResult.score}%
                  </div>
                  <div className={`inline-block px-3 py-1 rounded-full text-sm font-medium mt-2 ${getScoreBadge(selectedResult.score).color}`}>
                    {getScoreBadge(selectedResult.score).text}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="bg-secondary-50 rounded-lg p-4">
                    <p className="text-sm text-secondary-500">Correct Answers</p>
                    <p className="text-2xl font-bold text-secondary-900">
                      {selectedResult.correctAnswers}/{selectedResult.totalQuestions}
                    </p>
                  </div>
                  <div className="bg-secondary-50 rounded-lg p-4">
                    <p className="text-sm text-secondary-500">Time Taken</p>
                    <p className="text-2xl font-bold text-secondary-900">
                      {formatTime(selectedResult.timeTaken)}
                    </p>
                  </div>
                </div>

                <div className="bg-secondary-50 rounded-lg p-4">
                  <p className="text-sm text-secondary-500">Completed On</p>
                  <p className="text-lg font-semibold text-secondary-900">
                    {new Date(selectedResult.submittedAt).toLocaleString()}
                  </p>
                </div>

                {selectedResult.certificate && (
                  <div className="bg-warning-50 rounded-lg p-4 border border-warning-200">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">🏆</span>
                      <div>
                        <p className="font-semibold text-secondary-900">Certificate Earned!</p>
                        <p className="text-sm text-secondary-600">
                          Issued on {new Date(selectedResult.certificate.issuedAt).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    <div className="mt-4 flex space-x-2">
                      <button className="px-4 py-2 bg-warning-600 text-white rounded-lg text-sm font-medium hover:bg-warning-700 transition-colors">
                        Download Certificate
                      </button>
                      <button className="px-4 py-2 bg-white text-warning-600 rounded-lg text-sm font-medium hover:bg-warning-50 transition-colors border border-warning-200">
                        Share Certificate
                      </button>
                    </div>
                  </div>
                )}

                <div className="flex space-x-3 pt-4">
                  <button
                    onClick={() => setSelectedResult(null)}
                    className="flex-1 px-4 py-2 bg-secondary-100 text-secondary-700 rounded-lg font-medium hover:bg-secondary-200 transition-colors"
                  >
                    Close
                  </button>
                  <Link
                    to={`/results/review/${selectedResult.id}`}
                    className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg font-medium hover:bg-primary-700 transition-colors text-center"
                  >
                    Review Answers
                  </Link>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default UserResultsPage;