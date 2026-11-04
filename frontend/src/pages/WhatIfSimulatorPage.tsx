import React, { useEffect, useState } from 'react';
import {
  Sliders,
  CheckCircle2,
  Clock,
  Zap,
  ShieldCheck,
  TrendingUp,
  Award,
  ArrowRight,
  Sparkles,
  Layers,
  FileCheck,
} from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { apiClient } from '../api/client';
import { WhatIfComparison, SimulationScenario } from '../types';

interface Props {
  selectedEmployeeId: string;
}

export const WhatIfSimulatorPage: React.FC<Props> = ({ selectedEmployeeId }) => {
  const [data, setData] = useState<WhatIfComparison | null>(null);
  const [selectedScenarioKey, setSelectedScenarioKey] = useState<string>('scenario_a');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchSims = async () => {
      if (!selectedEmployeeId) return;
      setLoading(true);
      try {
        const res = await apiClient.getSimulations(selectedEmployeeId);
        setData(res);
        if (res.recommended_strategy) {
          setSelectedScenarioKey(res.recommended_strategy.recommended_scenario_key);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchSims();
  }, [selectedEmployeeId]);

  const handleProceedToApproval = () => {
    navigate('/approvals');
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const rec = data?.recommended_strategy;
  const activeScenario = data?.scenarios?.find((s) => s.scenario_key === selectedScenarioKey) || data?.scenarios?.[0];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white p-6 rounded-2xl border border-slate-200/80 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-slate-900">Onboarding What-If Simulator</h2>
            <span className="text-[11px] font-semibold px-2.5 py-0.5 bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-full flex items-center gap-1">
              <Sparkles className="w-3 h-3 text-indigo-600" /> Ephemeral Sandbox Engine
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1 max-w-2xl leading-relaxed">
            Evaluate alternative recovery interventions before executing production workflow mutations.
            Simulations calculate unblocked dependencies, schedule compression, and compliance constraints in isolation.
          </p>
        </div>

        <div className="flex items-center gap-4 bg-slate-50 px-4 py-3 rounded-xl border border-slate-200/60">
          <div>
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Baseline Readiness</span>
            <span className="text-lg font-black text-slate-900">{data?.baseline_readiness_score}%</span>
          </div>
          <div className="w-px h-8 bg-slate-200" />
          <div>
            <span className="text-[10px] uppercase font-bold text-slate-400 block">Baseline Risk</span>
            <span className="text-xs font-bold text-rose-600">{data?.baseline_risk_level} Risk</span>
          </div>
        </div>
      </div>

      {/* AI Recovery Optimizer Recommendation Callout */}
      {rec && (
        <div className="p-5 bg-gradient-to-r from-sky-50 via-indigo-50 to-blue-50 border border-sky-200 rounded-2xl shadow-sm">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-start gap-3">
              <div className="p-2.5 rounded-xl bg-sky-600 text-white shadow-sm flex-shrink-0 mt-0.5">
                <Award className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-bold uppercase tracking-wider text-sky-800">
                    Recommended Recovery Strategy
                  </span>
                  <span className="text-[10px] font-semibold px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded-full">
                    Highest Utility Score
                  </span>
                </div>
                <h3 className="text-base font-bold text-slate-900 mt-0.5">{rec.strategy_title}</h3>
                <p className="text-xs text-slate-700 mt-1 leading-relaxed max-w-3xl">
                  {rec.rationale}
                </p>
              </div>
            </div>

            <button
              onClick={handleProceedToApproval}
              className="px-4 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-xl text-xs font-bold shadow-md transition-all flex items-center gap-2 flex-shrink-0"
            >
              <FileCheck className="w-4 h-4" />
              <span>Review & Approve Action</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Scenarios Side-by-Side Comparison Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {data?.scenarios?.map((scenario) => {
          const isSelected = scenario.scenario_key === selectedScenarioKey;
          const isWinner = scenario.scenario_key === rec?.recommended_scenario_key;

          return (
            <div
              key={scenario.scenario_key}
              onClick={() => setSelectedScenarioKey(scenario.scenario_key)}
              className={`bg-white rounded-2xl border p-5 shadow-sm transition-all cursor-pointer relative text-left flex flex-col justify-between ${
                isSelected
                  ? 'border-sky-600 ring-2 ring-sky-100 shadow-md'
                  : 'border-slate-200/80 hover:border-slate-300'
              }`}
            >
              <div>
                {/* Header tag */}
                <div className="flex items-center justify-between mb-3">
                  <span className="font-mono text-xs font-bold text-slate-400 uppercase tracking-wider">
                    {scenario.scenario_key.replace('_', ' ')}
                  </span>
                  {isWinner && (
                    <span className="text-[10px] font-bold px-2 py-0.5 bg-sky-100 text-sky-800 rounded-full flex items-center gap-1">
                      <Zap className="w-3 h-3 text-sky-600" /> Optimal
                    </span>
                  )}
                </div>

                <h4 className="font-bold text-sm text-slate-900 leading-snug">
                  {scenario.scenario_title}
                </h4>

                <p className="text-xs text-slate-500 mt-2 leading-relaxed line-clamp-3">
                  {scenario.description}
                </p>

                {/* Metrics Matrix */}
                <div className="mt-4 pt-3 border-t border-slate-100 space-y-2 text-xs">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Tasks Unblocked:</span>
                    <span className="font-bold text-slate-900 font-mono">
                      {scenario.unblocked_count} Task(s)
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Timeline Compression:</span>
                    <span className="font-bold text-emerald-600 font-mono">
                      +{scenario.time_saved_days} Days Saved
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Projected Readiness:</span>
                    <span className="font-black text-sky-600 font-mono text-sm">
                      {scenario.readiness_score_projected}%
                    </span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-slate-500">Policy Compliance:</span>
                    <span className="font-semibold text-emerald-700 flex items-center gap-1 text-[11px]">
                      <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" /> 100% Compliant
                    </span>
                  </div>
                </div>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-400">Action: {scenario.action_type}</span>
                <span className={`font-semibold ${isSelected ? 'text-sky-600' : 'text-slate-400'}`}>
                  {isSelected ? 'Selected' : 'Click to inspect'}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Deep-Dive Inspection Panel for Active Scenario */}
      {activeScenario && (
        <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-bold text-slate-900 text-base">
                Scenario Breakdown: {activeScenario.scenario_title}
              </h3>
              <p className="text-xs text-slate-500 mt-0.5">
                Simulated downstream state adaptations and department parity projections
              </p>
            </div>
            <span className="text-xs font-mono font-semibold px-2.5 py-1 bg-slate-100 text-slate-700 rounded-lg">
              Feasibility Rating: {Math.round(activeScenario.feasibility_score * 100)}%
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 my-4">
            {Object.entries(activeScenario.department_readiness || {}).map(([dept, score]) => (
              <div key={dept} className="p-3 bg-slate-50 rounded-xl border border-slate-100">
                <span className="text-xs font-semibold text-slate-500 block mb-1">{dept} Readiness</span>
                <span className="text-lg font-bold text-slate-900">{score}%</span>
                <div className="h-1.5 w-full bg-slate-200 rounded-full mt-2 overflow-hidden">
                  <div className="h-full bg-sky-600 rounded-full" style={{ width: `${score}%` }} />
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 flex items-center justify-between gap-4 mt-4">
            <div className="text-xs text-slate-600">
              <span className="font-bold text-slate-900 block">Approval Checkpoint Requirement:</span>
              Manager approval (Sarah Johnson) is required before this self-healing workflow adaptation can be dispatched to department APIs.
            </div>
            <button
              onClick={handleProceedToApproval}
              className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-xs font-bold transition-colors shadow-sm flex items-center gap-1.5 flex-shrink-0"
            >
              <span>Go to Approvals Center</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
