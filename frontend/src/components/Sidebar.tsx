import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Users,
  Briefcase,
  GitBranch,
  AlertOctagon,
  Sliders,
  CheckCircle2,
  Gauge,
  LineChart,
} from 'lucide-react';

const navItems = [
  { path: '/', label: 'Main Dashboard', icon: LayoutDashboard },
  { path: '/employees', label: 'Employee Management', icon: Users },
  { path: '/workspace', label: 'Onboarding Workspace', icon: Briefcase },
  { path: '/graph', label: 'Dependency Graph', icon: GitBranch },
  { path: '/risk', label: 'Risk & Root-Cause', icon: AlertOctagon },
  { path: '/simulator', label: 'What-If Simulator', icon: Sliders },
  { path: '/approvals', label: 'Recovery & Approvals', icon: CheckCircle2 },
  { path: '/readiness', label: 'Readiness Dashboard', icon: Gauge },
  { path: '/analytics', label: 'Learning & Analytics', icon: LineChart },
];

export const Sidebar: React.FC = () => {
  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col flex-shrink-0 min-h-screen border-r border-slate-800">
      <div className="p-4 border-b border-slate-800">
        <div className="text-[11px] font-semibold tracking-wider text-slate-400 uppercase">
          Navigation Modules
        </div>
      </div>

      <nav className="p-3 space-y-1 flex-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-sky-600 text-white shadow-sm shadow-sky-900/50'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`
              }
            >
              <Icon className="w-4 h-4 flex-shrink-0" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer Info Box */}
      <div className="p-4 m-3 bg-slate-800/60 rounded-xl border border-slate-700/60 text-xs text-slate-400">
        <p className="font-semibold text-slate-200 text-xs mb-1">Hackathon Prototype</p>
        <p className="text-[11px] leading-relaxed text-slate-400">
          Powered by LangGraph multi-agent orchestration, dynamic graph engine, and predictive risk scoring.
        </p>
      </div>
    </aside>
  );
};
