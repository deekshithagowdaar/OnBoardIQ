import React, { useEffect, useState } from 'react';
import { Sparkles, Shield, UserCheck, RefreshCw } from 'lucide-react';
import { apiClient } from '../api/client';
import { Employee } from '../types';

interface Props {
  selectedEmployeeId: string;
  onSelectEmployee: (id: string) => void;
}

export const Navbar: React.FC<Props> = ({ selectedEmployeeId, onSelectEmployee }) => {
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [runningAgent, setRunningAgent] = useState(false);

  useEffect(() => {
    apiClient.getEmployees().then(setEmployees).catch(console.error);
  }, []);

  const handleRunOrchestration = async () => {
    if (!selectedEmployeeId) return;
    setRunningAgent(true);
    try {
      await apiClient.runOrchestrator(selectedEmployeeId);
      // reload or trigger update
      window.location.reload();
    } catch (err) {
      console.error(err);
    } finally {
      setRunningAgent(false);
    }
  };

  return (
    <header className="h-16 bg-white border-b border-slate-200/80 sticky top-0 z-30 flex items-center justify-between px-6">
      {/* Left Brand info */}
      <div className="flex items-center gap-3">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-sm font-bold text-lg">
          O
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="font-bold text-slate-900 text-base leading-tight">OnboardIQ</h1>
            <span className="text-[10px] font-semibold tracking-wider uppercase px-2 py-0.5 bg-sky-50 text-sky-700 border border-sky-200 rounded-full">
              Dayforce AI Challenge
            </span>
          </div>
          <p className="text-xs text-slate-500">Agentic AI Employee Onboarding Orchestrator</p>
        </div>
      </div>

      {/* Center & Right Controls */}
      <div className="flex items-center gap-4">
        {/* Active Employee Selector */}
        <div className="flex items-center gap-2 bg-slate-50 border border-slate-200 px-3 py-1.5 rounded-lg">
          <span className="text-xs font-medium text-slate-500">Active Profile:</span>
          <select
            value={selectedEmployeeId}
            onChange={(e) => onSelectEmployee(e.target.value)}
            className="bg-transparent text-xs font-semibold text-slate-800 focus:outline-none cursor-pointer"
          >
            {employees.map((emp) => (
              <option key={emp.id} value={emp.id}>
                {emp.full_name} ({emp.job_role} - {emp.department})
              </option>
            ))}
          </select>
        </div>

        {/* Coordinated Multi-Agent Trigger */}
        <button
          onClick={handleRunOrchestration}
          disabled={runningAgent}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-sky-600 to-blue-700 hover:from-sky-700 hover:to-blue-800 text-white rounded-lg text-xs font-medium shadow-sm transition-all disabled:opacity-50"
        >
          {runningAgent ? (
            <>
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              <span>Agents Coordinating...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-3.5 h-3.5" />
              <span>Run Agent Orchestration</span>
            </>
          )}
        </button>

        {/* User Identity Pill */}
        <div className="flex items-center gap-2 pl-3 border-l border-slate-200">
          <div className="w-8 h-8 rounded-full bg-slate-100 border border-slate-200 flex items-center justify-center text-slate-600 font-semibold text-xs">
            SJ
          </div>
          <div className="hidden md:block text-left">
            <p className="text-xs font-semibold text-slate-900 leading-tight">Sarah Johnson</p>
            <p className="text-[10px] text-slate-500 flex items-center gap-1">
              <Shield className="w-2.5 h-2.5 text-sky-600" /> Engineering Manager (Approver)
            </p>
          </div>
        </div>
      </div>
    </header>
  );
};
