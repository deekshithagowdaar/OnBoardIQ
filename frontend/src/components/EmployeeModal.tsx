import React, { useState } from 'react';
import { X, UserPlus, Check } from 'lucide-react';
import { Employee } from '../types';
import { apiClient } from '../api/client';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSaved: () => void;
  employeeToEdit?: Employee | null;
}

export const EmployeeModal: React.FC<Props> = ({ isOpen, onClose, onSaved, employeeToEdit }) => {
  if (!isOpen) return null;

  const [formData, setFormData] = useState({
    employee_id: employeeToEdit?.employee_id || `EMP-2024-${Math.floor(100 + Math.random() * 900)}`,
    full_name: employeeToEdit?.full_name || '',
    email: employeeToEdit?.email || '',
    department: employeeToEdit?.department || 'Engineering',
    job_role: employeeToEdit?.job_role || '',
    employment_type: employeeToEdit?.employment_type || 'Full-time',
    work_location: employeeToEdit?.work_location || 'Hybrid - New York',
    joining_date: employeeToEdit?.joining_date || '2026-12-01',
    reporting_manager: employeeToEdit?.reporting_manager || 'Sarah Johnson',
    experience_level: employeeToEdit?.experience_level || 'Mid-level',
    required_equipment: employeeToEdit?.required_equipment?.join(', ') || 'MacBook Pro, 4K Monitor, YubiKey',
    applicable_requirements: employeeToEdit?.applicable_requirements?.join(', ') || 'I-9 Verification, NDA, Direct Deposit',
  });
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      const payload = {
        ...formData,
        required_equipment: formData.required_equipment.split(',').map((s) => s.trim()).filter(Boolean),
        applicable_requirements: formData.applicable_requirements.split(',').map((s) => s.trim()).filter(Boolean),
      };

      if (employeeToEdit) {
        await apiClient.updateEmployee(employeeToEdit.id, payload);
      } else {
        await apiClient.createEmployee(payload);
      }
      onSaved();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-2xl overflow-hidden my-8 animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <div className="flex items-center gap-2">
            <div className="p-2 rounded-lg bg-sky-50 text-sky-600">
              <UserPlus className="w-4 h-4" />
            </div>
            <div>
              <h3 className="font-bold text-slate-900 text-sm">
                {employeeToEdit ? 'Edit Employee Profile' : 'Create New Employee Profile'}
              </h3>
              <p className="text-xs text-slate-500">
                AI Onboarding Orchestrator will automatically generate a tailored onboarding plan.
              </p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Employee ID</label>
              <input
                type="text"
                required
                value={formData.employee_id}
                onChange={(e) => setFormData({ ...formData, employee_id: e.target.value })}
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 font-mono"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
              <input
                type="text"
                required
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                placeholder="e.g. Alex Morgan"
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Email Address</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                placeholder="e.g. alex.morgan@corp.com"
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Department</label>
              <select
                value={formData.department}
                onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 bg-white"
              >
                <option value="Engineering">Engineering</option>
                <option value="Product">Product Management</option>
                <option value="Human Resources">Human Resources</option>
                <option value="Finance">Finance & Payroll</option>
                <option value="Sales">Sales & Go-to-Market</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Job Role</label>
              <input
                type="text"
                required
                value={formData.job_role}
                onChange={(e) => setFormData({ ...formData, job_role: e.target.value })}
                placeholder="e.g. Software Developer"
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Reporting Manager</label>
              <input
                type="text"
                required
                value={formData.reporting_manager}
                onChange={(e) => setFormData({ ...formData, reporting_manager: e.target.value })}
                placeholder="e.g. Sarah Johnson"
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Joining Date</label>
              <input
                type="date"
                required
                value={formData.joining_date}
                onChange={(e) => setFormData({ ...formData, joining_date: e.target.value })}
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Work Location</label>
              <input
                type="text"
                value={formData.work_location}
                onChange={(e) => setFormData({ ...formData, work_location: e.target.value })}
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Experience Level</label>
              <select
                value={formData.experience_level}
                onChange={(e) => setFormData({ ...formData, experience_level: e.target.value })}
                className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 bg-white"
              >
                <option value="Junior">Junior</option>
                <option value="Mid-level">Mid-level</option>
                <option value="Senior">Senior</option>
                <option value="Lead">Lead</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">
              Required Hardware / Equipment (Comma separated)
            </label>
            <input
              type="text"
              value={formData.required_equipment}
              onChange={(e) => setFormData({ ...formData, required_equipment: e.target.value })}
              className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </div>

          <div className="pt-4 border-t border-slate-100 flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="px-4 py-2 text-xs font-medium bg-sky-600 hover:bg-sky-700 text-white rounded-lg shadow-sm transition-colors disabled:opacity-50 flex items-center gap-1.5"
            >
              <Check className="w-3.5 h-3.5" />
              {submitting ? 'Generating Plan...' : employeeToEdit ? 'Save Changes' : 'Create & Generate Plan'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
