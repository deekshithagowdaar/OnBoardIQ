import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { DashboardPage } from './pages/DashboardPage';
import { EmployeeManagementPage } from './pages/EmployeeManagementPage';
import { OnboardingWorkspacePage } from './pages/OnboardingWorkspacePage';
import { DependencyGraphPage } from './pages/DependencyGraphPage';
import { RiskAnalysisPage } from './pages/RiskAnalysisPage';
import { WhatIfSimulatorPage } from './pages/WhatIfSimulatorPage';
import { RecoveryApprovalsPage } from './pages/RecoveryApprovalsPage';
import { ReadinessDashboardPage } from './pages/ReadinessDashboardPage';
import { LearningAnalyticsPage } from './pages/LearningAnalyticsPage';

export function App() {
  const [selectedEmployeeId, setSelectedEmployeeId] = useState<string>('emp-alex-001');

  return (
    <BrowserRouter>
      <Layout
        selectedEmployeeId={selectedEmployeeId}
        onSelectEmployee={setSelectedEmployeeId}
      >
        <Routes>
          <Route path="/" element={<DashboardPage selectedEmployeeId={selectedEmployeeId} />} />
          <Route
            path="/employees"
            element={<EmployeeManagementPage onSelectEmployee={setSelectedEmployeeId} />}
          />
          <Route
            path="/workspace"
            element={<OnboardingWorkspacePage selectedEmployeeId={selectedEmployeeId} />}
          />
          <Route
            path="/graph"
            element={<DependencyGraphPage selectedEmployeeId={selectedEmployeeId} />}
          />
          <Route
            path="/risk"
            element={<RiskAnalysisPage selectedEmployeeId={selectedEmployeeId} />}
          />
          <Route
            path="/simulator"
            element={<WhatIfSimulatorPage selectedEmployeeId={selectedEmployeeId} />}
          />
          <Route
            path="/approvals"
            element={<RecoveryApprovalsPage selectedEmployeeId={selectedEmployeeId} />}
          />
          <Route
            path="/readiness"
            element={<ReadinessDashboardPage selectedEmployeeId={selectedEmployeeId} />}
          />
          <Route path="/analytics" element={<LearningAnalyticsPage />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

export default App;
