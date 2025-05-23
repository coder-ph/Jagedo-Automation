import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Tag, 
  Button, 
  Select, 
  DatePicker, 
  Spin, 
  Alert, 
  Tabs, 
  Progress, 
  Row, 
  Col, 
  Statistic, 
  Space, 
  Tooltip 
} from 'antd';
import { mockStats } from '../mock/mockDashboardData';
import { 
  UserOutlined, 
  ShoppingCartOutlined, 
  CheckCircleOutlined, 
  DollarOutlined,
  BarChartOutlined,
  TeamOutlined,
  MoneyCollectOutlined,
  TrophyOutlined,
  CalendarOutlined,
  CheckCircleFilled,
  UserSwitchOutlined,
  StarFilled,
  StarOutlined,
  ClockCircleOutlined,
  EnvironmentOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  RiseOutlined,
  FallOutlined
} from '@ant-design/icons';
import dayjs from 'dayjs';
import customParseFormat from 'dayjs/plugin/customParseFormat';
import 'dayjs/locale/en';

// Chart.js imports with tree-shaking
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Legend,
  Tooltip as ChartTooltip,
  TimeScale,
  Filler
} from 'chart.js';
import { Line as LineChart, Bar as BarChart, Doughnut as DoughnutChart, Pie as PieChart } from 'react-chartjs-2';
import { useAuth } from '../context/AuthContext';
import api from '../services/api';
import './AdminDashboard.css';

// Extend dayjs with custom parse format
dayjs.extend(customParseFormat);

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  ArcElement,
  Title,
  Legend,
  ChartTooltip,
  TimeScale,
  Filler
);

const { RangePicker } = DatePicker;
const { Option } = Select;

