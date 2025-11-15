"use client";

import * as React from "react";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";
import {
  Music,
  Plus,
  FolderOpen,
  Play,
  Edit,
  Trash2,
  Download,
  Share2,
  Clock,
  CheckCircle,
  Search,
} from "lucide-react";
import { motion } from "framer-motion";
import { format } from "date-fns";

const mockProjects = [
  {
    id: 1,
    name: "Summer Vibes EP",
    description: "Chill electronic music for summer",
    tracks: 6,
    status: "in_progress",
    lastModified: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    totalDuration: 1320,
    workflow: "Complete Track Production",
  },
  {
    id: 2,
    name: "Rock Anthem Collection",
    description: "Powerful rock instrumentals",
    tracks: 8,
    status: "completed",
    lastModified: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    totalDuration: 2160,
    workflow: "Mixing & Mastering",
  },
  {
    id: 3,
    name: "Jazz Standards Remastered",
    description: "Classic jazz with AI enhancement",
    tracks: 12,
    status: "completed",
    lastModified: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
    totalDuration: 3600,
    workflow: "Audio Restoration",
  },
  {
    id: 4,
    name: "Hip Hop Beats Vol. 1",
    description: "Modern hip hop production",
    tracks: 15,
    status: "in_progress",
    lastModified: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    totalDuration: 2700,
    workflow: "Beat Making",
  },
];

export default function ProjectsPage() {
  const [searchQuery, setSearchQuery] = React.useState("");

  const filteredProjects = mockProjects.filter((project) =>
    project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const formatDuration = (seconds: number) => {
    const hours = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    return `${hours}h ${mins}m`;
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "completed":
        return <Badge variant="success">Completed</Badge>;
      case "in_progress":
        return <Badge variant="warning">In Progress</Badge>;
      default:
        return <Badge variant="secondary">{status}</Badge>;
    }
  };

  return (
    <div className="flex flex-col h-full">
      <Header
        title="Projects"
        description="Manage your music production projects"
        showSearch={false}
      />

      <div className="flex-1 p-6 space-y-6 overflow-auto scrollbar-thin">
        {/* Stats */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Projects</p>
                  <p className="text-2xl font-bold text-violet-400 mt-1">
                    {mockProjects.length}
                  </p>
                </div>
                <FolderOpen className="h-8 w-8 text-violet-400/50" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">In Progress</p>
                  <p className="text-2xl font-bold text-yellow-400 mt-1">
                    {mockProjects.filter((p) => p.status === "in_progress").length}
                  </p>
                </div>
                <Clock className="h-8 w-8 text-yellow-400/50" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Completed</p>
                  <p className="text-2xl font-bold text-green-400 mt-1">
                    {mockProjects.filter((p) => p.status === "completed").length}
                  </p>
                </div>
                <CheckCircle className="h-8 w-8 text-green-400/50" />
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-500">Total Tracks</p>
                  <p className="text-2xl font-bold text-blue-400 mt-1">
                    {mockProjects.reduce((sum, p) => sum + p.tracks, 0)}
                  </p>
                </div>
                <Music className="h-8 w-8 text-blue-400/50" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Action Bar */}
        <div className="flex flex-col sm:flex-row gap-4 justify-between">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
            <Input
              placeholder="Search projects..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <Button 
            size="lg"
            onClick={() => {
              // TODO: Open new project modal
              console.log('New project clicked');
            }}
          >
            <Plus className="h-4 w-4 mr-2" />
            New Project
          </Button>
        </div>

        {/* Projects Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {filteredProjects.map((project, index) => (
            <motion.div
              key={project.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3, delay: index * 0.05 }}
            >
              <Card className="hover:border-violet-600/50 transition-colors cursor-pointer">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <CardTitle className="text-lg mb-2">{project.name}</CardTitle>
                      <p className="text-sm text-gray-400">{project.description}</p>
                    </div>
                    {getStatusBadge(project.status)}
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* Project Stats */}
                  <div className="grid grid-cols-3 gap-4 text-center">
                    <div>
                      <p className="text-2xl font-bold text-violet-400">{project.tracks}</p>
                      <p className="text-xs text-gray-500">Tracks</p>
                    </div>
                    <div>
                      <p className="text-2xl font-bold text-blue-400">
                        {formatDuration(project.totalDuration)}
                      </p>
                      <p className="text-xs text-gray-500">Duration</p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-300">{format(project.lastModified, "MMM d")}</p>
                      <p className="text-xs text-gray-500">Modified</p>
                    </div>
                  </div>

                  {/* Workflow Badge */}
                  <div>
                    <Badge variant="outline" className="text-xs">
                      {project.workflow}
                    </Badge>
                  </div>

                  {/* Actions */}
                  <div className="flex items-center gap-2">
                    <Button size="sm" className="flex-1">
                      <Play className="h-3 w-3 mr-1" />
                      Open
                    </Button>
                    <Button size="sm" variant="outline">
                      <Edit className="h-3 w-3" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Download className="h-3 w-3" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Share2 className="h-3 w-3" />
                    </Button>
                    <Button size="sm" variant="outline">
                      <Trash2 className="h-3 w-3" />
                    </Button>
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>

        {filteredProjects.length === 0 && (
          <Card>
            <CardContent className="py-12 text-center">
              <FolderOpen className="h-12 w-12 mx-auto text-gray-600 mb-4" />
              <p className="text-gray-400">No projects found</p>
              <p className="text-sm text-gray-500 mt-2">
                {searchQuery ? "Try a different search" : "Create a new project to get started"}
              </p>
              <Button className="mt-4">
                <Plus className="h-4 w-4 mr-2" />
                New Project
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  );
}
