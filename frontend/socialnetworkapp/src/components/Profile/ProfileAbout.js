import React from 'react';
import { formatDateFromArray } from '../../app/utils/dateUtils';
import { FaUser, FaIdBadge, FaCalendarAlt, FaEnvelope, FaPhone } from 'react-icons/fa';

const ProfileAbout = ({ user }) => {
  console.log("user: ", user);

  const infoSections = [
    {
      title: 'Thông tin cơ bản',
      items: [
        { label: 'Vai trò', value: user?.role, icon: <FaIdBadge className="text-blue-500 w-5 h-5" /> },
        { label: 'Họ', value: user?.first_name, icon: <FaUser className="text-green-500 w-5 h-5" /> },
        { label: 'Tên', value: user?.last_name, icon: <FaUser className="text-green-500 w-5 h-5" /> },
        { label: 'Ngày tham gia', value: formatDateFromArray(user?.last_login), icon: <FaCalendarAlt className="text-purple-500 w-5 h-5" /> },
      ]
    },
    {
      title: 'Liên hệ',
      items: [
        { label: 'Email', value: user?.email, icon: <FaEnvelope className="text-red-500 w-5 h-5" /> },
        { label: 'Điện thoại', value: user?.phone, icon: <FaPhone className="text-yellow-500 w-5 h-5" /> },
      ]
    }
  ];

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border border-gray-100 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">Giới thiệu</h2>
      
      {infoSections.map((section, index) => (
        <div key={index} className="mb-6">
          <h3 className="font-semibold text-lg mb-3 text-gray-700 border-b pb-2">{section.title}</h3>
          <div className="space-y-3">
            {section.items.map((item, idx) => (
              item.value && (
                <div key={idx} className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                  <div className="flex-shrink-0">{item.icon}</div>
                  <div className="flex flex-col">
                    <span className="text-gray-500 text-sm">{item.label}</span>
                    <span className="font-medium text-gray-800">{item.value}</span>
                  </div>
                </div>
              )
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProfileAbout;
