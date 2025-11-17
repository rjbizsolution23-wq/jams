# Jukeyman AGI Music Studio (JAMS) - Complete API Endpoints

**Base URL:** `https://jams-api.rickjefferson.workers.dev`

All endpoints support CORS and return JSON responses.

---

## ✅ Health & Status

### `GET /health`
Health check endpoint.
- **Response:** Service status, version, and feature flags

---

## ✅ Agents API

### `GET /api/v1/agents`
List all 110 agents.
- **Response:** Array of agents with id, name, department, status, capabilities

### `GET /api/v1/agents/:id`
Get agent by ID.
- **Response:** Agent details

### `POST /api/v1/agent/run`
Execute an agent task.
- **Body:**
  ```json
  {
    "agent_name": "Music Agent",
    "task": "Create a short song melody description",
    "model": "deepseek/deepseek-chat"
  }
  ```
- **Response:** Execution result with success, model, provider, result, usage

---

## ✅ Models API

### `GET /api/v1/models/list`
Get all available models from all providers.
- **Response:** Array of 34+ models from OpenRouter, MiniMax, and Chutes
- Includes: Free models, paid models, audio models, video models, music generation models

---

## ✅ Cost API

### `GET /api/v1/cost/summary`
Get cost summary.
- **Response:** Total cost, today's cost, currency

---

## ✅ Projects API

### `GET /api/v1/projects`
List all projects.
- **Response:** Array of projects

### `POST /api/v1/projects`
Create a new project.
- **Body:**
  ```json
  {
    "name": "My Music Project",
    "description": "Project description",
    "owner_id": "user-default"
  }
  ```
- **Response:** Created project with id, name, description, status, timestamps

### `GET /api/v1/projects/:id`
Get project by ID.
- **Response:** Project details

### `PUT /api/v1/projects/:id`
Update project.
- **Body:**
  ```json
  {
    "name": "Updated Name",
    "description": "Updated description",
    "status": "archived"
  }
  ```
- **Response:** Updated project

### `DELETE /api/v1/projects/:id`
Delete project (soft delete).
- **Response:** Success message

---

## ✅ Workflows API

### `GET /api/v1/workflows`
List all workflows.
- **Response:** Array of workflows

### `POST /api/v1/workflows`
Create a new workflow.
- **Body:**
  ```json
  {
    "name": "My Workflow",
    "description": "Workflow description",
    "project_id": "project-id",
    "graph_json": {
      "nodes": [...],
      "edges": [...]
    }
  }
  ```
- **Response:** Created workflow with id, name, graph_json, status

### `GET /api/v1/workflows/:id`
Get workflow by ID.
- **Response:** Workflow details with parsed graph_json

### `PUT /api/v1/workflows/:id`
Update workflow.
- **Body:**
  ```json
  {
    "name": "Updated Name",
    "description": "Updated description",
    "graph_json": {...},
    "status": "active"
  }
  ```
- **Response:** Updated workflow

### `DELETE /api/v1/workflows/:id`
Delete workflow (soft delete).
- **Response:** Success message

### `POST /api/v1/workflows/:id/execute`
Execute a workflow.
- **Response:** Execution result with execution_id, workflow_id, results array

---

## ✅ Executions API

### `GET /api/v1/executions`
List all executions.
- **Response:** Array of executions with status, model, provider, result, cost

### `GET /api/v1/executions/:id`
Get execution by ID.
- **Response:** Execution details with parsed usage and result

### `GET /api/v1/executions/:id/logs`
Get execution logs.
- **Response:** Array of log entries

---

## ✅ Storage/Library API

### `GET /api/v1/storage`
List all audio files.
- **Response:** Array of audio files with id, filename, r2_key, size_bytes, project_id

### `POST /api/v1/storage`
Upload an audio file.
- **Body:** `multipart/form-data` with:
  - `file`: Audio file (mp3, wav, flac, m4a)
  - `project_id`: (optional) Project ID
- **Response:** Uploaded file metadata with id, filename, r2_key, size_bytes

### `GET /api/v1/storage/:id`
Get audio file by ID.
- **Response:** File details with signed URL

### `DELETE /api/v1/storage/:id`
Delete audio file (soft delete + R2 deletion).
- **Response:** Success message

---

## ✅ Notifications API

### `GET /api/v1/notifications`
List all notifications.
- **Response:** Array of notifications

### `POST /api/v1/notifications/read`
Mark notifications as read.
- **Body:**
  ```json
  {
    "notification_ids": ["id1", "id2", "id3"]
  }
  ```
- **Response:** Success message

---

## ✅ Settings API

### `GET /api/v1/settings`
Get all settings.
- **Response:** Object with key-value pairs
- Default settings:
  - `default_model`: "deepseek/deepseek-chat"
  - `max_concurrent_executions`: 10
  - `cost_alert_threshold`: 100
  - `retention_days`: 90

### `PUT /api/v1/settings`
Update a setting.
- **Body:**
  ```json
  {
    "key": "default_model",
    "value": "qwen/qwen-2.5-72b-instruct"
  }
  ```
- **Response:** Success message with key and value

---

## 📊 Database Schema

The D1 database includes the following tables:

- `users` - User accounts
- `projects` - Music projects
- `workflows` - Visual workflow definitions
- `workflow_nodes` - Workflow nodes
- `workflow_edges` - Workflow connections
- `agents` - Agent definitions
- `executions` - Execution history
- `execution_logs` - Execution logs
- `audio_files` - Audio library files
- `models` - Model cache
- `costs` - Cost tracking
- `notifications` - User notifications
- `settings` - System settings

---

## 🔧 Infrastructure

- **Database:** Cloudflare D1 (SQLite)
- **Storage:** Cloudflare R2 (Audio files)
- **Cache:** Cloudflare KV (Cost tracking)
- **Worker:** Cloudflare Workers (Edge runtime)
- **Region:** WNAM (US)

---

## ✅ Status

All endpoints are **fully operational** and deployed to production.

**Live URL:** https://jams-api.rickjefferson.workers.dev

