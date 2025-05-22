import React from 'react';
import { FaBell, FaCheck, FaExclamation, FaInfo, FaRegBell } from 'react-icons/fa';

const Notifications = () => {
  // Mock data - replace with API calls
  const notifications = [
    { id: 1, type: 'success', title: 'Request Approved', message: 'Your land survey request #JPG-1001 has been approved', date: '2023-06-18 09:30', read: false },
    { id: 2, type: 'info', title: 'Document Ready', message: 'Your soil analysis report is now available for download', date: '2023-06-17 14:15', read: true },
    { id: 3, type: 'warning', title: 'Payment Required', message: 'Please submit payment for boundary survey #JPG-1004 to proceed', date: '2023-06-16 11:45', read: false },
    { id: 4, type: 'info', title: 'Status Update', message: 'Your topographic map request is now in progress', date: '2023-06-15 16:20', read: true },
    { id: 5, type: 'success', title: 'Payment Received', message: 'We have received your payment for geotechnical report', date: '2023-06-14 10:05', read: true },
  ];

  const getNotificationIcon = (type) => {
    switch (type) {
      case 'success': return <FaCheck className="text-green-500" />;
      case 'warning': return <FaExclamation className="text-yellow-500" />;
      case 'info': return <FaInfo className="text-blue-500" />;
      default: return <FaRegBell className="text-gray-500" />;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-8">
        <div className="flex items-center">
          <FaBell className="h-6 w-6 text-indigo-600 mr-2" />
          <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
        </div>
        <button className="mt-4 md:mt-0 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
          Mark all as read
        </button>
      </div>

      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <ul className="divide-y divide-gray-200">
          {notifications.map((notification) => (
            <li key={notification.id} className={`${!notification.read ? 'bg-indigo-50' : 'hover:bg-gray-50'} transition-colors duration-150`}>
              <div className="px-4 py-4 sm:px-6">
                <div className="flex items-start">
                  <div className="flex-shrink-0 pt-1 mr-4">
                    {getNotificationIcon(notification.type)}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-medium ${!notification.read ? 'text-indigo-800' : 'text-gray-900'}`}>
                      {notification.title}
                    </p>
                    <p className="text-sm text-gray-500 mt-1">
                      {notification.message}
                    </p>
                    <p className="text-xs text-gray-400 mt-2">
                      {notification.date}
                    </p>
                  </div>
                  {!notification.read && (
                    <div className="ml-4 flex-shrink-0">
                      <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                        New
                      </span>
                    </div>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
        {notifications.length === 0 && (
          <div className="px-4 py-12 text-center">
            <p className="text-gray-500">No notifications found</p>
          </div>
        )}
        <div className="bg-gray-50 px-6 py-3 flex items-center justify-between border-t border-gray-200">
          <div className="flex-1 flex justify-between sm:hidden">
            <button className="relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Previous
            </button>
            <button className="ml-3 relative inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50">
              Next
            </button>
          </div>
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Showing <span className="font-medium">1</span> to <span className="font-medium">5</span> of{' '}
                <span className="font-medium">12</span> results
              </p>
            </div>
            <div>
              <nav className="relative z-0 inline-flex rounded-md shadow-sm -space-x-px" aria-label="Pagination">
                <button className="relative inline-flex items-center px-2 py-2 rounded-l-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <span className="sr-only">Previous</span>
                  &larr;
                </button>
                <button aria-current="page" className="z-10 bg-indigo-50 border-indigo-500 text-indigo-600 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
                  1
                </button>
                <button className="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
                  2
                </button>
                <button className="bg-white border-gray-300 text-gray-500 hover:bg-gray-50 relative inline-flex items-center px-4 py-2 border text-sm font-medium">
                  3
                </button>
                <button className="relative inline-flex items-center px-2 py-2 rounded-r-md border border-gray-300 bg-white text-sm font-medium text-gray-500 hover:bg-gray-50">
                  <span className="sr-only">Next</span>
                  &rarr;
                </button>
              </nav>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Notifications;