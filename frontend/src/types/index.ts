export interface Employee {
  id: string;
  employee_id: string;
  full_name: string;
  email: string;
  department: string;
  job_role: string;
  employment_type: string;
  work_location: string;
  joining_date: string;
  reporting_manager: string;
  experience_level: string;
  required_equipment: string[];
  applicable_requirements: string[];
  status: 'Onboarding' | 'Ready' | 'At Risk' | 'Completed';
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: string;
  employee_id: string;
  task_id: string;
  name: string;
  description: string;
  department: 'HR' | 'IT' | 'Payroll' | 'Benefits';
  assigned_person: string;
  priority: 'Low' | 'Medium' | 'High' | 'Critical';
  start_date: string;
  due_date: string;
  estimated_duration_days: number;
  actual_completion_date?: string | null;
  status: 'Pending' | 'In Progress' | 'Completed' | 'Blocked' | 'Delayed';
  requires_approval: boolean;
  is_critical: boolean;
  delay_reason?: string | null;
  category?: string;
  upstream_dependencies?: string[];
  downstream_tasks?: string[];
}

export interface DependencyGraphData {
  employee_id: string;
  nodes: any[];
  edges: any[];
  blocked_task_ids: string[];
  critical_path_task_ids: string[];
  has_cycles: boolean;
  total_tasks: number;
  completed_tasks: number;
}

export interface TaskRiskDetail {
  task_id: string;
  task_name: string;
  department: string;
  status: string;
  risk_score: number;
  delay_probability: number;
  reasons: string[];
}

export interface RiskPrediction {
  id: string;
  employee_id: string;
  overall_risk_score: number;
  risk_category: 'Low' | 'Medium' | 'High' | 'Critical';
  factors: string[];
  predicted_delay_days: number;
  attention_level: string;
  task_risks: TaskRiskDetail[];
  created_at: string;
}

export interface AffectedTaskDetail {
  task_id: string;
  task_name: string;
  department: string;
  status: string;
  delay_impact_days: number;
}

export interface RootCauseAnalysis {
  id: string;
  employee_id: string;
  primary_delayed_task_id: string;
  primary_delayed_task_name: string;
  root_cause_task_id: string;
  root_cause_task_name: string;
  root_cause_category: string;
  explanation: string;
  affected_downstream_task_ids: string[];
  affected_downstream_tasks: AffectedTaskDetail[];
  estimated_joining_date_impact_days: number;
  evidence: Record<string, any>;
  created_at: string;
}

export interface SimulationScenario {
  id: string;
  employee_id: string;
  scenario_key: string;
  scenario_title: string;
  description: string;
  action_type: string;
  parameters: Record<string, any>;
  unblocked_task_ids: string[];
  unblocked_count: number;
  time_saved_days: number;
  expected_completion_date?: string;
  joining_date_risk: string;
  readiness_score_projected: number;
  department_readiness: Record<string, number>;
  feasibility_score: number;
  policy_compliance: boolean;
  created_at: string;
}

export interface RecoveryRecommendation {
  id: string;
  employee_id: string;
  recommended_scenario_key: string;
  strategy_title: string;
  rationale: string;
  action_type: string;
  proposed_payload: Record<string, any>;
  requires_approval: boolean;
  approval_level: string;
  comparison_summary: Record<string, any>;
  created_at: string;
}

export interface WhatIfComparison {
  employee_id: string;
  baseline_readiness_score: number;
  baseline_risk_level: string;
  scenarios: SimulationScenario[];
  recommended_strategy?: RecoveryRecommendation;
}

export interface ApprovalRequest {
  id: string;
  employee_id: string;
  title: string;
  description: string;
  action_type: string;
  target_task_id?: string;
  proposed_payload: Record<string, any>;
  justification: string;
  impact_summary: Record<string, any>;
  status: 'Pending' | 'Approved' | 'Rejected';
  requested_by: string;
  approver_id?: string;
  approver_name?: string;
  decision_notes?: string;
  created_at: string;
  decided_at?: string;
}

export interface AuditLog {
  id: string;
  entity_type: string;
  entity_id: string;
  action: string;
  actor: string;
  details: Record<string, any>;
  timestamp: string;
}

export interface ReadinessData {
  id?: string;
  employee_id: string;
  overall_score: number;
  readiness_tier: 'Not Ready' | 'Needs Attention' | 'On Track' | 'Ready for Day 1';
  department_scores: Record<string, number>;
  completed_tasks_count: number;
  total_tasks_count: number;
  blocked_tasks_count: number;
  critical_pending_count: number;
  days_until_joining: number;
  score_explanation?: string;
  formula_breakdown?: Record<string, any>;
  critical_path_tasks?: Array<{
    id: string;
    name: string;
    department: string;
    status: string;
    is_blocked: boolean;
  }>;
  timestamp: string;
}

export interface LearningAnalytics {
  total_completed_onboardings: number;
  bottlenecks: Array<{
    department: string;
    task_name: string;
    delay_count: number;
    avg_delay_days: number;
    percentage_of_total_delays: number;
  }>;
  recovery_strategies_performance: Array<{
    strategy_name: string;
    times_recommended: number;
    approval_rate: number;
    success_rate: number;
    avg_days_saved: number;
  }>;
  prediction_accuracy_mae: number;
  prediction_vs_actual: Array<{
    task_name: string;
    predicted: number;
    actual: number;
    time_saved: number;
  }>;
  department_performance: Array<{
    department: string;
    total_cases: number;
    success_rate: number;
    avg_recovery_days: number;
  }>;
  historical_outcomes: any[];
}
