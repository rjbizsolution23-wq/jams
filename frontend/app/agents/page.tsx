"use client";

import * as React from "react";
import { Header } from "@/components/layout/Header";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { Input } from "@/components/ui/Input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/Select";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { AgentExecutionModal } from "@/components/agents/AgentExecutionModal";
import { useAgentStore, Agent } from "@/store/agentStore";
import { Search, Users, Sparkles, Star } from "lucide-react";
import { motion } from "framer-motion";

const departments = [
  "All Departments",
  "Audio Production",
  "Creative",
  "Technical",
  "Music Theory",
  "Genre Specialists",
  "AI/ML",
  "Post-Production",
  "Business",
  "Education",
  "Video & Visual",
  "Live Performance",
];

// Generate 110 agents with proper data
const generateAgents = (): Agent[] => {
  const agentsByDepartment: Record<string, { names: string[]; roles: string[] }> = {
    "Audio Production": {
      names: ["Composer", "Arranger", "Orchestrator", "Sound Designer", "Mixing Engineer", "Mastering Engineer", "Recording Engineer", "Music Producer", "Beat Maker", "Session Musician"],
      roles: ["Create melodies and harmonies", "Arrange music for instruments", "Orchestrate for ensembles", "Design synthesizer patches", "Professional mixing techniques", "Master tracks for distribution", "Recording setup and mic placement", "Overall production guidance", "Create drum patterns", "Instrument performance advice"]
    },
    "Creative": {
      names: ["Lyricist", "Poet", "Storyteller", "Brand Strategist", "Content Creator", "Copywriter", "Scriptwriter", "Concept Designer", "Theme Developer", "Mood Curator"],
      roles: ["Write song lyrics", "Create poetic content", "Develop narratives", "Music branding", "Social media content", "Promotional copy", "Video scripts", "Album concepts", "Musical themes", "Curate playlists"]
    },
    "Technical": {
      names: ["Audio Programmer", "DSP Engineer", "Plugin Developer", "System Architect", "Performance Optimizer", "QA Engineer", "DevOps Engineer", "Database Engineer", "API Developer", "Frontend Developer"],
      roles: ["Audio processing code", "DSP algorithms", "VST/AU plugins", "Design audio systems", "Optimize performance", "Test quality", "Deployment", "Data management", "Build APIs", "User interfaces"]
    },
    "Music Theory": {
      names: ["Music Theorist", "Harmony Expert", "Melody Specialist", "Rhythm Expert", "Counterpoint Master", "Scale Specialist", "Chord Progression Expert", "Form Analyst", "Jazz Theory Expert", "Contemporary Theory Expert"],
      roles: ["Analyze harmony", "Advanced harmonic concepts", "Melodic development", "Rhythmic patterns", "Contrapuntal writing", "Modes and scales", "Voice leading", "Song structure", "Jazz harmony", "Modern theory"]
    },
    "Genre Specialists": {
      names: ["Electronic Music Expert", "Hip Hop Specialist", "Rock Specialist", "Jazz Expert", "Classical Specialist", "Pop Expert", "R&B Specialist", "Country Expert", "World Music Expert", "Experimental Specialist", "Ambient Expert"],
      roles: ["EDM production", "Hip hop beats", "Rock mixing", "Jazz improvisation", "Classical composition", "Pop songwriting", "R&B production", "Country music", "Global styles", "Avant-garde", "Ambient soundscapes"]
    },
    "AI/ML": {
      names: ["Model Trainer", "Data Scientist", "ML Engineer", "Neural Network Expert", "Audio AI Specialist", "Voice Synthesis Expert", "Style Transfer Specialist", "Generative Model Expert", "Recommendation System Engineer", "Audio Classification Expert"],
      roles: ["Train AI models", "Analyze music data", "Build ML pipelines", "Deep learning", "AI audio generation", "Voice cloning", "Musical style transfer", "GANs for music", "Music recommendations", "Classify audio"]
    },
    "Post-Production": {
      names: ["Audio Restoration Specialist", "Vocal Tuning Expert", "Timing Editor", "Stem Separation Expert", "Format Converter", "Loudness Expert", "Spatial Audio Engineer", "Audio Forensics Analyst", "Archive Specialist", "Quality Control Manager"],
      roles: ["Remove noise", "Pitch correction", "Edit timing", "Separate stems", "Convert formats", "Loudness normalization", "3D audio", "Analyze audio", "Preserve recordings", "Quality checks"]
    },
    "Business": {
      names: ["Music Business Consultant", "Licensing Expert", "Publishing Specialist", "Rights Manager", "Contract Analyst", "Revenue Optimizer", "Distribution Expert", "Marketing Strategist", "Social Media Manager", "Analytics Expert"],
      roles: ["Business strategy", "Music licensing", "Publishing deals", "Rights and royalties", "Contracts", "Monetization", "Distribution", "Marketing campaigns", "Social media", "Data analytics"]
    },
    "Education": {
      names: ["Music Teacher", "Tutorial Creator", "Course Designer", "Lesson Planner", "Practice Coach", "Ear Training Specialist", "Sight Reading Coach", "Technique Instructor", "Music History Expert"],
      roles: ["Teach concepts", "Create tutorials", "Design courses", "Plan lessons", "Practice strategies", "Develop ear training", "Improve sight reading", "Instrument technique", "Music history"]
    },
    "Video & Visual": {
      names: ["Music Video Director", "VFX Artist", "Motion Graphics Designer", "3D Animator", "Video Editor", "Color Grading Specialist", "Visualizer Developer", "Album Art Designer", "Live Visual Artist", "Projection Mapping Specialist"],
      roles: ["Conceptualize videos", "VFX effects", "Motion graphics", "3D animation", "Edit videos", "Color correction", "Audio visualizers", "Album covers", "Live visuals", "Projection mapping"]
    },
    "Live Performance": {
      names: ["Live Sound Engineer", "Stage Manager", "Tour Manager", "DJ Specialist", "Live Looping Expert", "Performance Coach", "Venue Consultant", "Lighting Designer", "Audio Technician", "Monitor Engineer"],
      roles: ["Live sound setup", "Manage performances", "Tour planning", "DJing", "Live looping", "Stage presence", "Venue selection", "Lighting design", "Equipment setup", "Stage monitoring"]
    },
  };

  let agents: Agent[] = [];
  let id = 1;

  Object.entries(agentsByDepartment).forEach(([department, { names, roles }]) => {
    names.forEach((name, index) => {
      agents.push({
        id: `agent-${id}`,
        name,
        department,
        role: roles[index] || "AI specialist",
        status: "idle",
        tasksCompleted: 0,
        capabilities: [`Expert in ${name.toLowerCase()}`, "Real-time processing", "High accuracy"],
      });
      id++;
    });
  });

  return agents;
};

