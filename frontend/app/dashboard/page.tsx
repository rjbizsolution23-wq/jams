"use client";

import * as React from "react";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { TypewriterEffect, StreamingLines } from "@/components/realtime/StreamingText";
import { useAgentStore } from "@/store/agentStore";
import { useWorkflowStore } from "@/store/workflowStore";
import { useAudioStore } from "@/store/audioStore";
import {
  Play,
  Zap,
  Music,
  Users,
  Activity,
  TrendingUp,
  Clock,
  CheckCircle,
  Sparkles,
  Folder,
  Upload,
  GitBranch,
  BarChart3,
} from "lucide-react";
import { motion } from "framer-motion";
import { format } from "date-fns";
import { useAgents } from "@/lib/hooks/useAgents";

export default function DashboardPage() {
  const { agents } = useAgentStore();
  const { workflows } = useWorkflowStore();
  const { files } = useAudioStore();
  
  // Load agents from API
  const { data: apiAgents, isLoading: agentsLoading } = useAgents();
  
  // Update store when API agents load
  React.useEffect(() => {
    if (apiAgents && apiAgents.length > 0) {
      useAgentStore.getState().setAgents(apiAgents);
    }
  }, [apiAgents]);

  const [recentActivity, setRecentActivity] = React.useState<string[]>([
    "System initialized successfully",
    "110 AI agents loaded and ready",
    "Connected to Cloudflare edge network",
    "Real-time monitoring active",
  ]);

  // Quick stats
  const stats = {
    totalAgents: agents.length,
    activeAgents: agents.filter((a) => a.status === "working").length,
    completedTasks: agents.reduce((sum, a) => sum + a.tasksCompleted, 0),
    totalWorkflows: 3, // Mock
    totalFiles: 12, // Mock
    storageUsed: "4.2 GB",
  };

  const quickActions = [
    {
      icon: Sparkles,
      label: "Execute Agent",
      description: "Run any AI agent",
      color: "text-violet-400",
      href: "/agents",
    },
    {
      icon: GitBranch,
      label: "Build Workflow",
      description: "Create agent workflow",
      color: "text-blue-400",
      href: "/workflows",
    },
    {
      icon: Upload,
      label: "Upload Audio",
      description: "Add files to library",
      color: "text-green-400",
      href: "/library",
    },
    {
      icon: BarChart3,
      label: "View Analytics",
      description: "Check performance",
      color: "text-yellow-400",
      href: "/analytics",
    },
  ];

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Command Center"
        description="Your Music Production Empire at a Glance"
        showSearch={true}
      />

      <div className="flex-1 p-6 space-y-6 overflow-auto scrollbar-thin">
        {/* Welcome Banner */}
        <Card className="border-violet-600/20 bg-gradient-to-br from-violet-900/20 to-blue-900/20">
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-100 mb-2">
                  Welcome to Jukeyman AGI Music Studio (JAMS) 🎵
                </h1>
                <div className="text-gray-400">
                  <TypewriterEffect
                    words={[
                      "110 AI agents ready to create",
                      "Autonomous music production",
                      "Professional-grade output",
                      "Real-time collaboration",
                    ]}
                    className="text-violet-400 font-medium"
                  />
                </div>
              </div>
              <div className="flex gap-2">
                <Button 
                  size="lg" 
                  onClick={() => {
                    if (typeof window !== 'undefined') {
                      window.location.href = '/agents';
                    }
                  }}
                >
                  <Play className="h-5 w-5 mr-2" />
                  Start Creating
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0 }}
          >
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Total Agents</p>
                    <p className="text-2xl font-bold text-violet-400 mt-1">
                      {stats.totalAgents}
                    </p>
                  </div>
                  <Users className="h-8 w-8 text-violet-400/50" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Active Now</p>
                    <p className="text-2xl font-bold text-green-400 mt-1">
                      {stats.activeAgents}
                    </p>
                  </div>
                  <Activity className="h-8 w-8 text-green-400/50" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.2 }}
          >
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Tasks Done</p>
                    <p className="text-2xl font-bold text-blue-400 mt-1">
                      {stats.completedTasks}
                    </p>
                  </div>
                  <CheckCircle className="h-8 w-8 text-blue-400/50" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.3 }}
          >
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Workflows</p>
                    <p className="text-2xl font-bold text-yellow-400 mt-1">
                      {stats.totalWorkflows}
                    </p>
                  </div>
                  <GitBranch className="h-8 w-8 text-yellow-400/50" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.4 }}
          >
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Audio Files</p>
                    <p className="text-2xl font-bold text-pink-400 mt-1">
                      {stats.totalFiles}
                    </p>
                  </div>
                  <Music className="h-8 w-8 text-pink-400/50" />
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: 0.5 }}
          >
            <Card>
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-500">Storage</p>
                    <p className="text-2xl font-bold text-orange-400 mt-1">
                      {stats.storageUsed}
                    </p>
                  </div>
                  <Folder className="h-8 w-8 text-orange-400/50" />
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Quick Actions + Activity */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Actions */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5 text-violet-400" />
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  {quickActions.map((action, index) => (
                    <motion.div
                      key={action.label}
                      initial={{ opacity: 0, scale: 0.9 }}
                      animate={{ opacity: 1, scale: 1 }}
                      transition={{ duration: 0.2, delay: index * 0.05 }}
                    >
                      <Button
                        variant="outline"
                        className="h-auto flex-col items-start p-4 w-full"
                        onClick={() => {
                          if (typeof window !== 'undefined') {
                            window.location.href = action.href;
                          }
                        }}
                      >
                        <action.icon className={`h-6 w-6 ${action.color} mb-2`} />
                        <span className="text-sm font-medium text-gray-100">
                          {action.label}
                        </span>
                        <span className="text-xs text-gray-500 mt-1">
                          {action.description}
                        </span>
                      </Button>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Live Activity Feed */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle className="flex items-center gap-2">
                    <Activity className="h-5 w-5 text-green-400 animate-pulse" />
                    Live Activity
                  </CardTitle>
                  <Badge variant="success">Real-time</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="bg-black/20 rounded-lg p-4 font-mono text-sm">
                  <StreamingLines lines={recentActivity} isStreaming />
                </div>
              </CardContent>
            </Card>

            {/* System Health */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <TrendingUp className="h-5 w-5 text-green-400" />
                  System Health
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">API Status</span>
                    <Badge variant="success">Operational</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Edge Network</span>
                    <Badge variant="success">Connected</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">R2 Storage</span>
                    <Badge variant="success">Healthy</Badge>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-gray-400">Agent Pool</span>
                    <Badge variant="success">Ready</Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column: Recent Projects + Top Agents */}
          <div className="space-y-6">
            {/* Recent Projects */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Folder className="h-5 w-5 text-blue-400" />
                  Recent Projects
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {["Summer Vibes EP", "Rock Anthem Mix", "Jazz Collection"].map(
                    (project, i) => (
                      <div
                        key={project}
                        className="flex items-center gap-3 p-3 rounded-lg bg-gray-800/50 border border-gray-700 hover:border-violet-600/50 transition-colors cursor-pointer"
                      >
                        <div className="h-10 w-10 rounded bg-gradient-to-br from-violet-600 to-blue-600 flex items-center justify-center flex-shrink-0">
                          <Music className="h-5 w-5 text-white" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-200 truncate">
                            {project}
                          </p>
                          <p className="text-xs text-gray-500">
                            Modified {i + 1} days ago
                          </p>
                        </div>
                      </div>
                    )
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Top Performing Agents */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-violet-400" />
                  Top Agents
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {agents.slice(0, 5).map((agent, i) => (
                    <div
                      key={agent.id}
                      className="flex items-center justify-between"
                    >
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold text-gray-500">
                          #{i + 1}
                        </span>
                        <span className="text-sm text-gray-300">
                          {agent.name}
                        </span>
                      </div>
                      <Badge variant="outline" className="text-xs">
                        {agent.tasksCompleted} tasks
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Today's Highlights */}
            <Card className="border-violet-600/20 bg-gradient-to-br from-violet-900/10 to-blue-900/10">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Clock className="h-5 w-5 text-violet-400" />
                  Today's Highlights
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3 text-sm">
                  <div className="flex items-center gap-2">
                    <CheckCircle className="h-4 w-4 text-green-400" />
                    <span className="text-gray-300">
                      {stats.completedTasks} tasks completed
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Activity className="h-4 w-4 text-blue-400" />
                    <span className="text-gray-300">
                      {stats.activeAgents} agents active
                    </span>
                  </div>
                  <div className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4 text-green-400" />
                    <span className="text-gray-300">Cost: $0.42 today</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
}
