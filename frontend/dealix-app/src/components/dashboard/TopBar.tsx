import { Bell, Search, User, Calendar, Clock } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useState } from 'react';

interface Props {
  sidebarOpen: boolean;
  setSidebarOpen: (v: boolean) => void;
}

export default function TopBar(_props: Props) {
  const [searchFocused, setSearchFocused] = useState(false);
  void searchFocused;
  const now = new Date();
  const timeStr = now.toLocaleTimeString('ar-SA', { hour: '2-digit', minute: '2-digit' });
  const dateStr = now.toLocaleDateString('ar-SA', { year: 'numeric', month: 'short', day: 'numeric' });

  return (
    <header className="h-16 bg-white border-b border-gray-100 flex items-center justify-between px-6 sticky top-0 z-30">
      {/* Left: Search */}
      <div className={`flex items-center gap-2 bg-gray-50 rounded-lg px-3 py-2 transition-all ${searchFocused ? 'ring-2 ring-dealix-emerald/30 w-80' : 'w-64'}`}>
        <Search className="w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="البحث في النظام..."
          className="bg-transparent text-sm outline-none w-full text-right"
          style={{ direction: 'rtl' }}
          onFocus={() => setSearchFocused(true)}
          onBlur={() => setSearchFocused(false)}
        />
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-4">
        {/* Date/Time */}
        <div className="hidden md:flex items-center gap-4 text-sm text-gray-500">
          <div className="flex items-center gap-1.5">
            <Calendar className="w-4 h-4" />
            <span>{dateStr}</span>
          </div>
          <div className="flex items-center gap-1.5">
            <Clock className="w-4 h-4" />
            <span>{timeStr}</span>
          </div>
        </div>

        <div className="w-px h-6 bg-gray-200" />

        {/* Notifications */}
        <Link
          to="/notifications"
          className="relative p-2 text-gray-500 hover:text-dealix-emerald hover:bg-dealix-emerald/5 rounded-lg transition-colors"
        >
          <Bell className="w-5 h-5" />
          <span className="absolute top-1 right-1 w-4 h-4 bg-red-500 text-white text-[10px] rounded-full flex items-center justify-center font-bold">
            5
          </span>
        </Link>

        {/* User */}
        <div className="flex items-center gap-3">
          <div className="text-right hidden sm:block">
            <p className="text-sm font-semibold text-gray-800">المؤسس</p>
            <p className="text-xs text-gray-400">CEO</p>
          </div>
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-dealix-emerald to-dealix-gold flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
        </div>
      </div>
    </header>
  );
}
