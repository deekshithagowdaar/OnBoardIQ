import React from 'react';

interface Props {
  department: string;
}

export const DepartmentBadge: React.FC<Props> = ({ department }) => {
  const getColors = () => {
    switch (department) {
      case 'HR':
      case 'Human Resources':
        return 'bg-purple-50 text-purple-700 border-purple-200';
      case 'IT':
      case 'Information Technology':
        return 'bg-cyan-50 text-cyan-700 border-cyan-200';
      case 'Payroll':
      case 'Finance':
      case 'Finance & Payroll':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'Benefits':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'Engineering':
        return 'bg-indigo-50 text-indigo-700 border-indigo-200';
      case 'Product':
      case 'Product Management':
        return 'bg-pink-50 text-pink-700 border-pink-200';
      case 'Sales':
      case 'Sales & Go-to-Market':
        return 'bg-blue-50 text-blue-700 border-blue-200';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-200';
    }
  };

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold border ${getColors()}`}>
      {department}
    </span>
  );
};
