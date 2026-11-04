import React from 'react';

interface Props {
  status: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<Props> = ({ status, size = 'sm' }) => {
  const getColors = () => {
    switch (status) {
      case 'Completed':
      case 'Ready':
      case 'Approved':
      case 'Success':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'In Progress':
      case 'Onboarding':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      case 'Delayed':
      case 'At Risk':
      case 'Critical':
      case 'Rejected':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'Blocked':
      case 'High':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'Pending':
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  const px = size === 'sm' ? 'px-2 py-0.5 text-xs' : 'px-3 py-1 text-sm';

  return (
    <span className={`inline-flex items-center font-medium rounded-full border ${px} ${getColors()}`}>
      <span className="w-1.5 h-1.5 rounded-full mr-1.5 bg-current opacity-80" />
      {status}
    </span>
  );
};
