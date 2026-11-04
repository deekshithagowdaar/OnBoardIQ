import React, { useEffect, useState } from 'react';
import {
  Calendar,
  MapPin,
  Briefcase,
  User,
  Clock,
  AlertTriangle,
  CheckCircle2,
  Filter,
  Sparkles,
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { DepartmentBadge } from '../components/DepartmentBadge';
import { TaskDetailModal } from '../components/TaskDetailModal';
import { apiClient } from '../api/client';
import { Employee, Task } from '../types';

interface Props {
  selectedEmployeeId: string;
}

export const OnboardingWorkspacePage: React.FC<Props> = ({ selectedEmployeeId }) => {
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [activeTab, setActiveTab] = useState<'All' | 'HR' | 'IT' | 'Payroll' | 'Benefits'>('All');
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    if (!selectedEmployeeId) return;
    try {
      const [emp, tList] = await Promise.all([
        apiClient.getEmployee(selectedEmployeeId),
        apiClient.getTasks(selectedEmployeeId),
      ]);
      setEmployee(emp);
      setTasks(tList);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedEmployeeId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const filteredTasks = activeTab === 'All' ? tasks : tasks.filter((t) => t.department === activeTab);
  const completedCount = tasks.filter((t) => t.status === 'Completed').length;
  const blockedCount = tasks.filter((t) => t.status === 'Blocked' || t.status === 'Delayed').length;

  return (
    <div className="space-y-6">
      {/* Profile Header Banner */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="w-14 h-14 rounded-2xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center text-white font-extrabold text-xl shadow-md">
              {employee?.full_name?.split(' ').map((n) => n[0]).join('')}
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-xl font-bold text-slate-900">{employee?.full_name}</h2>
                <StatusBadge status={employee?.status || 'Onboarding'} />
              </div>
              <p className="text-xs text-slate-500 mt-0.5">
                {employee?.job_role} • <span className="font-semibold text-slate-700">{employee?.department}</span>
              </p>
              <div className="mt-2.5 flex flex-wrap gap-4 text-xs text-slate-500">
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-slate-400" /> {employee?.work_location}
                </span>
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-slate-400" /> Joining: {employee?.joining_date}
                </span>
                <span className="flex items-center gap-1.5">
                  <User className="w-3.5 h-3.5 text-slate-400" /> Manager: {employee?.reporting_manager}
                </span>
              </div>
            </div>
          </div>

          {/* Quick Metrics */}
          <div className="flex items-center gap-3 bg-slate-50 p-3 rounded-xl border border-slate-100">
            <div className="text-center px-3">
              <span className="text-[10px] font-semibold uppercase text-slate-400 block">Progress</span>
              <span className="text-base font-bold text-slate-900">
                {tasks.length > 0 ? Math.round((completedCount / tasks.length) * 100) : 0}%
              </span>
            </div>
            <div className="w-px h-8 bg-slate-200" />
            <div className="text-center px-3">
              <span className="text-[10px] font-semibold uppercase text-slate-400 block">Blockers</span>
              <span className={`text-base font-bold ${blockedCount > 0 ? 'text-rose-600' : 'text-slate-900'}`}>
                {blockedCount}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Department Tabs & Task Filters */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-200 pb-2">
        <div className="flex items-center gap-1 overflow-x-auto pb-1">
          {(['All', 'HR', 'IT', 'Payroll', 'Benefits'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === tab
                  ? 'bg-slate-900 text-white shadow-sm'
                  : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
              }`}
            >
              {tab === 'All' ? 'All Department Tasks' : `${tab} Agent Track`}
            </button>
          ))}
        </div>

        <span className="text-xs text-slate-500 font-medium">
          Showing {filteredTasks.length} task(s)
        </span>
      </div>

      {/* Task Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredTasks.map((task) => {
          const isBlocked = task.status === 'Blocked' || task.status === 'Delayed';
          return (
            <div
              key={task.id}
              onClick={() => setSelectedTask(task)}
              className={`bg-white rounded-xl border p-4 shadow-sm hover:shadow-md transition-all cursor-pointer text-left relative overflow-hidden ${
                isBlocked ? 'border-amber-300 ring-1 ring-amber-100' : 'border-slate-200/80'
              }`}
            >
              <div className="flex items-center justify-between gap-2 mb-2">
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs font-bold text-slate-400">{task.task_id}</span>
                  <DepartmentBadge department={task.department} />
                </div>
                <StatusBadge status={task.status} />
              </div>

              <h4 className="font-bold text-slate-900 text-sm">{task.name}</h4>
              <p className="text-xs text-slate-500 mt-1 line-clamp-2 leading-relaxed">
                {task.description}
              </p>

              {isBlocked && task.delay_reason && (
                <div className="mt-3 p-2 bg-rose-50 border border-rose-200 rounded-lg flex items-start gap-1.5 text-xs text-rose-800">
                  <AlertTriangle className="w-3.5 h-3.5 text-rose-600 flex-shrink-0 mt-0.5" />
                  <span className="font-medium text-[11px] leading-snug">{task.delay_reason}</span>
                </div>
              )}

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <div className="flex items-center gap-1.5">
                  <User className="w-3.5 h-3.5 text-slate-400" />
                  <span className="font-medium text-slate-700">{task.assigned_person}</span>
                </div>
                <div className="flex items-center gap-1.5 font-mono text-[11px] text-slate-600">
                  <Clock className="w-3 h-3 text-slate-400" />
                  <span>Due {task.due_date}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <TaskDetailModal
        task={selectedTask}
        onClose={() => setSelectedTask(null)}
        onTaskUpdated={loadData}
      />
    </div>
  );
};
