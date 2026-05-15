import { useEffect, useState } from 'react';
import { Plus, Search, FileText, CreditCard, ArrowUpRight, ArrowDownLeft, X } from 'lucide-react';
import api from '../../lib/api';

interface Invoice {
  id: string;
  invoice_number: string;
  client_name: string;
  amount: number;
  status: string;
  due_date: string;
}

const statusColors: Record<string, string> = {
  'PENDING': 'bg-amber-100 text-amber-700',
  'PAID': 'bg-emerald-100 text-emerald-700',
  'OVERDUE': 'bg-rose-100 text-rose-700',
};

export const Finance = () => {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newInvoice, setNewInvoice] = useState({
    invoice_number: '',
    client_name: '',
    amount: 0,
    due_date: ''
  });

  const fetchInvoices = async () => {
    setIsLoading(true);
    try {
      const response = await api.get('/finance/invoices');
      setInvoices(response.data);
    } catch (error) {
      console.error('Failed to fetch invoices:', error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchInvoices();
  }, []);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.post('/finance/invoices', newInvoice);
      setShowModal(false);
      setNewInvoice({
        invoice_number: '',
        client_name: '',
        amount: 0,
        due_date: ''
      });
      fetchInvoices();
    } catch (error) {
      console.error('Failed to create invoice:', error);
    }
  };

  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Financial Management</h1>
          <p className="text-slate-500 mt-1">Track your invoices, expenses, and overall financial health.</p>
        </div>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-5 py-2.5 rounded-xl font-medium hover:bg-blue-700 transition-colors flex items-center gap-2 shadow-sm shadow-blue-600/20"
        >
          <Plus size={18} />
          New Invoice
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-emerald-50 flex items-center justify-center text-emerald-600">
              <ArrowDownLeft size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">Total Income</p>
              <h3 className="text-2xl font-bold text-slate-900">$12,450.00</h3>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-rose-50 flex items-center justify-center text-rose-600">
              <ArrowUpRight size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">Total Expenses</p>
              <h3 className="text-2xl font-bold text-slate-900">$4,280.00</h3>
            </div>
          </div>
        </div>
        <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600">
              <CreditCard size={24} />
            </div>
            <div>
              <p className="text-sm font-medium text-slate-500">Net Profit</p>
              <h3 className="text-2xl font-bold text-slate-900">$8,170.00</h3>
            </div>
          </div>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-3xl shadow-2xl w-full max-w-lg overflow-hidden">
            <div className="p-6 border-b border-slate-100 flex items-center justify-between">
              <h2 className="text-xl font-bold text-slate-900">Create New Invoice</h2>
              <button onClick={() => setShowModal(false)} className="p-2 hover:bg-slate-100 rounded-full text-slate-400">
                <X size={20} />
              </button>
            </div>
            <form onSubmit={handleCreate} className="p-6 space-y-4">
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Invoice Number</label>
                <input 
                  required
                  type="text" 
                  value={newInvoice.invoice_number}
                  onChange={(e) => setNewInvoice({...newInvoice, invoice_number: e.target.value})}
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                  placeholder="INV-2026-001"
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-slate-700">Client Name</label>
                <input 
                  required
                  type="text" 
                  value={newInvoice.client_name}
                  onChange={(e) => setNewInvoice({...newInvoice, client_name: e.target.value})}
                  className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-slate-700">Amount ($)</label>
                  <input 
                    required
                    type="number" 
                    value={newInvoice.amount}
                    onChange={(e) => setNewInvoice({...newInvoice, amount: parseFloat(e.target.value)})}
                    className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-slate-700">Due Date</label>
                  <input 
                    required
                    type="date" 
                    value={newInvoice.due_date}
                    onChange={(e) => setNewInvoice({...newInvoice, due_date: e.target.value})}
                    className="w-full px-4 py-2 bg-slate-50 border border-slate-200 rounded-xl"
                  />
                </div>
              </div>
              <div className="pt-4 flex gap-3">
                <button 
                  type="button" 
                  onClick={() => setShowModal(false)}
                  className="flex-1 px-4 py-2.5 border border-slate-200 text-slate-600 font-medium rounded-xl hover:bg-slate-50"
                >
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="flex-1 px-4 py-2.5 bg-blue-600 text-white font-medium rounded-xl hover:bg-blue-700 shadow-sm shadow-blue-600/20"
                >
                  Create Invoice
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/50">
          <div className="relative w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
            <input 
              type="text" 
              placeholder="Search invoices..." 
              className="w-full pl-9 pr-4 py-2 bg-white border border-slate-200 rounded-lg text-sm"
            />
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50/50 border-b border-slate-200">
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Invoice</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Client</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Status</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Amount</th>
                <th className="px-6 py-4 text-xs font-semibold text-slate-500 uppercase">Due Date</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {isLoading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                    <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
                    Loading invoices...
                  </td>
                </tr>
              ) : invoices.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-8 text-center text-slate-500">
                    No invoices found.
                  </td>
                </tr>
              ) : (
                invoices.map((invoice) => (
                  <tr key={invoice.id} className="hover:bg-slate-50/50 transition-colors cursor-pointer">
                    <td className="px-6 py-4">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-600">
                          <FileText size={18} />
                        </div>
                        <span className="text-sm font-medium text-slate-900">{invoice.invoice_number}</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-600">{invoice.client_name}</td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${statusColors[invoice.status] || 'bg-slate-100 text-slate-700'}`}>
                        {invoice.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm font-medium text-slate-900">
                      {new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(invoice.amount)}
                    </td>
                    <td className="px-6 py-4 text-sm text-slate-500">
                      {new Date(invoice.due_date).toLocaleDateString()}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
