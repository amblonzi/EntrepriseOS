import React from 'react';
import { useNavigate, Link, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { 
  LayoutDashboard, 
  Users, 
  Briefcase, 
  Package, 
  BarChart3, 
  LogOut,
  ChevronLeft,
  ChevronRight,
  CreditCard,
  UserCheck
} from 'lucide-react';
import { cn } from '../../lib/utils';

const navItems = [
  { icon: LayoutDashboard, label: 'Dashboard', href: '/' },
  { icon: Users, label: 'CRM', href: '/crm' },
  { icon: Package, label: 'Inventory', href: '/inventory' },
  { icon: CreditCard, label: 'Finance', href: '/finance' },
  { icon: UserCheck, label: 'HR', href: '/hr' },
  { icon: BarChart3, label: 'Analytics', href: '/analytics' },
  { icon: Briefcase, label: 'Projects', href: '/projects' },
];

export const Sidebar = () => {
  const [collapsed, setCollapsed] = React.useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const logout = useAuthStore((state) => state.logout);

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className={cn(
      "h-screen bg-slate-950 text-slate-300 flex flex-col transition-all duration-300 ease-in-out border-r border-slate-800",
      collapsed ? "w-20" : "w-64"
    )}>
      <div className="p-6 flex items-center justify-between">
        {!collapsed ? (
          <img src="/src/assets/logo.png" alt="Inphora OS" className="h-8 brightness-0 invert" />
        ) : (
          <img src="/favicon.png" alt="OS" className="w-8 h-8 rounded-lg" />
        )}
        <button 
          onClick={() => setCollapsed(!collapsed)}
          className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 transition-colors ml-2"
        >
          {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
        </button>
      </div>

      <nav className="flex-1 px-4 space-y-2 mt-4">
        {navItems.map((item) => {
          const isActive = location.pathname === item.href;
          return (
            <Link
              key={item.label}
              to={item.href}
              className={cn(
                "flex items-center gap-4 px-4 py-3 rounded-xl transition-all duration-200 group hover:bg-blue-600 hover:text-white",
                collapsed ? "justify-center px-2" : "",
                isActive ? "bg-blue-600 text-white" : ""
              )}
            >
              <item.icon size={22} className="shrink-0 transition-transform group-hover:scale-110" />
              {!collapsed && <span className="font-medium">{item.label}</span>}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 mt-auto border-t border-slate-800">
        <button 
          onClick={handleLogout}
          className={cn(
          "flex items-center gap-4 px-4 py-3 w-full rounded-xl hover:bg-rose-500/10 hover:text-rose-500 transition-colors",
          collapsed ? "justify-center px-2" : ""
        )}>
          <LogOut size={22} className="shrink-0" />
          {!collapsed && <span className="font-medium">Logout</span>}
        </button>
      </div>
    </aside>
  );
};

