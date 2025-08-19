import React from 'react';
import ThreeDotMenuGroup from './ThreeDotMenuGroup';

const tabs = [
  { key: 'timeline', label: 'Bài viết' },
  { key: 'about', label: 'Giới thiệu' },
  { key: 'photos', label: 'Ảnh' },
];

const ProfileTabsGroup = ({ activeTab, setActiveTab }) => {
  return (
    <div className="flex border-b mb-4 items-center justify-between">
  <div className="flex">
    {tabs.map(tab => (
      <button
        key={tab.key}
        onClick={() => setActiveTab(tab.key)}
        className={`px-8 py-4 font-medium relative ${
          activeTab === tab.key
            ? 'text-blue-600'
            : 'text-gray-600 hover:bg-gray-100'
        }`}
      >
        {tab.label}
        {activeTab === tab.key && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-blue-600" />
        )}
      </button>
    ))}
  </div>
  <div className="ml-auto px-4">
    <ThreeDotMenuGroup />
  </div>
</div>

  );
};

export default ProfileTabsGroup;