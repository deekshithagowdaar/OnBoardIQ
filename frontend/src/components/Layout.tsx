import React from 'react';
import { Navbar } from './Navbar';
import { Sidebar } from './Sidebar';

interface Props {
  selectedEmployeeId: string;
  onSelectEmployee: (id: string) => void;
  children: React.ReactNode;
}

export const Layout: React.FC<Props> = ({
  selectedEmployeeId,
  onSelectEmployee,
  children,
}) => {
  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      <Sidebar />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <Navbar
          selectedEmployeeId={selectedEmployeeId}
          onSelectEmployee={onSelectEmployee}
        />
        <main className="flex-1 overflow-y-auto p-8">
          <div className="max-w-7xl mx-auto">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};
