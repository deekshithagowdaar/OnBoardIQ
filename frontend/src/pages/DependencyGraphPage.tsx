import React, { useEffect, useState, useMemo } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';
import { CustomTaskNode } from '../components/CustomTaskNode';
import { apiClient } from '../api/client';
import { DependencyGraphData, Task } from '../types';
import { AlertCircle, GitBranch, RefreshCw, ZoomIn, Info } from 'lucide-react';
import { TaskDetailModal } from '../components/TaskDetailModal';

interface Props {
  selectedEmployeeId: string;
}

export const DependencyGraphPage: React.FC<Props> = ({ selectedEmployeeId }) => {
  const [graphData, setGraphData] = useState<DependencyGraphData | null>(null);
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);

  const nodeTypes = useMemo(() => ({ customTaskNode: CustomTaskNode }), []);

  const fetchGraph = async () => {
    if (!selectedEmployeeId) return;
    setLoading(true);
    try {
      const data = await apiClient.getDependencyGraph(selectedEmployeeId);
      setGraphData(data);
      setNodes(data.nodes);
      setEdges(data.edges);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchGraph();
  }, [selectedEmployeeId]);

  const onNodeClick = (_: any, node: any) => {
    const found = nodes.find((n) => n.id === node.id);
    if (found?.data) {
      setSelectedTask(found.data as any);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-4 border-sky-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Top Header Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2">
            <h2 className="text-xl font-bold text-slate-900">Dynamic Dependency Graph</h2>
            <span className="text-[11px] font-semibold px-2 py-0.5 bg-sky-50 text-sky-700 border border-sky-200 rounded-full">
              Real-Time DAG Traversal
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-0.5">
            Directed acyclic graph illustrating upstream blockers and downstream blast radius. Red animated edges indicate blocked task chains.
          </p>
        </div>

        <button
          onClick={fetchGraph}
          className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-xs font-semibold shadow-sm transition-colors"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh Graph</span>
        </button>
      </div>

      {/* Legend & Summary Info */}
      <div className="bg-white p-3 rounded-xl border border-slate-200/80 shadow-sm flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex flex-wrap items-center gap-4">
          <span className="font-semibold text-slate-700">Status Legend:</span>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
            <span className="text-slate-600">Completed</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-blue-500" />
            <span className="text-slate-600">In Progress</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-500" />
            <span className="text-slate-600">Blocked</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full bg-rose-500" />
            <span className="text-slate-600">Delayed (Root Blocker)</span>
          </div>
        </div>

        <div className="flex items-center gap-3 font-mono text-[11px] text-slate-500">
          <span>Total Nodes: <strong className="text-slate-900">{graphData?.total_tasks || 0}</strong></span>
          <span>Blocked: <strong className="text-rose-600">{graphData?.blocked_task_ids?.length || 0}</strong></span>
          <span>Completed: <strong className="text-emerald-600">{graphData?.completed_tasks || 0}</strong></span>
        </div>
      </div>

      {/* React Flow Container */}
      <div className="h-[620px] bg-slate-900/5 rounded-2xl border border-slate-200/80 shadow-inner overflow-hidden relative">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          fitView
          attributionPosition="bottom-right"
        >
          <Background color="#94a3b8" gap={20} size={1} />
          <Controls />
          <MiniMap
            nodeColor={(node) => {
              if (node.data?.status === 'Completed') return '#10b981';
              if (node.data?.status === 'Delayed') return '#f43f5e';
              if (node.data?.status === 'Blocked') return '#f59e0b';
              return '#3b82f6';
            }}
            className="rounded-lg shadow border border-slate-200"
          />
        </ReactFlow>

        <div className="absolute bottom-3 left-3 bg-white/90 backdrop-blur-sm px-3 py-1.5 rounded-lg border border-slate-200 text-[11px] text-slate-600 shadow-sm flex items-center gap-1.5">
          <Info className="w-3.5 h-3.5 text-sky-600" />
          <span>Click on any task node to inspect details and simulate status changes.</span>
        </div>
      </div>

      <TaskDetailModal
        task={selectedTask}
        onClose={() => setSelectedTask(null)}
        onTaskUpdated={fetchGraph}
      />
    </div>
  );
};
