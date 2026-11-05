import React, { useEffect, useState } from 'react';
import {
  Search,
  Plus,
  Filter,
  Sparkles,
  Edit,
  ExternalLink,
  Laptop,
  CheckCircle,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { StatusBadge } from '../components/StatusBadge';
import { DepartmentBadge } from '../components/DepartmentBadge';
import { EmployeeModal } from '../components/EmployeeModal';
import { apiClient } from '../api/client';
import { Employee } from '../types';

interface Props {
  onSelectEmployee: (id: string) => void;
}

export const EmployeeManagementPage: React.FC<Props> = ({ onSelectEmployee }) => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [search, setSearch] = useState('');
  const [deptFilter, setDeptFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [employeeToEdit, setEmployeeToEdit] = useState<Employee | null>(null);
  const [generatingId, setGeneratingId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const fetchEmployees = async () => {
    try {
      const data = await apiClient.getEmployees(search, deptFilter || undefined, statusFilter || undefined);
      setEmployees(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEmployees();
  }, [search, deptFilter, statusFilter]);

  const handleGeneratePlan = async (empId: string) => {
    setGeneratingId(empId);
    try {
      await apiClient.generatePlan(empId);
      onSelectEmployee(empId);
      navigate('/workspace');
    } catch (err) {
      console.error(err);
    } finally {
      setGeneratingId(null);
    }
  };

  const openEdit = (emp: Employee) => {
    setEmployeeToEdit(emp);
    setIsModalOpen(true);
  };

  const openCreate = () => {
    setEmployeeToEdit(null);
    setIsModalOpen(true);
  };

  return (
    <div className="space-y-6">
      {/* Header with Title and Add Button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Employee Management</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Manage onboarding candidates, departmental roles, and AI-personalized onboarding roadmaps.
          </p>
        </div>
        <button
          onClick={openCreate}
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-sky-600 hover:bg-sky-700 text-white rounded-lg text-xs font-semibold shadow-sm transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>Add Employee</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row gap-3 items-center justify-between">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search candidate name, ID, or role..."
            className="w-full pl-9 pr-3 py-1.5 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
        </div>

        <div className="flex flex-wrap items-center gap-2 w-full md:w-auto">
          <div className="flex items-center gap-1 text-xs text-slate-500">
            <Filter className="w-3.5 h-3.5" />
            <span>Filter:</span>
          </div>

          <select
            value={deptFilter}
            onChange={(e) => setDeptFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
          >
            <option value="">All Departments</option>
            <option value="Engineering">Engineering</option>
            <option value="Product">Product</option>
            <option value="Human Resources">Human Resources</option>
            <option value="Finance">Finance & Payroll</option>
            <option value="Sales">Sales</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-2.5 py-1.5 text-xs border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-sky-500"
          >
            <option value="">All Statuses</option>
            <option value="Onboarding">Onboarding</option>
            <option value="At Risk">At Risk</option>
            <option value="Ready">Ready</option>
            <option value="Completed">Completed</option>
          </select>
        </div>
      </div>

      {/* Employee List Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50/80 border-b border-slate-200/80 text-slate-500 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3.5 px-4">Employee ID</th>
                <th className="py-3.5 px-4">Candidate Name</th>
                <th className="py-3.5 px-4">Department & Role</th>
                <th className="py-3.5 px-4">Work Location</th>
                <th className="py-3.5 px-4">Joining Date</th>
                <th className="py-3.5 px-4">Status</th>
                <th className="py-3.5 px-4 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {loading ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center">
                    <div className="w-6 h-6 border-4 border-sky-600 border-t-transparent rounded-full animate-spin mx-auto" />
                  </td>
                </tr>
              ) : employees.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-sm text-slate-400 font-medium">
                    No employees found matching your filters.
                  </td>
                </tr>
              ) : (
              employees.map((emp) => (
                <tr key={emp.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3.5 px-4 font-mono font-semibold text-slate-700">{emp.employee_id}</td>
                  <td className="py-3.5 px-4">
                    <div className="font-bold text-slate-900">{emp.full_name}</div>
                    <div className="text-[11px] text-slate-400">{emp.email}</div>
                  </td>
                  <td className="py-3.5 px-4">
                    <div className="flex items-center gap-1.5 mb-1">
                      <DepartmentBadge department={emp.department} />
                      <span className="text-[11px] font-medium text-slate-500">{emp.experience_level}</span>
                    </div>
                    <div className="text-slate-800 font-semibold">{emp.job_role}</div>
                  </td>
                  <td className="py-3.5 px-4 text-slate-600">{emp.work_location}</td>
                  <td className="py-3.5 px-4 font-mono text-slate-700">{emp.joining_date}</td>
                  <td className="py-3.5 px-4">
                    <StatusBadge status={emp.status} />
                  </td>
                  <td className="py-3.5 px-4 text-right">
                    <div className="flex items-center justify-end gap-1.5">
                      <button
                        onClick={() => {
                          onSelectEmployee(emp.id);
                          navigate('/workspace');
                        }}
                        title="View Workspace"
                        className="px-2.5 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                        <span>Workspace</span>
                      </button>

                      <button
                        onClick={() => handleGeneratePlan(emp.id)}
                        disabled={generatingId === emp.id}
                        title="Regenerate AI Onboarding Plan"
                        className="p-1.5 bg-sky-50 hover:bg-sky-100 text-sky-700 rounded-lg transition-colors disabled:opacity-50"
                      >
                        <Sparkles className="w-3.5 h-3.5" />
                      </button>

                      <button
                        onClick={() => openEdit(emp)}
                        title="Edit Details"
                        className="p-1.5 text-slate-400 hover:text-slate-700 hover:bg-slate-100 rounded-lg transition-colors"
                      >
                        <Edit className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      <EmployeeModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSaved={fetchEmployees}
        employeeToEdit={employeeToEdit}
      />
    </div>
  );
};
