import { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { DashboardLayout } from './components/layout/DashboardLayout';
import Dashboard from './features/dashboard/Dashboard';
import { Login } from './features/auth/Login';
import { ProtectedRoute } from './components/layout/ProtectedRoute';
import { useAuthStore } from './store/authStore';
import { CRM } from './features/crm/CRM';
import { Finance } from './features/finance/Finance';

const AuthInitializer = () => {
  const checkAuth = useAuthStore((state) => state.checkAuth);

  useEffect(() => {
    checkAuth();
  }, [checkAuth]);

  return null;
};

export function App() {
  return (
    <Router>
      <AuthInitializer />
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route path="/" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Dashboard />
            </DashboardLayout>
          </ProtectedRoute>
        } />
        
        <Route path="/crm" element={
          <ProtectedRoute>
            <DashboardLayout>
              <CRM />
            </DashboardLayout>
          </ProtectedRoute>
        } />
        
        <Route path="/inventory" element={
          <ProtectedRoute>
            <DashboardLayout>
              <div className="p-8">
                <h1 className="text-3xl font-bold text-slate-900">Inventory Module</h1>
                <p className="text-slate-500 mt-2">Stock tracking and product management coming soon.</p>
              </div>
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/finance" element={
          <ProtectedRoute>
            <DashboardLayout>
              <Finance />
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/hr" element={
          <ProtectedRoute>
            <DashboardLayout>
              <div className="p-8">
                <h1 className="text-3xl font-bold text-slate-900">HR Module</h1>
                <p className="text-slate-500 mt-2">Employee management and payroll coming soon.</p>
              </div>
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/analytics" element={
          <ProtectedRoute>
            <DashboardLayout>
              <div className="p-8">
                <h1 className="text-3xl font-bold text-slate-900">Analytics</h1>
                <p className="text-slate-500 mt-2">Advanced reporting and data visualization coming soon.</p>
              </div>
            </DashboardLayout>
          </ProtectedRoute>
        } />

        <Route path="/projects" element={
          <ProtectedRoute>
            <DashboardLayout>
              <div className="p-8">
                <h1 className="text-3xl font-bold text-slate-900">Projects</h1>
                <p className="text-slate-500 mt-2">Task management and resource planning coming soon.</p>
              </div>
            </DashboardLayout>
          </ProtectedRoute>
        } />
        
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}
