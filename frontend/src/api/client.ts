import axios from 'axios';
import {
  Employee,
  Task,
  DependencyGraphData,
  RiskPrediction,
  RootCauseAnalysis,
  WhatIfComparison,
  ApprovalRequest,
  ReadinessData,
  LearningAnalytics
} from '../types';

const api = axios.create({
  baseURL: (import.meta as any).env?.VITE_API_BASE_URL || '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiClient = {
  // Employees
  getEmployees: async (search?: string, department?: string, status?: string): Promise<Employee[]> => {
    const res = await api.get('/employees', { params: { search, department, status } });
    return res.data;
  },
  getEmployee: async (id: string): Promise<Employee> => {
    const res = await api.get(`/employees/${id}`);
    return res.data;
  },
  createEmployee: async (data: Partial<Employee>): Promise<Employee> => {
    const res = await api.post('/employees', data);
    return res.data;
  },
  updateEmployee: async (id: string, data: Partial<Employee>): Promise<Employee> => {
    const res = await api.put(`/employees/${id}`, data);
    return res.data;
  },
  generatePlan: async (employeeId: string) => {
    const res = await api.post(`/employees/${employeeId}/generate-plan`);
    return res.data;
  },

  // Tasks
  getTasks: async (employeeId: string): Promise<Task[]> => {
    const res = await api.get(`/tasks/employee/${employeeId}`);
    return res.data;
  },
  updateTask: async (taskId: string, data: Partial<Task>): Promise<Task> => {
    const res = await api.put(`/tasks/${taskId}`, data);
    return res.data;
  },
  addDependency: async (data: { task_id: string; depends_on_task_id: string; dependency_type?: string }) => {
    const res = await api.post('/tasks/dependencies', data);
    return res.data;
  },

  // Dependency Graph
  getDependencyGraph: async (employeeId: string): Promise<DependencyGraphData> => {
    const res = await api.get(`/dependency/${employeeId}/graph`);
    return res.data;
  },

  // Risk & Root Cause
  getRiskAnalysis: async (employeeId: string): Promise<RiskPrediction> => {
    const res = await api.get(`/risk/${employeeId}`);
    return res.data;
  },
  getRootCauseAnalysis: async (employeeId: string): Promise<RootCauseAnalysis> => {
    const res = await api.get(`/root-cause/${employeeId}`);
    return res.data;
  },

  // What-If Simulation
  getSimulations: async (employeeId: string): Promise<WhatIfComparison> => {
    const res = await api.get(`/simulation/${employeeId}/scenarios`);
    return res.data;
  },
  runCustomSimulation: async (employeeId: string, action_type: string, parameters: any = {}) => {
    const res = await api.post(`/simulation/${employeeId}/run-custom`, {
      scenario_key: 'custom',
      action_type,
      parameters,
    });
    return res.data;
  },

  // Approvals & Execution
  getApprovals: async (employeeId?: string, status?: string): Promise<ApprovalRequest[]> => {
    const res = await api.get('/approvals', { params: { employee_id: employeeId, status } });
    return res.data;
  },
  decideApproval: async (approvalId: string, status: 'Approved' | 'Rejected', notes?: string): Promise<ApprovalRequest> => {
    const res = await api.post(`/approvals/${approvalId}/decide`, {
      status,
      approver_id: 'user-sarah',
      approver_name: 'Sarah Johnson (Engineering Manager)',
      decision_notes: notes || `Action marked as ${status} for onboarding workflow recovery.`,
    });
    return res.data;
  },
  getAuditLogs: async (employeeId?: string) => {
    const res = await api.get('/approvals/audit-logs', { params: { employee_id: employeeId } });
    return res.data;
  },

  // Readiness
  getReadiness: async (employeeId: string): Promise<ReadinessData> => {
    const res = await api.get(`/readiness/${employeeId}`);
    return res.data;
  },

  // Learning & Analytics
  getLearningAnalytics: async (): Promise<LearningAnalytics> => {
    const res = await api.get('/learning/analytics');
    return res.data;
  },

  // Orchestrator trigger
  runOrchestrator: async (employeeId: string) => {
    const res = await api.post(`/orchestration/run/${employeeId}`);
    return res.data;
  },
};
