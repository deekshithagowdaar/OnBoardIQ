import React, { useEffect, useState } from 'react';
import {
  AlertTriangle,
  ShieldAlert,
  ArrowRight,
  TrendingDown,
  Layers,
  Clock,
  Sparkles,
  Info,
} from 'lucide-react';
import { Link } from 'react-router-dom';
import { StatusBadge } from '../components/StatusBadge';
import { DepartmentBadge } from '../components/DepartmentBadge';
import { apiClient } from '../api/client';
import { RiskPrediction, RootCauseAnalysis } from '../types';

interface Props {
  selectedEmployeeId: string;
}

export const RiskAnalysisPage: React.FC<Props> = ({ selectedEmployeeId }) => {
  const [riskData, setRiskData] = useState<RiskPrediction | null>(null);
  const [rootCause, setRootCause] = useState<RootCauseAnalysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAnalysis = async () => {
      if (!selectedEmployeeId) return;
      setLoading(true);
      try {
        const [rData, rcData] = await Promise.all([
          apiClient.getRiskAnalysis(selectedEmployeeId),
          apiClient.getRootCauseAnalysis(selectedEmployeeId),
        ]);
        setRiskData(rData);
        setRootCause(rcData);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalysis();
  }, [selectedEmployeeId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const isHighRisk = riskData?.overall_risk_score && riskData.overall_risk_score >= 50;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Predictive Delay & Risk Engine</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            AI-driven root-cause detection, downstream blast radius analysis, and timeline impact projection.
          </p>
        </div>
        <Link
          to="/simulator"
          className="inline-flex items-center gap-1.5 px-4 py-2 bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 text-white rounded-lg text-xs font-semibold shadow-sm transition-all"
        >
          <Sparkles className="w-3.5 h-3.5" />
          <span>Simulate Recovery Strategies</span>
          <ArrowRight className="w-3.5 h-3.5" />
        </Link>
      </div>

      {/* Top Cards: Risk Gauge & Root-Cause Card */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Gauge Card */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="font-bold text-slate-900 text-sm">Onboarding Risk Score</h3>
            <span
              className={`text-xs font-bold px-2.5 py-0.5 rounded-full ${
                riskData?.risk_category === 'Critical'
                  ? 'bg-rose-100 text-rose-800'
                  : riskData?.risk_category === 'High'
                  ? 'bg-amber-100 text-amber-800'
                  : 'bg-emerald-100 text-emerald-800'
              }`}
            >
              {riskData?.risk_category} Risk
            </span>
          </div>

          <div className="flex items-center gap-4 my-6">
            <div className="text-4xl font-black text-slate-900">
              {riskData?.overall_risk_score}%
            </div>
            <div className="space-y-0.5">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Attention Level</span>
              <p className="text-xs font-bold text-rose-600">{riskData?.attention_level}</p>
              <p className="text-xs text-slate-500">
                Est. Slippage: <strong className="text-slate-800">{riskData?.predicted_delay_days} Day(s)</strong>
              </p>
            </div>
          </div>

          <div className="space-y-2 pt-4 border-t border-slate-100">
            <span className="text-xs font-semibold text-slate-700 block">Diagnosed Risk Drivers:</span>
            <ul className="space-y-1.5 text-xs text-slate-600">
              {riskData?.factors?.map((f, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 rounded-full bg-rose-500 mt-1.5 flex-shrink-0" />
                  <span>{f}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* AI Root-Cause Investigation Card */}
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm lg:col-span-2">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <div className="p-2 rounded-lg bg-rose-50 text-rose-600">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <div>
                <h3 className="font-bold text-slate-900 text-base">Root-Cause Investigation</h3>
                <p className="text-xs text-slate-500">Upstream dependency graph traversal result</p>
              </div>
            </div>
            <span className="text-xs font-mono font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-lg">
              {rootCause?.root_cause_category}
            </span>
          </div>

          <div className="p-4 bg-slate-50/80 rounded-xl border border-slate-200/60 my-4 text-xs text-slate-700 leading-relaxed">
            <p className="font-medium">{rootCause?.explanation}</p>
          </div>

          {/* Blast Radius Breakdown */}
          <div className="space-y-3">
            <div className="flex items-center justify-between text-xs">
              <span className="font-semibold text-slate-700 flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-slate-400" />
                Downstream Blast Radius ({rootCause?.affected_downstream_tasks?.length || 0} Affected Tasks)
              </span>
              <span className="text-rose-600 font-semibold font-mono text-[11px]">
                +{rootCause?.estimated_joining_date_impact_days} Days Critical Path Impact
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
              {rootCause?.affected_downstream_tasks?.map((at) => (
                <div
                  key={at.task_id}
                  className="p-3 bg-white rounded-xl border border-slate-200/80 shadow-xs flex items-center justify-between"
                >
                  <div>
                    <div className="font-bold text-xs text-slate-900">{at.task_name}</div>
                    <div className="text-[11px] text-slate-500 flex items-center gap-1.5 mt-0.5">
                      <DepartmentBadge department={at.department} />
                      <span>{at.status}</span>
                    </div>
                  </div>
                  <div className="text-right font-mono text-xs font-semibold text-rose-600">
                    +{at.delay_impact_days}d
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Task Risk Assessment Table */}
      <div className="bg-white rounded-xl border border-slate-200/80 shadow-sm overflow-hidden">
        <div className="p-4 border-b border-slate-100">
          <h3 className="font-bold text-slate-900 text-sm">Task-Level Risk Breakdown</h3>
          <p className="text-xs text-slate-500 mt-0.5">Individual task delay probabilities and vulnerability weights</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-4">Task Name</th>
                <th className="py-3 px-4">Department</th>
                <th className="py-3 px-4">Status</th>
                <th className="py-3 px-4">Risk Weight</th>
                <th className="py-3 px-4">Delay Probability</th>
                <th className="py-3 px-4">Primary Vulnerability</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {riskData?.task_risks?.map((tr) => (
                <tr key={tr.task_id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3 px-4 font-bold text-slate-900">{tr.task_name}</td>
                  <td className="py-3 px-4"><DepartmentBadge department={tr.department} /></td>
                  <td className="py-3 px-4"><StatusBadge status={tr.status} /></td>
                  <td className="py-3 px-4">
                    <span className={`font-mono font-bold ${tr.risk_score >= 70 ? 'text-rose-600' : 'text-slate-700'}`}>
                      {tr.risk_score}%
                    </span>
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-600">
                    {Math.round(tr.delay_probability * 100)}%
                  </td>
                  <td className="py-3 px-4 text-slate-500 text-[11px]">
                    {tr.reasons[0] || 'Nominal progression'}
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
