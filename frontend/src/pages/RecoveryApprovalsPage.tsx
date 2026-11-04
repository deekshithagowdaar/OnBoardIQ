import React, { useEffect, useState } from 'react';
import {
  CheckCircle2,
  XCircle,
  Clock,
  Shield,
  FileCheck,
  AlertTriangle,
  History,
  Check,
  Zap,
} from 'lucide-react';
import { StatusBadge } from '../components/StatusBadge';
import { apiClient } from '../api/client';
import { ApprovalRequest, AuditLog } from '../types';

interface Props {
  selectedEmployeeId: string;
}

export const RecoveryApprovalsPage: React.FC<Props> = ({ selectedEmployeeId }) => {
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [auditLogs, setAuditLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [actionSuccess, setActionSuccess] = useState<string | null>(null);

  const loadData = async () => {
    try {
      const [appRes, logsRes] = await Promise.all([
        apiClient.getApprovals(selectedEmployeeId || undefined),
        apiClient.getAuditLogs(selectedEmployeeId || undefined),
      ]);
      setApprovals(appRes);
      setAuditLogs(logsRes);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedEmployeeId]);

  const handleDecision = async (approvalId: string, status: 'Approved' | 'Rejected') => {
    try {
      const note = status === 'Approved'
        ? 'Approved by Sarah Johnson (Engineering Manager) for Day-1 developer onboarding acceleration.'
        : 'Action rejected due to policy restrictions.';
      await apiClient.decideApproval(approvalId, status, note);
      setActionSuccess(
        status === 'Approved'
          ? 'Action successfully executed! Upstream blockers resolved and downstream task graph updated.'
          : 'Approval request rejected. No workflow mutations applied.'
      );
      loadData();
    } catch (err) {
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  const pendingApprovals = approvals.filter((a) => a.status === 'Pending');
  const pastApprovals = approvals.filter((a) => a.status !== 'Pending');

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Recovery & Approval Center</h2>
        <p className="text-xs text-slate-500 mt-0.5">
          Human-in-the-loop checkpoints for AI recovery interventions. Sensitive actions require explicit authorization.
        </p>
      </div>

      {actionSuccess && (
        <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-800 flex items-center justify-between animate-in fade-in">
          <div className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
            <span className="font-semibold">{actionSuccess}</span>
          </div>
          <button
            onClick={() => setActionSuccess(null)}
            className="text-emerald-700 hover:text-emerald-900 font-bold"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Pending Approvals Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Clock className="w-4 h-4 text-amber-500" />
            <span>Pending Authorization Requests ({pendingApprovals.length})</span>
          </h3>
          <span className="text-xs font-medium text-slate-500">
            Current Role: <strong className="text-slate-800">Sarah Johnson (Engineering Manager)</strong>
          </span>
        </div>

        {pendingApprovals.length === 0 ? (
          <div className="p-8 bg-white rounded-2xl border border-slate-200/80 text-center shadow-xs">
            <CheckCircle2 className="w-10 h-10 text-emerald-500 mx-auto mb-2 opacity-80" />
            <h4 className="font-bold text-slate-800 text-sm">No Pending Approvals</h4>
            <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
              All proposed self-healing actions have been processed or no bottlenecks require intervention.
            </p>
          </div>
        ) : (
          pendingApprovals.map((req) => (
            <div
              key={req.id}
              className="bg-white rounded-2xl border border-amber-200/80 p-6 shadow-sm ring-1 ring-amber-100"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[11px] font-mono font-bold bg-amber-50 text-amber-800 border border-amber-200">
                    {req.action_type}
                  </span>
                  <StatusBadge status={req.status} />
                </div>
                <span className="text-xs text-slate-400">
                  Requested by: <strong className="text-slate-700">{req.requested_by}</strong>
                </span>
              </div>

              <div className="my-4">
                <h4 className="text-base font-bold text-slate-900">{req.title}</h4>
                <p className="text-xs text-slate-600 mt-1.5 leading-relaxed">{req.description}</p>
              </div>

              {/* Justification & Impact box */}
              <div className="p-4 bg-slate-50 rounded-xl border border-slate-100 text-xs space-y-2 mb-5">
                <div>
                  <span className="font-bold text-slate-700 block mb-0.5">Automated Recovery Justification</span>
                  <p className="text-slate-600 leading-relaxed">{req.justification}</p>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-100">
                <button
                  onClick={() => handleDecision(req.id, 'Rejected')}
                  className="px-4 py-2 border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold transition-colors flex items-center gap-1.5"
                >
                  <XCircle className="w-4 h-4 text-rose-500" />
                  <span>Reject Action</span>
                </button>
                <button
                  onClick={() => handleDecision(req.id, 'Approved')}
                  className="px-5 py-2 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold shadow-sm transition-colors flex items-center gap-1.5"
                >
                  <Zap className="w-4 h-4" />
                  <span>Approve & Execute Self-Healing Action</span>
                </button>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Decision History & Audit Trail */}
      <div className="bg-white rounded-2xl border border-slate-200/80 p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-4">
          <History className="w-4 h-4 text-slate-500" />
          <h3 className="text-sm font-bold text-slate-900">Execution History & Audit Log</h3>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-slate-100 text-slate-500 font-semibold uppercase tracking-wider">
              <tr>
                <th className="py-3 px-3">Timestamp</th>
                <th className="py-3 px-3">Entity</th>
                <th className="py-3 px-3">Action</th>
                <th className="py-3 px-3">Actor</th>
                <th className="py-3 px-3">Outcome Summary</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 font-medium">
              {auditLogs.slice(0, 8).map((log) => (
                <tr key={log.id} className="hover:bg-slate-50/60 transition-colors">
                  <td className="py-3 px-3 font-mono text-slate-500">{log.timestamp?.slice(0, 19).replace('T', ' ')}</td>
                  <td className="py-3 px-3 font-bold text-slate-800">{log.entity_type}</td>
                  <td className="py-3 px-3">
                    <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-slate-100 text-slate-800">
                      {log.action}
                    </span>
                  </td>
                  <td className="py-3 px-3 text-slate-700">{log.actor}</td>
                  <td className="py-3 px-3 text-slate-600 truncate max-w-xs">
                    {log.details?.summary || log.details?.title || log.details?.name || JSON.stringify(log.details)}
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
