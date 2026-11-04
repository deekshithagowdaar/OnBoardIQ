import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import { DepartmentBadge } from './DepartmentBadge';
import { StatusBadge } from './StatusBadge';
import { AlertTriangle, Clock, User } from 'lucide-react';

export const CustomTaskNode = memo(({ data }: { data: any }) => {
  const isBlocked = data.is_blocked || data.status === 'Blocked' || data.status === 'Delayed';
  const isCompleted = data.status === 'Completed';

  let borderColor = 'border-slate-200';
  if (data.status === 'Completed') borderColor = 'border-emerald-300';
  else if (data.status === 'Delayed') borderColor = 'border-rose-400 ring-2 ring-rose-100';
  else if (data.status === 'Blocked') borderColor = 'border-amber-400 ring-2 ring-amber-100';
  else if (data.status === 'In Progress') borderColor = 'border-blue-400 ring-2 ring-blue-100';

  return (
    <div className={`w-64 bg-white rounded-xl shadow-md border ${borderColor} p-3 transition-all hover:shadow-lg text-left`}>
      <Handle type="target" position={Position.Left} className="w-3 h-3 bg-slate-400 border-2 border-white" />
      
      <div className="flex items-center justify-between gap-1 mb-2">
        <DepartmentBadge department={data.department} />
        <StatusBadge status={data.status} size="sm" />
      </div>

      <div className="font-semibold text-sm text-slate-900 leading-snug line-clamp-2">
        {data.name}
      </div>

      {isBlocked && data.delay_reason && (
        <div className="mt-2 p-1.5 bg-rose-50 border border-rose-200/60 rounded-md flex items-start gap-1.5 text-[11px] text-rose-800">
          <AlertTriangle className="w-3.5 h-3.5 text-rose-600 flex-shrink-0 mt-0.5" />
          <span className="line-clamp-2 font-medium">{data.delay_reason}</span>
        </div>
      )}

      <div className="mt-3 pt-2 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <div className="flex items-center gap-1 truncate max-w-[120px]">
          <User className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
          <span className="truncate">{data.assigned_person?.split(' ')[0]}</span>
        </div>
        <div className="flex items-center gap-1 font-mono text-[11px]">
          <Clock className="w-3 h-3 text-slate-400" />
          <span>{data.due_date?.slice(5)}</span>
        </div>
      </div>

      <Handle type="source" position={Position.Right} className="w-3 h-3 bg-slate-400 border-2 border-white" />
    </div>
  );
});
