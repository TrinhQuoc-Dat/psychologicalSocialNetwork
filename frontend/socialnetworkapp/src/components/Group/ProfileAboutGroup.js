import React from 'react';
import { formatDateFromArray } from '../../app/utils/dateUtils';

const ProfileAboutGroups = ({ group }) => {
  const infoSections = [
    { title: 'Thông tin cơ bản', items: [
      { label: 'Vai trò', value: group?.creator.role },
      { label: 'Ngày tham gia', value: formatDateFromArray(group?.created_date) }
    ]},
    { title: 'Liên hệ', items: [
      { label: 'Email', value: group?.creator.email },
      { label: 'Điện thoại', value: group?.creator.phone }
    ]}
  ];

  return (
    <div className="bg-white p-4 rounded-xl shadow">
      <h2 className="text-xl font-bold mb-4">Giới thiệu</h2>
      
      {infoSections.map((section, index) => (
        <div key={index} className="mb-6">
          <h3 className="font-semibold text-lg mb-2">{section.title}</h3>
          <div className="space-y-2">
            {section.items.map((item, idx) => (
              item.value && (
                <div key={idx} className="flex gap-4">
                  <span className="text-gray-600 w-24">{item.label}:</span>
                  <span className="font-medium">{item.value}</span>
                </div>
              )
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProfileAboutGroups;