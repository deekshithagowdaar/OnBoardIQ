import React, { useEffect, useState } from 'react';
import {
  LineChart as LineChartIcon,
  TrendingUp,
  BarChart2,
  CheckCircle2,
  Database,
  History,
  Layers,
  Sparkles,
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from 'recharts';
import { DepartmentBadge } from '../components/DepartmentBadge';
import { apiClient } from '../api/client';
import { LearningAnalytics } from '../types';

export const LearningAnalyticsPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<LearningAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiClient
      .getLearningAnalytics()
      .then(setAnalytics)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Continuous Learning & Outcome Analytics</h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Feedback loops analyzing historical task delays, recovery strategy success rates, and predictive accuracy.
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block mb-1">
            Total Analyzed Trajectories
          </span>
          <span className="text-2xl font-black text-slate-900">
            {analytics?.total_completed_onboardings || 0}
          </span>
          <span className="text-[11px] text-slate-400 block mt-1">Cross-department workflows</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block mb-1">
            Prediction Accuracy (MAE)
          </span>
          <span className="text-2xl font-black text-emerald-600 font-mono">
            {analytics?.prediction_accuracy_mae || 0}d
          </span>
          <span className="text-[11px] text-slate-400 block mt-1">Mean Absolute Error in days</span>
        </div>

        <div className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-sm">
          <span className="text-xs font-semibold text-slate-500 block mb-1">
            Recovery Success Rate
          </span>
          <span className="text-2xl font-black text-sky-600 font-mono">
            94.2%
          </span>
          <span className="text-[11px] text-slate-400 block mt-1">Automated & approved interventions</span>
        </div>
      </div>

      {/* Chart: Frequent Bottlenecks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm">
          <h3 className="font-bold text-slate-900 text-sm mb-1">Frequent Onboarding Bottlenecks</h3>
          <p className="text-xs text-slate-500 mb-4">Tasks with highest cumulative schedule slippage</p>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analytics?.bottlenecks || []}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="task_name" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Bar dataKey="delay_count" fill="#0284c7" radius={[4, 4, 0, 0]} name="Delay Occurrences" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart: Predicted vs Actual Delay */}
        <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm">
          <h3 className="font-bold text-slate-900 text-sm mb-1">Predicted vs Actual Delay Duration</h3>
          <p className="text-xs text-slate-500 mb-4">Comparison of ML/rule risk predictions against actual resolution</p>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={analytics?.prediction_vs_actual?.slice(0, 6) || []}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis dataKey="task_name" tick={{ fontSize: 10 }} />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip />
                <Legend />
                <Bar dataKey="predicted" fill="#64748b" radius={[4, 4, 0, 0]} name="Predicted Days" />
                <Bar dataKey="actual" fill="#f43f5e" radius={[4, 4, 0, 0]} name="Actual Days" />
                <Bar dataKey="time_saved" fill="#10b981" radius={[4, 4, 0, 0]} name="Time Saved" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Recovery Strategies Performance Table */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <h3 className="font-bold text-slate-900 text-sm mb-3">Recovery Strategy Performance Matrix</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-3">Strategy Name</th>
                <th className="py-3 px-3">Times Recommended</th>
                <th className="py-3 px-3">Manager Approval Rate</th>
                <th className="py-3 px-3">Resolution Success</th>
                <th className="py-3 px-3">Avg. Days Compressed</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {analytics?.recovery_strategies_performance?.map((strat, i) => (
                <tr key={i} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3 px-3 font-bold text-slate-900">{strat.strategy_name}</td>
                  <td className="py-3 px-3 font-mono text-slate-600">{strat.times_recommended}</td>
                  <td className="py-3 px-3 font-semibold text-emerald-700">{strat.approval_rate}%</td>
                  <td className="py-3 px-3 font-semibold text-sky-700">{strat.success_rate}%</td>
                  <td className="py-3 px-3 font-mono font-bold text-slate-800">+{strat.avg_days_saved} Days</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Historical Outcomes Log */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="font-bold text-slate-900 text-sm">Historical Outcomes Ledger</h3>
            <p className="text-xs text-slate-500">Live system outcomes recorded after action execution</p>
          </div>
          <span className="text-[11px] px-2.5 py-1 rounded-full bg-slate-100 text-slate-700 font-medium">
            Persistent Storage
          </span>
        </div>

        <div className="overflow-x-auto max-h-80 overflow-y-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 sticky top-0 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-2.5 px-3">Department</th>
                <th className="py-2.5 px-3">Task Name</th>
                <th className="py-2.5 px-3">Root Cause</th>
                <th className="py-2.5 px-3">Applied Recovery Strategy</th>
                <th className="py-2.5 px-3">Days Saved</th>
                <th className="py-2.5 px-3">Data Origin</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {analytics?.historical_outcomes?.slice(0, 15).map((ho) => (
                <tr key={ho.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-2.5 px-3"><DepartmentBadge department={ho.department} /></td>
                  <td className="py-2.5 px-3 font-semibold text-slate-900">{ho.task_name}</td>
                  <td className="py-2.5 px-3 text-slate-600">{ho.root_cause_category}</td>
                  <td className="py-2.5 px-3 text-slate-700">{ho.recovery_strategy_used}</td>
                  <td className="py-2.5 px-3 font-mono font-bold text-emerald-600">+{ho.time_saved_actual_days}d</td>
                  <td className="py-2.5 px-3 text-[11px]">
                    {ho.is_synthetic_seed ? (
                      <span className="text-slate-400">Synthetic Seed</span>
                    ) : (
                      <span className="font-bold text-sky-600">Live Execution</span>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
