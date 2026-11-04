import React, { useEffect, useState } from 'react';
import {
  Gauge,
  CheckCircle2,
  AlertTriangle,
  Clock,
  Calendar,
  Layers,
  Info,
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { DepartmentBadge } from '../components/DepartmentBadge';
import { apiClient } from '../api/client';
import { ReadinessData } from '../types';

interface Props {
  selectedEmployeeId: string;
}

export const ReadinessDashboardPage: React.FC<Props> = ({ selectedEmployeeId }) => {
  const [readiness, setReadiness] = useState<ReadinessData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchReadiness = async () => {
      if (!selectedEmployeeId) return;
      setLoading(true);
      try {
        const data = await apiClient.getReadiness(selectedEmployeeId);
        setReadiness(data);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReadiness();
  }, [selectedEmployeeId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const score = readiness?.overall_score || 0;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Dynamic Onboarding Readiness Score</h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Explainable Day-1 readiness calculation weighted by completion, critical path health, and blocker deductions.
        </p>
      </div>

      {/* Main Readiness Gauge Hero Card */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-8 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="flex items-center gap-6">
            <div className="relative w-32 h-32 rounded-full border-8 border-slate-100 flex items-center justify-center shadow-inner">
              <div
                className={`text-4xl font-black ${
                  score >= 80 ? 'text-emerald-600' : score >= 50 ? 'text-amber-500' : 'text-rose-600'
                }`}
              >
                {score}%
              </div>
            </div>

            <div className="space-y-1">
              <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">Readiness Tier</span>
              <h3 className="text-2xl font-extrabold text-slate-900">{readiness?.readiness_tier}</h3>
              <p className="text-xs text-slate-500 max-w-md leading-relaxed mt-1">
                {readiness?.score_explanation}
              </p>
            </div>
          </div>

          {/* Key Metrics Chips */}
          <div className="grid grid-cols-2 gap-3 text-xs min-w-[240px]">
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <span className="text-slate-400 block mb-0.5">Completed Tasks</span>
              <span className="text-base font-bold text-slate-900">
                {readiness?.completed_tasks_count} / {readiness?.total_tasks_count}
              </span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <span className="text-slate-400 block mb-0.5">Active Blockers</span>
              <span className={`text-base font-bold ${readiness?.blocked_tasks_count ? 'text-rose-600' : 'text-slate-900'}`}>
                {readiness?.blocked_tasks_count}
              </span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <span className="text-slate-400 block mb-0.5">Critical Pending</span>
              <span className="text-base font-bold text-amber-600">
                {readiness?.critical_pending_count}
              </span>
            </div>
            <div className="p-3 bg-slate-50 rounded-xl border border-slate-100">
              <span className="text-slate-400 block mb-0.5">Days to Joining</span>
              <span className="text-base font-bold text-slate-900">
                {readiness?.days_until_joining} Days
              </span>
            </div>
          </div>
        </div>

        {/* Explainable Formula Breakdown */}
        {readiness?.formula_breakdown && (
          <div className="mt-8 pt-6 border-t border-slate-100">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">
              Mathematical Score Formulation:
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-slate-500 block">35% Task Completion</span>
                <span className="font-mono font-bold text-slate-800">
                  +{readiness.formula_breakdown.completion_ratio_component} pts
                </span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-slate-500 block">25% Critical Health</span>
                <span className="font-mono font-bold text-slate-800">
                  +{readiness.formula_breakdown.critical_health_component} pts
                </span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-slate-500 block">20% Dept Parity</span>
                <span className="font-mono font-bold text-slate-800">
                  +{readiness.formula_breakdown.department_parity_component} pts
                </span>
              </div>
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-100">
                <span className="text-slate-500 block">20% Timeline / Blocker</span>
                <span className="font-mono font-bold text-slate-800">
                  +{readiness.formula_breakdown.timeline_component} pts
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Department Readiness & Critical Path Checklist */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Department Readiness Cards */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm">Department-Specific Readiness</h3>
          <div className="space-y-3">
            {Object.entries(readiness?.department_scores || {}).map(([dept, dScore]) => (
              <div key={dept} className="space-y-1">
                <div className="flex justify-between text-xs font-medium">
                  <span className="text-slate-700">{dept} Readiness</span>
                  <span className="font-bold text-slate-900">{dScore}%</span>
                </div>
                <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className="h-full bg-sky-600 rounded-full transition-all duration-300"
                    style={{ width: `${dScore}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Critical Path Tasks */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm space-y-4">
          <h3 className="font-bold text-slate-900 text-sm">Critical Path Sequence</h3>
          <div className="space-y-2.5">
            {readiness?.critical_path_tasks?.map((ct, idx) => (
              <div
                key={ct.id}
                className="p-3 rounded-xl border border-slate-100 bg-slate-50/60 flex items-center justify-between text-xs"
              >
                <div className="flex items-center gap-2">
                  <span className="w-5 h-5 rounded-full bg-slate-200 font-mono font-bold flex items-center justify-center text-[10px] text-slate-700">
                    {idx + 1}
                  </span>
                  <div>
                    <span className="font-semibold text-slate-900 block">{ct.name}</span>
                    <span className="text-[11px] text-slate-400">{ct.department}</span>
                  </div>
                </div>
                <StatusBadge status={ct.status} />
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
