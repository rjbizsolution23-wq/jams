"use client";

import * as React from "react";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { WorkflowCanvas } from "@/components/workflows/WorkflowCanvas";
import { GitBranch, Plus, Play } from "lucide-react";

const mockWorkflows = [
  {
    id: 1,
    name: "Complete Track Production",
    description: "Full workflow from composition to mastering",
    steps: 8,
    status: "ready",
  },
  {
    id: 2,
    name: "Stem Separation + Mixing",
    description: "Separate stems and apply professional mixing",
    steps: 5,
    status: "ready",
  },
  {
    id: 3,
    name: "AI Music Generation",
    description: "Generate music from text prompts",
    steps: 3,
    status: "ready",
  },
];

export default function WorkflowsPage() {
  const [showBuilder, setShowBuilder] = React.useState(false);

  if (showBuilder) {
    return (
      <div className="h-full flex flex-col">
        <div className="flex items-center justify-between p-4 bg-gray-900 border-b border-gray-800">
          <h1 className="text-lg font-semibold">Visual Workflow Builder</h1>
          <Button onClick={() => setShowBuilder(false)} variant="secondary" size="sm">
            Back to List
          </Button>
        </div>
        <div className="flex-1 overflow-hidden">
          <WorkflowCanvas />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Workflows"
        description="Build and execute multi-agent workflows"
        showSearch={false}
      />

      <div className="flex-1 p-6 space-y-6 overflow-auto scrollbar-thin">
        {/* Action Bar */}
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-lg font-semibold text-gray-100">My Workflows</h2>
            <p className="text-sm text-gray-400">Create and manage agent workflows</p>
          </div>
          <Button onClick={() => setShowBuilder(true)}>
            <Plus className="h-4 w-4 mr-2" />
            New Workflow
          </Button>
        </div>

        {/* Workflows Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          {mockWorkflows.map((workflow) => (
            <Card key={workflow.id} className="hover:border-violet-600/50 transition-colors cursor-pointer">
              <CardHeader>
                <div className="flex items-start justify-between">
                  <GitBranch className="h-5 w-5 text-violet-400" />
                  <Badge variant="success">{workflow.status}</Badge>
                </div>
                <CardTitle className="text-base mt-2">{workflow.name}</CardTitle>
                <CardDescription>{workflow.description}</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">{workflow.steps} steps</span>
                  <Button 
                    size="sm" 
                    variant="outline"
                    onClick={() => {
                      // TODO: Execute workflow via API
                      console.log('Execute workflow:', workflow.id);
                    }}
                  >
                    <Play className="h-3 w-3 mr-1" />
                    Execute
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Visual Builder CTA */}
        <Card className="border-violet-600/20 bg-gradient-to-br from-violet-900/10 to-blue-900/10">
          <CardHeader>
            <CardTitle>Visual Workflow Builder</CardTitle>
            <CardDescription>Drag and drop agents to create custom workflows</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="rounded-lg h-[300px] flex items-center justify-center bg-black/20 backdrop-blur-sm border border-gray-800">
              <div className="text-center">
                <GitBranch className="h-12 w-12 mx-auto text-violet-400 mb-4" />
                <p className="text-gray-300 mb-1 font-medium">Fully Functional Workflow Builder</p>
                <p className="text-gray-400 text-sm mb-4">
                  Build complex multi-agent workflows with drag-and-drop
                </p>
                <Button onClick={() => setShowBuilder(true)} size="lg">
                  <Plus className="h-4 w-4 mr-2" />
                  Open Workflow Builder
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