export default function AgentsPage() {
  const [searchQuery, setSearchQuery] = React.useState("");
  const [selectedDepartment, setSelectedDepartment] = React.useState("All Departments");
  const [modalOpen, setModalOpen] = React.useState(false);
  const [favoriteAgents, setFavoriteAgents] = React.useState<Set<string>>(new Set());
  
  const { agents, selectedAgent, selectAgent, setAgents, setLoading, setError } = useAgentStore();

  // Load agents from API
  React.useEffect(() => {
    const loadAgents = async () => {
      if (agents.length > 0) return; // Already loaded
      
      setLoading(true);
      try {
        const response = await fetch('https://jams-api.rickjefferson.workers.dev/api/v1/agents');
        if (!response.ok) {
          throw new Error('Failed to load agents');
        }
        const data = await response.json();
        
        // Transform API response to match Agent interface
        const apiAgents: Agent[] = (data.agents || []).map((agent: any, index: number) => ({
          id: agent.id || `agent-${index}`,
          name: agent.name || 'Unknown Agent',
          department: agent.department || 'Production',
          role: agent.capabilities?.[0] || 'Agent',
          status: agent.status || 'idle',
          tasksCompleted: 0,
          capabilities: agent.capabilities || [],
        }));
        
        setAgents(apiAgents.length > 0 ? apiAgents : generateAgents()); // Fallback to mock if empty
        setError(null);
      } catch (error: any) {
        console.error('Failed to load agents from API:', error);
        setError(error.message);
        // Fallback to mock agents if API fails
        setAgents(generateAgents());
      } finally {
        setLoading(false);
      }
    };

    loadAgents();
  }, [agents.length, setAgents, setLoading, setError]);

  const filteredAgents = agents.filter((agent) => {
    const matchesSearch = agent.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.department.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         agent.role.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesDepartment = selectedDepartment === "All Departments" || agent.department === selectedDepartment;
    return matchesSearch && matchesDepartment;
  });

  const handleAgentClick = (agent: Agent) => {
    selectAgent(agent);
    setModalOpen(true);
  };

  const toggleFavorite = (agentId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setFavoriteAgents((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(agentId)) {
        newSet.delete(agentId);
      } else {
        newSet.add(agentId);
      }
      return newSet;
    });
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "idle": return "bg-gray-500";
      case "working": return "bg-yellow-500 animate-pulse";
      case "completed": return "bg-green-500";
      case "error": return "bg-red-500";
      default: return "bg-gray-500";
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "idle": return { variant: "secondary" as const, text: "Ready" };
      case "working": return { variant: "warning" as const, text: "Working" };
      case "completed": return { variant: "success" as const, text: "Completed" };
      case "error": return { variant: "destructive" as const, text: "Error" };
      default: return { variant: "secondary" as const, text: status };
    }
  };

  if (agents.length === 0) {
    return (
      <div className="flex flex-col h-full">
        <Header
          title="AI Agents"
          description="110 specialized agents across 11 departments"
          showSearch={false}
        />
        <div className="flex-1 flex items-center justify-center">
          <LoadingSpinner size="lg" />
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full">
      <Header
        title="AI Agents"
        description="110 specialized agents across 11 departments"
        showSearch={false}
      />

      <div className="flex-1 p-6 space-y-6 overflow-auto scrollbar-thin">
        {/* Filters */}
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500" />
            <Input
              placeholder="Search agents..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
          <Select value={selectedDepartment} onValueChange={setSelectedDepartment}>
            <SelectTrigger className="w-full sm:w-[200px]">
              <SelectValue placeholder="Select department" />
            </SelectTrigger>
            <SelectContent>
              {departments.map((dept) => (
                <SelectItem key={dept} value={dept}>
                  {dept}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        {/* Stats Summary */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-violet-400">{agents.length}</div>
              <p className="text-sm text-gray-500">Total Agents</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-green-400">
                {agents.filter(a => a.status === "idle").length}
              </div>
              <p className="text-sm text-gray-500">Ready</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-yellow-400">
                {agents.filter(a => a.status === "working").length}
              </div>
              <p className="text-sm text-gray-500">Working</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-blue-400">
                {agents.reduce((sum, a) => sum + a.tasksCompleted, 0)}
              </div>
              <p className="text-sm text-gray-500">Tasks Completed</p>
            </CardContent>
          </Card>
        </div>

        {/* Agents Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
          {filteredAgents.map((agent, index) => {
            const statusBadge = getStatusBadge(agent.status);
            return (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3, delay: index * 0.02 }}
              >
                <Card
                  onClick={() => handleAgentClick(agent)}
                  className="hover:border-violet-600/50 transition-all cursor-pointer hover:shadow-lg hover:shadow-violet-600/10"
                >
                  <CardHeader>
                    <div className="flex items-start justify-between mb-2">
                      <div className={`h-3 w-3 rounded-full ${getStatusColor(agent.status)}`} />
                      <button
                        onClick={(e) => toggleFavorite(agent.id, e)}
                        className="text-gray-600 hover:text-yellow-400 transition-colors"
                      >
                        <Star
                          className="h-4 w-4"
                          fill={favoriteAgents.has(agent.id) ? "currentColor" : "none"}
                        />
                      </button>
                    </div>
                    <div className="flex items-start gap-2">
                      <div className="flex-shrink-0 h-10 w-10 rounded-lg bg-gradient-to-br from-violet-600 to-blue-600 flex items-center justify-center">
                        <Sparkles className="h-5 w-5 text-white" />
                      </div>
                      <div className="flex-1 min-w-0">
                        <CardTitle className="text-sm truncate">{agent.name}</CardTitle>
                        <p className="text-xs text-gray-400 mt-1 line-clamp-2">{agent.role}</p>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="flex items-center justify-between">
                      <Badge variant={statusBadge.variant} className="text-xs">
                        {statusBadge.text}
                      </Badge>
                      <span className="text-xs text-gray-500">{agent.tasksCompleted} tasks</span>
                    </div>
                    <Badge variant="outline" className="text-xs">{agent.department}</Badge>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })}
        </div>

        {filteredAgents.length === 0 && (
          <Card>
            <CardContent className="py-12 text-center">
              <Users className="h-12 w-12 mx-auto text-gray-600 mb-4" />
              <p className="text-gray-400">No agents found matching your filters</p>
            </CardContent>
          </Card>
        )}
      </div>

      {/* Agent Execution Modal */}
      <AgentExecutionModal
        agent={selectedAgent}
        open={modalOpen}
        onOpenChange={setModalOpen}
      />
    </div>
  );
}