const AdminDashboard = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(mockStats);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [dateRange, setDateRange] = useState([dayjs().subtract(30, 'day'), dayjs()]);
  const [timeRange, setTimeRange] = useState('month');
  const [activeTab, setActiveTab] = useState('overview');
  const [revenuePeriod, setRevenuePeriod] = useState('monthly');
  const [userGrowthPeriod, setUserGrowthPeriod] = useState('yearly');
  const [ratingFilter, setRatingFilter] = useState('all');
  const [locationFilter, setLocationFilter] = useState('all');

  // Tab items configuration
  const tabItems = [
    {
      key: 'overview',
      label: (
        <span>
          <BarChartOutlined /> Overview
        </span>
      ),
    },
    {
      key: 'users',
      label: (
        <span>
          <TeamOutlined /> Users
        </span>
      ),
    },
    {
      key: 'revenue',
      label: (
        <span>
          <MoneyCollectOutlined /> Revenue
        </span>
      ),
      disabled: loading || !stats?.revenue_stats,
    },
    {
      key: 'performance',
      label: (
        <span>
          <TrophyOutlined /> Performance
        </span>
      ),
      disabled: loading || !stats?.platform_stats,
    },
  ];

  // Format currency
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  // Render star rating
  const renderRating = (rating, showNumber = true) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 >= 0.5;
    
    for (let i = 1; i <= 5; i++) {
      if (i <= fullStars) {
        stars.push(<StarFilled key={i} className="text-yellow-400" />);
      } else if (i === fullStars + 1 && hasHalfStar) {
        stars.push(<StarFilled key={i} className="text-yellow-400 opacity-70" />);
      } else {
        stars.push(<StarOutlined key={i} className="text-gray-300" />);
      }
    }
    
    return (
      <div className="flex items-center">
        {stars}
        {showNumber && <span className="ml-1 text-sm text-gray-500">({rating.toFixed(1)})</span>}
      </div>
    );
  };

  // Calculate percentage
  const calculatePercentage = (value, total) => {
    if (!total) return 0;
    return Math.round((value / total) * 100);
  };

  // Get color based on value (for progress bars, etc.)
  const getColorForValue = (value, max = 100) => {
    const percentage = (value / max) * 100;
    if (percentage >= 80) return '#10B981'; // Green
    if (percentage >= 50) return '#F59E0B'; // Yellow
    return '#EF4444'; // Red
  };

  // Format date
  const formatDate = (date, format = 'MMM D, YYYY') => {
    return dayjs(date).format(format);
  };

  const fetchDashboardStats = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // For now, we'll use mock data directly
      // In a real app, you would make an API call here:
      setStats(mockStats);
    } catch (err) {
      console.error('Error fetching dashboard stats:', err);
      setError('Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardStats();
  }, [dateRange, timeRange]);

  const handleDateRangeChange = (dates) => {
    if (dates && dates[0] && dates[1]) {
      setDateRange([dates[0], dates[1]]);
    }
  };

  const handleTimeRangeChange = (value) => {
    setTimeRange(value);
    let startDate, endDate = dayjs().endOf('day');
    
    switch (value) {
      case 'today':
        startDate = dayjs().startOf('day');
        break;
      case 'week':
        startDate = dayjs().startOf('week');
        break;
      case 'month':
        startDate = dayjs().startOf('month');
        break;
      case 'year':
        startDate = dayjs().startOf('year');
        break;
      default:
        startDate = dayjs().startOf('month');
    }
    
    setDateRange([startDate, endDate]);
  };

  if (loading || !stats) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Spin size="large" tip="Loading dashboard data..." />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <Alert
          message="Error Loading Dashboard"
          description={error}
          type="error"
          showIcon
          action={
            <Button type="primary" onClick={() => window.location.reload()}>
              Retry
            </Button>
          }
        />
      </div>
    );
  }

  const {
    user_stats = {},
    job_stats = {},
    revenue_stats = {},
    category_distribution = [],
    recent_activities = []
  } = stats || {};

  // Prepare data for charts
  const jobStatusData = {
    labels: ['Active', 'Completed', 'Cancelled'],
    datasets: [
      {
        data: [
          job_stats.active_jobs || 0,
          job_stats.completed_jobs || 0,
          job_stats.cancelled_jobs || 0
        ],
        backgroundColor: ['#1890ff', '#52c41a', '#f5222d'],
      },
    ],
  };

  const categoryData = {
    labels: category_distribution.map(item => item.category_name),
    datasets: [
      {
        data: category_distribution.map(item => item.job_count),
        backgroundColor: [
          '#1890ff', '#52c41a', '#f5222d', '#faad14', '#722ed1',
          '#13c2c2', '#eb2f96', '#fa8c16', '#a0d911', '#fa541c'
        ],
      },
    ],
  };

  const revenueChartData = {
    labels: revenue_stats.monthly_revenue?.map(item => item.month) || [],
    datasets: [
      {
        label: 'Monthly Revenue',
        data: revenue_stats.monthly_revenue?.map(item => item.amount) || [],
        borderColor: '#1890ff',
        backgroundColor: 'rgba(24, 144, 255, 0.2)',
        fill: true,
      },
    ],
  };

  // Process user growth data based on selected period
  const getUserGrowthData = () => {
    if (!user_stats) return { labels: [], datasets: [] };
    
    let labels = [];
    let data = [];
    
    switch(userGrowthPeriod) {
      case 'yearly':
        labels = user_stats.yearly_signups?.map(item => item.year) || [];
        data = user_stats.yearly_signups?.map(item => item.count) || [];
        break;
      case 'quarterly':
        labels = user_stats.quarterly_signups?.map(item => `Q${item.quarter} ${item.year}`) || [];
        data = user_stats.quarterly_signups?.map(item => item.count) || [];
        break;
      case 'monthly':
      default:
        labels = user_stats.monthly_signups?.map(item => item.month) || [];
        data = user_stats.monthly_signups?.map(item => item.count) || [];
    }
    
    return {
      labels,
      datasets: [
        {
          label: 'New Users',
          data,
          borderColor: '#52c41a',
          backgroundColor: 'rgba(82, 196, 26, 0.2)',
          fill: true,
          tension: 0.4,
        },
      ],
    };
  };
  
  const userGrowthData = getUserGrowthData();

  const userGrowthOptions = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    plugins: {
      legend: {
        display: false,
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: function(context) {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            if (context.parsed.y !== null) {
              label += context.parsed.y.toLocaleString();
            }
            return label;
          }
        }
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          precision: 0
        },
        title: {
          display: true,
          text: 'Number of Users',
          font: {
            weight: 'bold'
          }
        }
      },
      x: {
        title: {
          display: true,
          text: userGrowthPeriod === 'yearly' ? 'Year' : 
                userGrowthPeriod === 'quarterly' ? 'Quarter' : 'Month',
          font: {
            weight: 'bold'
          }
        },
        grid: {
          display: false
        }
      }
    },
    animation: {
      duration: 1000,
      easing: 'easeInOutQuart'
    }
  };

  const columns = [
    {
      title: 'Activity',
      dataIndex: 'activity',
      key: 'activity',
    },
    {
      title: 'User',
      dataIndex: 'user_name',
      key: 'user_name',
    },
    {
      title: 'Date',
      dataIndex: 'created_at',
      key: 'created_at',
      render: (date) => dayjs(date).format('MMM D, YYYY h:mm A'),
    },
  ];

  // Calculate derived statistics
  const totalUsers = stats.user_stats?.total_users || 0;
  const activeJobs = stats.job_stats?.active_jobs || 0;
  const completedJobs = stats.job_stats?.completed_jobs || 0;
  const totalRevenue = stats.revenue_stats?.total_revenue || 0;
  const revenueGrowth = stats.revenue_stats?.revenue_growth || 0;
  const avgRating = stats.platform_stats?.avg_rating || 0;
  const jobSuccessRate = stats.platform_stats?.job_success_rate || 0;
  const avgResponseTime = stats.platform_stats?.avg_response_time || 'N/A';

  return (
    <div className="admin-dashboard bg-gray-50 min-h-screen p-4 md:p-6">
      {/* Header */}
      <div className="mb-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-6">
          <div>
            <h1 className="text-2xl md:text-3xl font-bold text-gray-800">Dashboard Overview</h1>
            <p className="text-gray-500">Welcome back, {user?.name || 'Admin'}</p>
          </div>
          <div className="flex flex-col sm:flex-row gap-3">
            <Select 
              value={timeRange} 
              onChange={handleTimeRangeChange}
              className="w-full sm:w-40"
              suffixIcon={<CalendarOutlined />}
            >
              <Option value="today">Today</Option>
              <Option value="week">This Week</Option>
              <Option value="month">This Month</Option>
              <Option value="quarter">This Quarter</Option>
              <Option value="year">This Year</Option>
              <Option value="custom">Custom Range</Option>
            </Select>
            <RangePicker
              value={dateRange}
              onChange={handleDateRangeChange}
              className="w-full sm:w-64"
              disabled={timeRange !== 'custom'}
              format="MMM D, YYYY"
              allowClear={false}
            />
          </div>
        </div>
        
        {/* Stats Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          {/* Total Users */}
          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-blue-50 text-blue-500 mr-4">
                <UserOutlined className="text-xl" />
              </div>
              <div>
                <div className="text-gray-500 text-sm font-medium">Total Users</div>
                <div className="text-2xl font-bold">{totalUsers.toLocaleString()}</div>
                <div className="text-xs text-gray-500">
                  <span className="text-green-500">+{stats.user_stats?.new_users_this_month || 0} this month</span>
                </div>
              </div>
            </div>
          </Card>
          
          {/* Active Jobs */}
          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-purple-50 text-purple-500 mr-4">
                <ShoppingCartOutlined className="text-xl" />
              </div>
              <div>
                <div className="text-gray-500 text-sm font-medium">Active Jobs</div>
                <div className="text-2xl font-bold">{activeJobs.toLocaleString()}</div>
                <div className="text-xs text-gray-500">
                  <span className="text-green-500">+{stats.job_stats?.new_jobs_this_week || 0} new this week</span>
                </div>
              </div>
            </div>
          </Card>
          
          {/* Completed Jobs */}
          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-green-50 text-green-500 mr-4">
                <CheckCircleOutlined className="text-xl" />
              </div>
              <div>
                <div className="text-gray-500 text-sm font-medium">Completed Jobs</div>
                <div className="text-2xl font-bold">{completedJobs.toLocaleString()}</div>
                <div className="text-xs text-gray-500">
                  <span className="text-green-500">+{stats.job_stats?.completed_this_month || 0} this month</span>
                </div>
              </div>
            </div>
          </Card>
          
          {/* Total Revenue */}
          <Card className="shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center">
              <div className="p-3 rounded-lg bg-yellow-50 text-yellow-500 mr-4">
                <DollarOutlined className="text-xl" />
              </div>
              <div>
                <div className="text-gray-500 text-sm font-medium">Total Revenue</div>
                <div className="text-2xl font-bold">{formatCurrency(totalRevenue)}</div>
                <div className="text-xs">
                  <span className={revenueGrowth >= 0 ? 'text-green-500' : 'text-red-500'}>
                    {revenueGrowth >= 0 ? '↑' : '↓'} {Math.abs(revenueGrowth)}% vs last period
                  </span>
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
      
      {/* Main Content */}
      <div className="bg-white rounded-lg shadow-sm p-4 md:p-6">
        {/* Tabs */}
        <Tabs 
          activeKey={activeTab}
          onChange={setActiveTab}
          items={tabItems}
          className="mb-6"
        />
        
        {/* Tab Content */}
        <div className="chart-container">
          <div className="mb-4 flex justify-end">
            <Select 
              value={userGrowthPeriod}
              onChange={setUserGrowthPeriod}
              style={{ width: 150 }}
              className="ml-2"
            >
              <Option value="yearly">Yearly</Option>
              <Option value="quarterly">Quarterly</Option>
              <Option value="monthly">Monthly</Option>
            </Select>
          </div>
          <div className="h-80">
            <LineChart 
              data={userGrowthData} 
              options={userGrowthOptions} 
              redraw
            />
          </div>
        </div>
        <div className="space-y-6">
          {activeTab === 'overview' && (
            <div className="space-y-6">
              {/* Platform Performance */}
              <Card title="Platform Performance" className="mb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <div className="p-4 border rounded-lg">
                    <div className="text-gray-500 text-sm mb-1">Average Rating</div>
                    <div className="flex items-center">
                      {renderRating(avgRating)}
                      <span className="ml-2 text-gray-700 font-medium">{avgRating.toFixed(1)}/5.0</span>
                    </div>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <div className="text-gray-500 text-sm mb-1">Job Success Rate</div>
                    <div className="text-2xl font-bold text-gray-800">{jobSuccessRate}%</div>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <div className="text-gray-500 text-sm mb-1">Avg. Response Time</div>
                    <div className="text-2xl font-bold text-gray-800">{avgResponseTime}</div>
                  </div>
                  <div className="p-4 border rounded-lg">
                    <div className="text-gray-500 text-sm mb-1">Active Professionals</div>
                    <div className="text-2xl font-bold text-gray-800">
                      {stats.platform_stats?.active_professionals?.toLocaleString() || '0'}
                    </div>
                  </div>
                </div>
              </Card>
              
              {/* Recent Activities */}
              <Card title="Recent Activities" className="mb-6">
                <div className="space-y-4">
                  {stats.recent_activities?.slice(0, 5).map(activity => (
                    <div key={activity.id} className="flex items-start pb-4 border-b border-gray-100 last:border-0 last:pb-0">
                      <div className="p-2 bg-blue-50 rounded-full text-blue-500 mr-3">
                        {activity.type === 'job_completed' && <CheckCircleFilled />}
                        {activity.type === 'payment' && <DollarOutlined />}
                        {activity.type === 'subscription' && <UserSwitchOutlined />}
                        {activity.type === 'review' && <StarFilled />}
                        {!['job_completed', 'payment', 'subscription', 'review'].includes(activity.type) && <ClockCircleOutlined />}
                      </div>
                      <div className="flex-1">
                        <div className="flex justify-between items-start">
                          <div className="font-medium">{activity.activity}</div>
                          <div className="text-xs text-gray-400">
                            {formatDate(activity.created_at, 'MMM D, h:mm A')}
                          </div>
                        </div>
                        <div className="text-sm text-gray-600">
                          {activity.user_name} 
                          <Tag color={activity.user_type === 'Professional' ? 'blue' : 'green'} className="ml-2">
                            {activity.user_type}
                          </Tag>
                        </div>
                        {activity.amount && (
                          <div className="mt-1 text-sm font-medium">
                            {formatCurrency(activity.amount)}
                          </div>
                        )}
                        {activity.rating && (
                          <div className="mt-1">
                            {renderRating(activity.rating, false)}
                            {activity.review && (
                              <div className="mt-1 text-sm text-gray-600 italic">"{activity.review}"</div>
                            )}
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </Card>
            </div>
          )}
          
          {activeTab === 'users' && (
            <div className="space-y-6">
              {/* User Growth */}
              <Card title="User Growth" className="mb-6">
                <div className="h-80">
                  <LineChart 
                    data={{
                      labels: stats.user_stats.monthly_signups.map(item => item.month),
                      datasets: [
                        {
                          label: 'Total Signups',
                          data: stats.user_stats.monthly_signups.map(item => item.count),
                          borderColor: '#4f46e5',
                          backgroundColor: 'rgba(79, 70, 229, 0.1)',
                          tension: 0.3,
                          fill: true
                        },
                        {
                          label: 'Clients',
                          data: stats.user_stats.monthly_signups.map(item => item.clients),
                          borderColor: '#10b981',
                          borderDash: [5, 5],
                          backgroundColor: 'transparent',
                          tension: 0.3
                        },
                        {
                          label: 'Professionals',
                          data: stats.user_stats.monthly_signups.map(item => item.professionals),
                          borderColor: '#f59e0b',
                          borderDash: [5, 5],
                          backgroundColor: 'transparent',
                          tension: 0.3
                        }
                      ]
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          position: 'top',
                        },
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          ticks: {
                            precision: 0
                          }
                        }
                      }
                    }}
                  />
                </div>
              </Card>
              
              {/* Top Clients */}
              <Card title="Top Clients by Jobs Posted" className="mb-6">
                <Table 
                  dataSource={stats.user_stats.top_clients}
                  rowKey="id"
                  pagination={false}
                  columns={[
                    {
                      title: 'Client',
                      dataIndex: 'name',
                      key: 'name',
                      render: (text) => <span className="font-medium">{text}</span>
                    },
                    {
                      title: 'Jobs Posted',
                      dataIndex: 'jobs_posted',
                      key: 'jobs_posted',
                      render: (value) => (
                        <div className="flex items-center">
                          <div className="w-16">{value}</div>
                          <div className="flex-1 ml-2">
                            <div 
                              className="h-2 bg-blue-100 rounded-full overflow-hidden"
                            >
                              <div 
                                className="h-full bg-blue-500"
                                style={{ 
                                  width: `${(value / Math.max(...stats.user_stats.top_clients.map(c => c.jobs_posted))) * 100}%` 
                                }}
                              />
                            </div>
                          </div>
                        </div>
                      ),
                      sorter: (a, b) => a.jobs_posted - b.jobs_posted,
                      defaultSortOrder: 'descend'
                    },
                    {
                      title: 'Total Spent',
                      dataIndex: 'total_spent',
                      key: 'total_spent',
                      render: (value) => formatCurrency(value),
                      sorter: (a, b) => a.total_spent - b.total_spent,
                    },
                  ]}
                />
              </Card>
            </div>
          )}
          
          {activeTab === 'revenue' && (
            <div className="space-y-6">
              {loading ? (
                <div className="flex justify-center items-center h-64">
                  <Spin size="large" tip="Loading revenue data..." />
                </div>
              ) : error ? (
                <Alert
                  message="Error loading revenue data"
                  description={error}
                  type="error"
                  showIcon
                  action={
                    <Button type="primary" onClick={() => window.location.reload()}>
                      Retry
                    </Button>
                  }
                />
              ) : stats?.revenue_stats ? (
                <>
                  <Card title="Revenue Overview" className="mb-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                      <div className="p-4 border rounded-lg">
                        <div className="text-gray-500 text-sm mb-1">This Month</div>
                        <div className="text-2xl font-bold">
                          {stats.revenue_stats.revenue_this_month ? 
                            formatCurrency(stats.revenue_stats.revenue_this_month) : 'N/A'}
                        </div>
                        <div className="text-xs mt-1">
                          {stats.revenue_stats.revenue_growth !== undefined && (
                            <span className={stats.revenue_stats.revenue_growth >= 0 ? 'text-green-500' : 'text-red-500'}>
                              {stats.revenue_stats.revenue_growth >= 0 ? '↑' : '↓'} 
                              {Math.abs(stats.revenue_stats.revenue_growth)}% vs last month
                            </span>
                          )}
                        </div>
                      </div>
                      <div className="p-4 border rounded-lg">
                        <div className="text-gray-500 text-sm mb-1">This Quarter</div>
                        <div className="text-2xl font-bold">
                          {stats.revenue_stats.revenue_this_quarter ? 
                            formatCurrency(stats.revenue_stats.revenue_this_quarter) : 'N/A'}
                        </div>
                      </div>
                      <div className="p-4 border rounded-lg">
                        <div className="text-gray-500 text-sm mb-1">This Year</div>
                        <div className="text-2xl font-bold">
                          {stats.revenue_stats.revenue_this_year ? 
                            formatCurrency(stats.revenue_stats.revenue_this_year) : 'N/A'}
                        </div>
                      </div>
                    </div>
                
                    <div className="h-80">
                      <BarChart 
                        data={{
                          labels: stats.revenue_stats.quarterly_revenue?.map(item => `Q${item.quarter}`) || [],
                          datasets: [
                            {
                              label: 'Revenue',
                              data: stats.revenue_stats.quarterly_revenue?.map(item => item.amount) || [],
                              backgroundColor: 'rgba(79, 70, 229, 0.7)',
                            },
                            {
                              label: 'Growth %',
                              data: stats.revenue_stats.quarterly_revenue?.map(item => (item.growth || 0) * 100) || [],
                              backgroundColor: 'rgba(16, 185, 129, 0.7)',
                              yAxisID: 'y1',
                              type: 'line',
                              borderColor: 'rgba(16, 185, 129, 1)',
                              borderWidth: 2,
                              pointBackgroundColor: 'rgba(16, 185, 129, 1)',
                              pointBorderColor: '#fff',
                              pointHoverRadius: 5,
                              pointHoverBackgroundColor: 'rgba(16, 185, 129, 1)',
                              pointHoverBorderColor: '#fff',
                              pointHitRadius: 10,
                              pointBorderWidth: 2,
                            }
                          ]
                        }}
                        options={{
                          responsive: true,
                          maintainAspectRatio: false,
                          interaction: {
                            mode: 'index',
                            intersect: false,
                          },
                          plugins: {
                            legend: {
                              position: 'top',
                            },
                            tooltip: {
                              callbacks: {
                                label: function(context) {
                                  let label = context.dataset.label || '';
                                  if (label) {
                                    label += ': ';
                                  }
                                  if (context.parsed.y !== null) {
                                    if (context.dataset.label === 'Growth %') {
                                      label += (context.parsed.y / 100).toFixed(2) + '%';
                                    } else {
                                      label += formatCurrency(context.parsed.y);
                                    }
                                  }
                                  return label;
                                }
                              }
                            }
                          },
                          scales: {
                            y: {
                              type: 'linear',
                              display: true,
                              position: 'left',
                              title: {
                                display: true,
                                text: 'Revenue (KSh)'
                              },
                              grid: {
                                drawOnChartArea: false
                              }
                            },
                            y1: {
                              type: 'linear',
                              display: true,
                              position: 'right',
                              title: {
                                display: true,
                                text: 'Growth %'
                              },
                              grid: {
                                drawOnChartArea: false
                              },
                              min: 0,
                              max: 100,
                              ticks: {
                                callback: function(value) {
                                  return value + '%';
                                }
                              }
                            },
                            x: {
                              grid: {
                                display: false
                              }
                            }
                          }
                        }}
                      />
                    </div>
                  </Card>
                </>
              ) : (
                <Alert
                  message="No revenue data available"
                  description="There is no revenue data to display at the moment."
                  type="info"
                  showIcon
                />
              )}
              
              {/* Revenue by Region */}
              <Card title="Revenue by Region" className="mb-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="h-80">
                    <Doughnut
                      data={{
                        labels: stats.revenue_stats.revenue_by_region.map(item => item.region),
                        datasets: [{
                          data: stats.revenue_stats.revenue_by_region.map(item => item.amount),
                          backgroundColor: [
                            'rgba(79, 70, 229, 0.7)',
                            'rgba(99, 102, 241, 0.7)',
                            'rgba(129, 140, 248, 0.7)',
                            'rgba(165, 180, 252, 0.7)'
                          ],
                          borderWidth: 1,
                          hoverOffset: 10
                        }]
                      }}
                      options={{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                          legend: {
                            position: 'right',
                          },
                          tooltip: {
                            callbacks: {
                              label: function(context) {
                                const label = context.label || '';
                                const value = context.raw || 0;
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = Math.round((value / total) * 100);
                                return `${label}: ${formatCurrency(value)} (${percentage}%)`;
                              }
                            }
                          }
                        },
                        cutout: '70%'
                      }}
                    />
                  </div>
                  <div>
                    <div className="space-y-4">
                      {stats.revenue_stats.revenue_by_region.map((region, index) => {
                        const percentage = calculatePercentage(
                          region.amount,
                          stats.revenue_stats.revenue_by_region.reduce((sum, r) => sum + r.amount, 0)
                        );
                        
                        return (
                          <div key={index}>
                            <div className="flex justify-between text-sm mb-1">
                              <div className="font-medium">{region.region}</div>
                              <div>{formatCurrency(region.amount)}</div>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="h-full rounded-full" 
                                style={{
                                  width: `${percentage}%`,
                                  backgroundColor: [
                                    '#4f46e5',
                                    '#6366f1',
                                    '#818cf8',
                                    '#a5b4fc'
                                  ][index % 4]
                                }}
                              />
                            </div>
                            <div className="text-xs text-gray-500 mt-1">{percentage}% of total revenue</div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                </div>
              </Card>
            </div>
          )}
          
          {activeTab === 'performance' && (
            <div className="space-y-6">
              {/* Top Performers */}
              <Card title="Top Performing Professionals" className="mb-6">
                <Table 
                  dataSource={stats.professional_stats.top_performers}
                  rowKey="id"
                  pagination={false}
                  columns={[
                    {
                      title: 'Professional',
                      dataIndex: 'name',
                      key: 'name',
                      render: (text, record) => (
                        <div>
                          <div className="font-medium">{text}</div>
                          <div className="text-xs text-gray-500">
                            {record.categories.join(', ')}
                          </div>
                        </div>
                      )
                    },
                    {
                      title: 'Rating',
                      dataIndex: 'rating',
                      key: 'rating',
                      render: (rating) => renderRating(rating),
                      sorter: (a, b) => a.rating - b.rating,
                      defaultSortOrder: 'descend'
                    },
                    {
                      title: 'Jobs Completed',
                      dataIndex: 'jobs_completed',
                      key: 'jobs_completed',
                      sorter: (a, b) => a.jobs_completed - b.jobs_completed,
                    },
                    {
                      title: 'Completion Rate',
                      dataIndex: 'completion_rate',
                      key: 'completion_rate',
                      render: (rate) => (
                        <div>
                          <div className="flex items-center">
                            <div className="w-12 text-right mr-2">{rate}%</div>
                            <div className="flex-1">
                              <div className="w-full bg-gray-200 rounded-full h-2">
                                <div 
                                  className="h-full rounded-full" 
                                  style={{ 
                                    width: `${rate}%`,
                                    backgroundColor: getColorForValue(rate)
                                  }}
                                />
                              </div>
                            </div>
                          </div>
                        </div>
                      ),
                      sorter: (a, b) => a.completion_rate - b.completion_rate,
                    },
                    {
                      title: 'Total Earned',
                      dataIndex: 'total_earned',
                      key: 'total_earned',
                      render: (value) => formatCurrency(value),
                      sorter: (a, b) => a.total_earned - b.total_earned,
                    },
                  ]}
                />
              </Card>
              
              {/* Professionals Needing Attention */}
              <Card title="Professionals Needing Attention" className="mb-6">
                <Table 
                  dataSource={stats.professional_stats.low_ratings}
                  rowKey="id"
                  pagination={false}
                  columns={[
                    {
                      title: 'Professional',
                      dataIndex: 'name',
                      key: 'name',
                      render: (text, record) => (
                        <div>
                          <div className="font-medium">{text}</div>
                          <div className="text-xs text-gray-500">
                            {record.categories.join(', ')}
                          </div>
                        </div>
                      )
                    },
                    {
                      title: 'Rating',
                      dataIndex: 'rating',
                      key: 'rating',
                      render: (rating, record) => (
                        <div>
                          {renderRating(rating)}
                          <div className="text-xs text-gray-500 mt-1">
                            Last: {record.last_rating.toFixed(1)}
                          </div>
                        </div>
                      ),
                      sorter: (a, b) => a.rating - b.rating,
                    },
                    {
                      title: 'Jobs',
                      dataIndex: 'jobs_completed',
                      key: 'jobs_completed',
                      render: (value) => `${value} completed`,
                      sorter: (a, b) => a.jobs_completed - b.jobs_completed,
                    },
                    {
                      title: 'Complaints',
                      dataIndex: 'complaints',
                      key: 'complaints',
                      render: (value) => (
                        <Tag color={value > 2 ? 'red' : 'orange'} className="font-medium">
                          {value} {value === 1 ? 'complaint' : 'complaints'}
                        </Tag>
                      ),
                      sorter: (a, b) => a.complaints - b.complaints,
                    },
                    {
                      title: 'Action',
                      key: 'action',
                      render: () => (
                        <Button type="link" size="small" className="text-red-500">
                          Review Profile
                        </Button>
                      ),
                    },
                  ]}
                />
              </Card>
              
              {/* Rating Distribution */}
              <Card title="Rating Distribution" className="mb-6">
                <div className="h-80">
                  <Bar
                    data={{
                      labels: stats.professional_stats.rating_distribution.map(r => `${r.rating} Star`),
                      datasets: [{
                        label: 'Number of Ratings',
                        data: stats.professional_stats.rating_distribution.map(r => r.count),
                        backgroundColor: [
                          'rgba(239, 68, 68, 0.7)',  // Red for 1 star
                          'rgba(249, 115, 22, 0.7)', // Orange for 2 stars
                          'rgba(234, 179, 8, 0.7)',  // Yellow for 3 stars
                          'rgba(16, 185, 129, 0.7)', // Green for 4 stars
                          'rgba(34, 197, 94, 0.7)'   // Emerald for 5 stars
                        ],
                        borderWidth: 1,
                        barPercentage: 0.6,
                      }]
                    }}
                    options={{
                      responsive: true,
                      maintainAspectRatio: false,
                      plugins: {
                        legend: {
                          display: false
                        },
                        tooltip: {
                          callbacks: {
                            label: function(context) {
                              const label = context.dataset.label || '';
                              const value = context.raw || 0;
                              const total = context.dataset.data.reduce((a, b) => a + b, 0);
                              const percentage = Math.round((value / total) * 100);
                              return `${label}: ${value} (${percentage}%)`;
                            }
                          }
                        }
                      },
                      scales: {
                        y: {
                          beginAtZero: true,
                          ticks: {
                            precision: 0
                          }
                        }
                      }
                    }}
                  />
                </div>
              </Card>
            </div>
          )}
        </div>
      </div>

      {loading && (
        <div className="loading-overlay">
          <Spin size="large" />
        </div>
      )}

      <Row gutter={[16, 16]} className="dashboard-stats">
        <Col xs={24} sm={12} md={6}>
          <Card className="stat-card">
            <Statistic
              title="Total Users"
              value={user_stats.total_users || 0}
              prefix={<UserOutlined />}
            />
            <div className="stat-comparison">
              <span className="trend-up">+{user_stats.new_users_this_month || 0} this month</span>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card className="stat-card">
            <Statistic
              title="Active Jobs"
              value={job_stats.active_jobs || 0}
              prefix={<ShoppingCartOutlined />}
            />
            <div className="stat-comparison">
              <span className="trend-up">+{job_stats.new_jobs_this_month || 0} new this month</span>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card className="stat-card">
            <Statistic
              title="Completed Jobs"
              value={job_stats.completed_jobs || 0}
              prefix={<CheckCircleOutlined />}
            />
            <div className="stat-comparison">
              <span className="trend-up">+{job_stats.completed_this_month || 0} this month</span>
            </div>
          </Card>
        </Col>
        <Col xs={24} sm={12} md={6}>
          <Card className="stat-card">
            <Statistic
              title="Total Revenue"
              value={revenue_stats.total_revenue || 0}
              prefix={<DollarOutlined />}
              precision={2}
              formatter={(value) => `KSh ${value.toLocaleString()}`}
            />
            <div className="stat-comparison">
              <span className="trend-up">KSh {revenue_stats.monthly_revenue_total?.toLocaleString() || 0} this month</span>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="dashboard-charts">
        <Col xs={24} lg={12}>
          <Card title="Job Status" className="chart-card">
            <div style={{ height: 300 }}>
              <PieChart 
                data={jobStatusData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      position: 'bottom',
                    },
                  },
                }}
              />
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="Jobs by Category" className="chart-card">
            <div style={{ height: 300 }}>
              <BarChart 
                data={categoryData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      ticks: {
                        precision: 0,
                      },
                    },
                  },
                }}
              />
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="dashboard-charts">
        <Col xs={24} lg={12}>
          <Card title="Revenue Trend" className="chart-card">
            <div style={{ height: 300 }}>
              <LineChart 
                data={revenueChartData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      ticks: {
                        callback: (value) => `KSh ${value.toLocaleString()}`,
                      },
                    },
                  },
                }}
              />
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card title="User Growth" className="chart-card">
            <div style={{ height: 300 }}>
              <LineChart 
                data={userGrowthData}
                options={{
                  responsive: true,
                  maintainAspectRatio: false,
                  plugins: {
                    legend: {
                      display: false,
                    },
                  },
                  scales: {
                    y: {
                      beginAtZero: true,
                      ticks: {
                        precision: 0,
                      },
                    },
                  },
                }}
              />
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="dashboard-tables">
        <Col xs={24}>
          <Card title="Recent Activities" className="table-card">
            <Table 
              columns={columns} 
              dataSource={recent_activities}
              rowKey="id"
              pagination={{ pageSize: 5 }}
              size="middle"
            />
          </Card>
        </Col>
      </Row>


    </div>
  );
};

export default AdminDashboard;
