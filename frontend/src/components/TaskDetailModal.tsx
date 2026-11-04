import React, { useState } from 'react';
import { X, CheckCircle, Clock, AlertTriangle, User } from 'lucide-react';
import { Task } from '../types';
import { DepartmentBadge } from './DepartmentBadge';
import { StatusBadge } from './StatusBadge';
import { apiClient } from '../api/client';

interface Props {
  task: Task | null;
  onClose: () => void;
  onTaskUpdated: () => void;
}

export const TaskDetailModal: React.FC<Props> = ({ task, onClose, onTaskUpdated }) => {
  if (!task) return null;

  const [status, setStatus] = useState(task.status);
  const [delayReason, setDelayReason] = useState(task.delay_reason || '');
  const [updating, setUpdating] = useState(false);

  const handleSave = async () => {
    setUpdating(true);
    try {
      await apiClient.updateTask(task.id, {
        status,
        delay_reason: delayReason || null,
        actual_completion_date: status === 'Completed' ? new Date().toISOString().split('T')[0] : null,
      });
      onTaskUpdated();
      onClose();
    } catch (err) {
      console.error(err);
    } finally {
      setUpdating(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-sm p-4">
      <div className="bg-white rounded-2xl shadow-xl border border-slate-200 w-full max-w-lg overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <div className="flex items-center gap-2">
            <span className="font-mono text-xs font-bold text-slate-500">{task.task_id}</span>
            <DepartmentBadge department={task.department} />
            <StatusBadge status={task.status} />
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100">
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-5">
          <div>
            <h3 className="text-lg font-bold text-slate-900 leading-snug">{task.name}</h3>
            <p className="mt-1.5 text-xs text-slate-600 leading-relaxed">{task.description}</p>
          </div>

          <div className="grid grid-cols-2 gap-4 p-4 bg-slate-50 rounded-xl border border-slate-100 text-xs">
            <div>
              <span className="text-slate-500 block mb-0.5">Assigned Owner</span>
              <span className="font-semibold text-slate-900 flex items-center gap-1.5">
                <User className="w-3.5 h-3.5 text-slate-400" /> {task.assigned_person}
              </span>
            </div>
            <div>
              <span className="text-slate-500 block mb-0.5">Priority & Criticality</span>
              <span className="font-semibold text-slate-900">
                {task.priority} {task.is_critical && '• Day-1 Critical'}
              </span>
            </div>
            <div>
              <span className="text-slate-500 block mb-0.5">Timeline Schedule</span>
              <span className="font-mono text-slate-700">
                {task.start_date} → {task.due_date}
              </span>
            </div>
            <div>
              <span className="text-slate-500 block mb-0.5">Est. Duration</span>
              <span className="font-semibold text-slate-900">{task.estimated_duration_days} Day(s)</span>
            </div>
          </div>

          {task.delay_reason && (
            <div className="p-3 bg-rose-50 border border-rose-200 rounded-xl text-xs text-rose-800 flex items-start gap-2">
              <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
              <div>
                <span className="font-bold block">Current Delay Diagnosis</span>
                <span>{task.delay_reason}</span>
              </div>
            </div>
          )}

          {/* Edit status form */}
          <div className="pt-2 border-t border-slate-100 space-y-3">
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider">
              Update Task Status
            </label>
            <div className="grid grid-cols-2 gap-2">
              {(['Pending', 'In Progress', 'Completed', 'Blocked', 'Delayed'] as const).map((s) => (
                <button
                  key={s}
                  type="button"
                  onClick={() => setStatus(s)}
                  className={`px-3 py-2 rounded-lg text-xs font-semibold border transition-all text-left flex items-center justify-between ${
                    status === s
                      ? 'border-sky-600 bg-sky-50 text-sky-700'
                      : 'border-slate-200 text-slate-600 hover:bg-slate-50'
                  }`}
                >
                  <span>{s}</span>
                  {status === s && <CheckCircle className="w-3.5 h-3.5 text-sky-600" />}
                </button>
              ))}
            </div>

            {(status === 'Delayed' || status === 'Blocked') && (
              <div>
                <label className="block text-xs font-medium text-slate-600 mb-1">Delay / Block Reason</label>
                <input
                  type="text"
                  value={delayReason}
                  onChange={(e) => setDelayReason(e.target.value)}
                  placeholder="e.g. Waiting on government ID scan re-upload"
                  className="w-full px-3 py-2 text-xs border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500"
                />
              </div>
            )}
          </div>
        </div>

        <div className="px-6 py-4 border-t border-slate-100 bg-slate-50/50 flex justify-end gap-2">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-200/60 rounded-lg transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            disabled={updating}
            className="px-4 py-2 text-xs font-medium bg-sky-600 hover:bg-sky-700 text-white rounded-lg shadow-sm transition-colors disabled:opacity-50"
          >
            {updating ? 'Saving Changes...' : 'Save & Recalculate Graph'}
          </button>
        </div>
      </div>
    </div>
  );
};
