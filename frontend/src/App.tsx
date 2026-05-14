import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { DashboardLayout } from './components/layout/DashboardLayout';
import Dashboard from './features/dashboard/Dashboard';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={
          <DashboardLayout>
            <Dashboard />
          </DashboardLayout>
        } />
        {/* Add more routes as needed */}
        <Route path="/crm" element={
          <DashboardLayout>
            <div className="p-8">
              <h1 className="text-3xl font-bold">CRM Module</h1>
              <p className="text-slate-500 mt-2">Lead management and sales pipeline coming soon.</p>
            </div>
          </DashboardLayout>
        } />
      </Routes>
    </Router>
  );
}

export default App;
