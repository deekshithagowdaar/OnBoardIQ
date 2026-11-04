import React, { useEffect, useState } from 'react';
import {
  Users,
  AlertTriangle,
  Clock,
  CheckCircle2,
  TrendingUp,
  ArrowRight,
  ShieldAlert,
  Sparkles,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { StatCard } from '../components/StatCard';
import { StatusBadge } from '../components/StatusBadge';
import { DepartmentBadge } from '../components/DepartmentBadge';
import { apiClient } from '../api/client';
import { Employee, Task, ApprovalRequest, ReadinessData } from '../types';

interface Props {
  selectedEmployeeId: string;
}

export const DashboardPage: React.FC<Props> = ({ selectedEmployeeId }) => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [readiness, setReadiness] = useState<ReadinessData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [empRes, appRes] = await Promise.all([
          apiClient.getEmployees(),
          apiClient.getApprovals(),
        ]);
        setEmployees(empRes);
        setApprovals(appRes);

        if (selectedEmployeeId) {
          const [tRes, rRes] = await Promise.all([
            apiClient.getTasks(selectedEmployeeId),
            apiClient.getReadiness(selectedEmployeeId),
          ]);
          setTasks(tRes);
          setReadiness(rRes);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [selectedEmployeeId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const activeEmployee = employees.find((e) => e.id === selectedEmployeeId) || employees[0];
  const atRiskEmployees = employees.filter((e) => e.status === 'At Risk');
  const blockedTasks = tasks.filter((t) => t.status === 'Blocked' || t.status === 'Delayed');
  const pendingApprovals = approvals.filter((a) => a.status === 'Pending');

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-sky-900 via-indigo-900 to-slate-900 rounded-2xl p-6 text-white shadow-lg relative overflow-hidden">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-sky-500/20 border border-sky-400/30 text-sky-200 text-xs font-semibold mb-3">
            <Sparkles className="w-3.5 h-3.5" /> Agentic AI Orchestration Active
          </div>
          <h2 className="text-2xl font-bold tracking-tight">
            Welcome back, Sarah. Onboarding Orchestrator is running.
          </h2>
          <p className="mt-2 text-sm text-slate-300 leading-relaxed">
            Active employee profile: <span className="font-semibold text-white">{activeEmployee?.full_name}</span> ({activeEmployee?.job_role}).
            {blockedTasks.length > 0
              ? ` System detected ${blockedTasks.length} blocked or delayed task(s) requiring automated recovery simulation.`
              : ' All scheduled tasks are progressing within established SLA parameters.'}
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Link
              to="/simulator"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-sky-500 hover:bg-sky-400 text-white text-xs font-semibold shadow transition-colors"
            >
              <span>Launch What-If Simulator</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
            <Link
              to="/graph"
              className="inline-flex items-center gap-1.5 px-4 py-2 rounded-lg bg-white/10 hover:bg-white/20 text-white text-xs font-semibold border border-white/20 transition-colors"
            >
              <span>Inspect Dependency Graph</span>
            </Link>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Total Employees"
          value={employees.length}
          subtitle="Across 4 departments"
          icon={<Users className="w-5 h-5 text-sky-600" />}
          trend="+2 this month"
          trendType="neutral"
        />
        <StatCard
          title="Employees At Risk"
          value={atRiskEmployees.length}
          subtitle="Predicted delay impact"
          icon={<AlertTriangle className="w-5 h-5 text-rose-600" />}
          trend={atRiskEmployees.length > 0 ? 'Action Needed' : 'Nominal'}
          trendType={atRiskEmployees.length > 0 ? 'negative' : 'positive'}
        />
        <StatCard
          title="Blocked Tasks"
          value={blockedTasks.length}
          subtitle="Awaiting upstream resolution"
          icon={<Clock className="w-5 h-5 text-amber-600" />}
          trend={`${tasks.length} total tasks`}
          trendType="neutral"
        />
        <StatCard
          title="Pending Approvals"
          value={pendingApprovals.length}
          subtitle="Self-healing recovery actions"
          icon={<CheckCircle2 className="w-5 h-5 text-emerald-600" />}
          trend="Manager Decision Required"
          trendType={pendingApprovals.length > 0 ? 'negative' : 'positive'}
        />
      </div>

      {/* Middle Grid: Active Profile Health & Department Progress */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Active Profile Health Card */}
        <div className="bg-white rounded-xl border border-slate-200/80 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base">Day-1 Readiness Health</h3>
              <p className="text-xs text-slate-500">{activeEmployee?.full_name}</p>
            </div>
            <StatusBadge status={activeEmployee?.status || 'Onboarding'} />
          </div>

          <div className="flex items-center gap-4 my-6">
            <div className="relative w-24 h-24 flex items-center justify-center">
              <div className="text-3xl font-extrabold text-slate-900">
                {readiness?.overall_score || 0}%
              </div>
            </div>
            <div className="flex-1 space-y-1">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Status Tier</span>
              <p className="text-sm font-bold text-slate-800">{readiness?.readiness_tier || 'Evaluating...'}</p>
              <p className="text-xs text-slate-500 leading-relaxed">
                Joining Date: <span className="font-mono font-semibold text-slate-700">{activeEmployee?.joining_date}</span>
              </p>
            </div>
          </div>

          <div className="space-y-3 pt-3 border-t border-slate-100">
            <div className="flex justify-between text-xs">
              <span className="text-slate-500">Completed Tasks:</span>
              <span className="font-semibold text-slate-900">{readiness?.completed_tasks_count || 0} / {readiness?.total_tasks_count || 0}</span>
            </div>
            <div className="flex justify-between text-xs">
              <span className="text-slate-500">Active Blockers:</span>
              <span className="font-semibold text-rose-600">{readiness?.blocked_tasks_count || 0}</span>
            </div>
            <div className="flex justify-between text-xs">
              <span className="text-slate-500">Critical Path Tasks:</span>
              <span className="font-semibold text-slate-900">{readiness?.critical_path_tasks?.length || 0}</span>
            </div>
          </div>

          <Link
            to="/readiness"
            className="mt-5 w-full flex items-center justify-center gap-1.5 py-2 rounded-lg border border-slate-200 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition-colors"
          >
            <span>View Full Readiness Breakdown</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {/* Department Coordination Progress */}
        <div className="bg-white rounded-xl border border-slate-200/80 p-6 shadow-sm lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base">Multi-Agent Department Progress</h3>
              <p className="text-xs text-slate-500">Cross-functional task completion status</p>
            </div>
            <span className="text-xs font-medium text-slate-500">Synchronized via LangGraph</span>
          </div>

          <div className="space-y-4 my-2">
            {[
              { name: 'Human Resources (HR)', key: 'HR', color: 'bg-purple-600', score: readiness?.department_scores?.HR ?? 50 },
              { name: 'Information Technology (IT)', key: 'IT', color: 'bg-cyan-600', score: readiness?.department_scores?.IT ?? 25 },
              { name: 'Finance & Payroll', key: 'Payroll', color: 'bg-emerald-600', score: readiness?.department_scores?.Payroll ?? 75 },
              { name: 'Benefits & Healthcare', key: 'Benefits', color: 'bg-amber-600', score: readiness?.department_scores?.Benefits ?? 100 },
            ].map((d) => (
              <div key={d.key} className="space-y-1.5">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-700">{d.name}</span>
                  <span className="font-semibold text-slate-900">{d.score}%</span>
                </div>
                <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full ${d.color} transition-all duration-500 rounded-full`}
                    style={{ width: `${d.score}%` }}
                  />
                </div>
              </div>
            ))}
          </div>

          {/* Active Blocker Alert */}
          {blockedTasks.length > 0 && (
            <div className="mt-5 p-3.5 bg-rose-50 border border-rose-200 rounded-xl flex items-start justify-between gap-3">
              <div className="flex items-start gap-2.5">
                <ShieldAlert className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="text-xs font-bold text-rose-900">Upstream Delay Affecting Technical Onboarding</h4>
                  <p className="text-xs text-rose-700 mt-0.5">
                    {blockedTasks[0].name} ({blockedTasks[0].department}) is stalled. Downstream technical accounts are blocked.
                  </p>
                </div>
              </div>
              <Link
                to="/simulator"
                className="px-3 py-1 bg-rose-600 hover:bg-rose-700 text-white rounded-lg text-xs font-semibold flex-shrink-0 transition-colors"
              >
                Simulate Fix
              </Link>
            </div>
          )}
        </div>
      </div>

      {/* Bottom Section: Active Onboarding Tasks & Quick Action */}
      <div className="bg-white rounded-xl border border-slate-200/80 p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-slate-900 text-base">Active Onboarding Tasks</h3>
            <p className="text-xs text-slate-500">Live workflow tasks for {activeEmployee?.full_name}</p>
          </div>
          <Link
            to="/workspace"
            className="text-xs font-semibold text-sky-600 hover:text-sky-700 flex items-center gap-1"
          >
            <span>Open Workspace</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-100 text-slate-400 font-semibold uppercase tracking-wider">
                <th className="pb-3 pl-1">Task ID</th>
                <th className="pb-3">Task Name</th>
                <th className="pb-3">Department</th>
                <th className="pb-3">Owner</th>
                <th className="pb-3">Due Date</th>
                <th className="pb-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {tasks.slice(0, 6).map((task) => (
                <tr key={task.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3 pl-1 font-mono text-slate-500">{task.task_id}</td>
                  <td className="py-3 font-semibold text-slate-900">{task.name}</td>
                  <td className="py-3"><DepartmentBadge department={task.department} /></td>
                  <td className="py-3 text-slate-600">{task.assigned_person}</td>
                  <td className="py-3 font-mono text-slate-500">{task.due_date}</td>
                  <td className="py-3"><StatusBadge status={task.status} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
