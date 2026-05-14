import React from 'react';
import { Bell, Search, User } from 'lucide-react';

export const TopBar = () => {
  return (
    <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-8">
      <div className="relative w-96">
        <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
          <Search size={18} />
        </span>
        <input 
          type="text" 
          placeholder="Search for anything..." 
          className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border-none rounded-xl focus:ring-2 focus:ring-blue-500/20 transition-all outline-none text-sm"
        />
      </div>

      <div className="flex items-center gap-6">
        <button className="relative p-2 text-slate-500 hover:bg-slate-50 rounded-full transition-colors">
          <Bell size={20} />
          <span className="absolute top-2 right-2 w-2 h-2 bg-rose-500 rounded-full border-2 border-white"></span>
        </button>
        
        <div className="flex items-center gap-3 pl-6 border-l border-slate-200">
          <div className="text-right">
            <p className="text-sm font-semibold text-slate-900">John Doe</p>
            <p className="text-xs text-slate-500">Administrator</p>
          </div>
          <div className="w-10 h-10 rounded-full bg-blue-100 flex items-center justify-center text-blue-600">
            <User size={20} />
          </div>
        </div>
      </div>
    </header>
  );
};
