import React, { useState, useRef, useEffect } from 'react';
import { MoreHorizontal } from 'lucide-react';


const ThreeDotMenuGroup = () => {
  const [open, setOpen] = useState(false);
  const menuRef = useRef();

  // Đóng menu khi click bên ngoài
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={menuRef}>
      <button
        onClick={() => setOpen(!open)}
        className="p-2 rounded-full hover:bg-gray-200"
      >
        <MoreHorizontal className="w-5 h-5" />
      </button>

      {open && (
        <div className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-xl bg-white shadow-xl ring-1 ring-black ring-opacity-5">
          <div className="py-2 px-3 text-sm text-gray-800">
            <div className="flex items-center gap-2 hover:bg-gray-100 p-2 rounded cursor-pointer">
              <span>🚩</span> <span>Báo cáo Trang</span>
            </div>
            <div className="flex items-center gap-2 hover:bg-gray-100 p-2 rounded cursor-pointer">
              <span>🚫</span> <span>Chặn</span>
            </div>
            <div className="flex items-center gap-2 hover:bg-gray-100 p-2 rounded cursor-pointer">
              <span>➕</span> <span>Mời bạn bè</span>
            </div>
            <div className="flex items-center gap-2 hover:bg-gray-100 p-2 rounded cursor-pointer">
              <span>👍</span> <span>Thích</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ThreeDotMenuGroup;
