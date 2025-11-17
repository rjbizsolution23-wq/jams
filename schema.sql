-- Jukeyman AGI Music Studio (JAMS) - Database Schema
-- Cloudflare D1 (SQLite) Database Schema

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT,
  role TEXT DEFAULT 'user', -- 'user', 'admin'
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);

-- Projects table
CREATE TABLE IF NOT EXISTS projects (
  id TEXT PRIMARY KEY,
  owner_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  status TEXT DEFAULT 'active', -- 'active', 'archived', 'deleted'
  metadata TEXT, -- JSON metadata
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Workflows table
CREATE TABLE IF NOT EXISTS workflows (
  id TEXT PRIMARY KEY,
  project_id TEXT,
  name TEXT NOT NULL,
  description TEXT,
  graph_json TEXT NOT NULL, -- Full workflow graph as JSON
  status TEXT DEFAULT 'draft', -- 'draft', 'active', 'paused', 'archived'
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Workflow nodes table
CREATE TABLE IF NOT EXISTS workflow_nodes (
  id TEXT PRIMARY KEY,
  workflow_id TEXT NOT NULL,
  node_type TEXT NOT NULL, -- 'agent', 'input', 'output', 'conditional'
  data_json TEXT NOT NULL, -- Node data as JSON
  position_x REAL DEFAULT 0,
  position_y REAL DEFAULT 0,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE
);

-- Workflow edges table
CREATE TABLE IF NOT EXISTS workflow_edges (
  id TEXT PRIMARY KEY,
  workflow_id TEXT NOT NULL,
  source_node_id TEXT NOT NULL,
  target_node_id TEXT NOT NULL,
  label TEXT,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE CASCADE,
  FOREIGN KEY (source_node_id) REFERENCES workflow_nodes(id) ON DELETE CASCADE,
  FOREIGN KEY (target_node_id) REFERENCES workflow_nodes(id) ON DELETE CASCADE
);

-- Agents table (extended from static list)
CREATE TABLE IF NOT EXISTS agents (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  department TEXT NOT NULL,
  capabilities_json TEXT, -- JSON array of capabilities
  status TEXT DEFAULT 'idle', -- 'idle', 'working', 'error'
  tasks_completed INTEGER DEFAULT 0,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);

-- Executions table (track all agent/workflow executions)
CREATE TABLE IF NOT EXISTS executions (
  id TEXT PRIMARY KEY,
  workflow_id TEXT,
  project_id TEXT,
  agent_name TEXT NOT NULL,
  agent_id TEXT,
  model_id TEXT NOT NULL,
  provider TEXT, -- 'openrouter', 'minimax', 'chutes'
  task TEXT NOT NULL,
  status TEXT DEFAULT 'pending', -- 'pending', 'running', 'completed', 'failed', 'cancelled'
  result TEXT,
  usage_json TEXT, -- Token usage as JSON
  cost_usd REAL DEFAULT 0,
  started_at INTEGER,
  finished_at INTEGER,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (workflow_id) REFERENCES workflows(id) ON DELETE SET NULL,
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL,
  FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE SET NULL
);

-- Execution logs table
CREATE TABLE IF NOT EXISTS execution_logs (
  id TEXT PRIMARY KEY,
  execution_id TEXT NOT NULL,
  level TEXT DEFAULT 'info', -- 'debug', 'info', 'warn', 'error'
  message TEXT NOT NULL,
  meta_json TEXT, -- Additional metadata as JSON
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE
);

-- Audio files table (library)
CREATE TABLE IF NOT EXISTS audio_files (
  id TEXT PRIMARY KEY,
  project_id TEXT,
  r2_key TEXT NOT NULL UNIQUE, -- R2 object key
  filename TEXT NOT NULL,
  file_type TEXT NOT NULL, -- 'mp3', 'wav', 'flac', 'm4a'
  duration_seconds REAL,
  size_bytes INTEGER,
  waveform_json TEXT, -- Waveform data as JSON
  metadata_json TEXT, -- Audio metadata as JSON
  status TEXT DEFAULT 'active', -- 'active', 'archived', 'deleted'
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
);

-- Models table (cache of available models)
CREATE TABLE IF NOT EXISTS models (
  id TEXT PRIMARY KEY,
  provider TEXT NOT NULL, -- 'openrouter', 'minimax', 'chutes'
  model_id TEXT NOT NULL UNIQUE, -- Provider-specific model ID
  name TEXT NOT NULL,
  cost_per_1m REAL DEFAULT 0,
  context_tokens INTEGER,
  model_type TEXT, -- 'text', 'audio', 'music', 'video', 'image'
  features_json TEXT, -- JSON array of features
  enabled BOOLEAN DEFAULT 1,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);

-- Costs table (detailed cost tracking)
CREATE TABLE IF NOT EXISTS costs (
  id TEXT PRIMARY KEY,
  day_utc TEXT NOT NULL, -- YYYY-MM-DD format
  provider TEXT NOT NULL,
  model_id TEXT NOT NULL,
  tokens_input INTEGER DEFAULT 0,
  tokens_output INTEGER DEFAULT 0,
  tokens_total INTEGER DEFAULT 0,
  cost_usd REAL DEFAULT 0,
  execution_count INTEGER DEFAULT 0,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  updated_at INTEGER NOT NULL DEFAULT (unixepoch()),
  UNIQUE(day_utc, provider, model_id)
);

-- Notifications table
CREATE TABLE IF NOT EXISTS notifications (
  id TEXT PRIMARY KEY,
  user_id TEXT,
  type TEXT NOT NULL, -- 'info', 'success', 'warning', 'error'
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  read BOOLEAN DEFAULT 0,
  link_url TEXT,
  created_at INTEGER NOT NULL DEFAULT (unixepoch()),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Settings table (key-value store)
CREATE TABLE IF NOT EXISTS settings (
  id TEXT PRIMARY KEY,
  key TEXT NOT NULL UNIQUE,
  value_json TEXT NOT NULL, -- JSON value
  description TEXT,
  updated_at INTEGER NOT NULL DEFAULT (unixepoch())
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_projects_owner ON projects(owner_id);
CREATE INDEX IF NOT EXISTS idx_workflows_project ON workflows(project_id);
CREATE INDEX IF NOT EXISTS idx_workflow_nodes_workflow ON workflow_nodes(workflow_id);
CREATE INDEX IF NOT EXISTS idx_workflow_edges_workflow ON workflow_edges(workflow_id);
CREATE INDEX IF NOT EXISTS idx_executions_workflow ON executions(workflow_id);
CREATE INDEX IF NOT EXISTS idx_executions_project ON executions(project_id);
CREATE INDEX IF NOT EXISTS idx_executions_status ON executions(status);
CREATE INDEX IF NOT EXISTS idx_execution_logs_execution ON execution_logs(execution_id);
CREATE INDEX IF NOT EXISTS idx_audio_files_project ON audio_files(project_id);
CREATE INDEX IF NOT EXISTS idx_costs_day ON costs(day_utc);
CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id);
CREATE INDEX IF NOT EXISTS idx_notifications_read ON notifications(read);

-- Insert default user (for now)
INSERT OR IGNORE INTO users (id, email, role) VALUES ('user-default', 'admin@jams.ai', 'admin');

-- Insert default agents (110 agents)
-- This will be populated via the API on startup if not present

-- Insert default settings
INSERT OR IGNORE INTO settings (id, key, value_json, description) VALUES
  ('setting-1', 'default_model', '"deepseek/deepseek-chat"', 'Default model for agent execution'),
  ('setting-2', 'max_concurrent_executions', '10', 'Maximum concurrent executions'),
  ('setting-3', 'cost_alert_threshold', '100', 'Cost alert threshold in USD'),
  ('setting-4', 'retention_days', '90', 'Data retention period in days');

