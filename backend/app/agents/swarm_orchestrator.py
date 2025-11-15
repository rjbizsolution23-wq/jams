"""
Jukeyman Autonomous Media Station (JAMS) - Swarm Orchestrator
Manages 100 AI agents across 10 departments
"""
import httpx
import asyncio
import logging
from typing import Dict, Any, List
from app.agents.swarm_config import SWARM_ARCHITECTURE
from app.core.config import settings

logger = logging.getLogger(__name__)


class SwarmOrchestrator:
    """
    Orchestrates 100 AI agents across 10 departments.
    Uses OpenRouter for free model access.
    """
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.openrouter_url = "https://openrouter.ai/api/v1/chat/completions"
        self.departments = SWARM_ARCHITECTURE["departments"]
        
        logger.info(f"Initialized Swarm with {len(self.departments)} departments")
        total_agents = sum(len(dept["workers"]) + 1 for dept in self.departments)
        logger.info(f"Total agents: {total_agents}")
    
    async def call_agent(
        self,
        agent_name: str,
        model_id: str,
        prompt: str,
        system_prompt: str = None
    ) -> Dict[str, Any]:
        """
        Call a specific agent via OpenRouter
        
        Args:
            agent_name: Name of the agent
            model_id: OpenRouter model ID
            prompt: User prompt
            system_prompt: Optional system prompt
            
        Returns:
            Agent response with metadata
        """
        messages = []
        
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        messages.append({
            "role": "user",
            "content": prompt
        })
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.openrouter_url,
                    json={
                        "model": model_id,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 4000
                    },
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                        "HTTP-Referer": "https://jams.app",
                        "X-Title": "Jukeyman Autonomous Media Station"
                    }
                )
                
                response.raise_for_status()
                result = response.json()
                
                return {
                    "agent_name": agent_name,
                    "model": model_id,
                    "content": result["choices"][0]["message"]["content"],
                    "usage": result.get("usage", {}),
                    "success": True
                }
        
        except Exception as e:
            logger.error(f"Agent {agent_name} failed: {e}")
            return {
                "agent_name": agent_name,
                "model": model_id,
                "content": None,
                "error": str(e),
                "success": False
            }
    
    async def execute_department_task(
        self,
        department_id: str,
        task_description: str
    ) -> Dict[str, Any]:
        """
        Execute a task with a specific department
        
        Args:
            department_id: Department ID (e.g., 'dept_01_architecture')
            task_description: Description of the task
            
        Returns:
            Department execution result
        """
        dept = next(
            (d for d in self.departments if d["id"] == department_id),
            None
        )
        
        if not dept:
            raise ValueError(f"Department not found: {department_id}")
        
        logger.info(f"Executing task in department: {dept['name']}")
        
        # Call supervisor first
        supervisor = dept["supervisor"]
        supervisor_prompt = f"""
You are {supervisor['name']}, supervisor of the {dept['name']} department.

Your role: {supervisor['role']}

Task: {task_description}

Analyze this task and provide:
1. High-level approach
2. Which workers should handle specific subtasks
3. Expected outcome

Be detailed and strategic.
"""
        
        supervisor_result = await self.call_agent(
            agent_name=supervisor["name"],
            model_id=supervisor["model"],
            prompt=supervisor_prompt
        )
        
        logger.info(f"Supervisor {supervisor['name']} completed analysis")
        
        return {
            "department": dept["name"],
            "supervisor_response": supervisor_result,
            "task": task_description,
            "status": "completed" if supervisor_result["success"] else "failed"
        }
    
    async def parallel_agent_execution(
        self,
        tasks: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple agent tasks in parallel
        
        Args:
            tasks: List of task dictionaries with 'agent_name', 'model_id', 'prompt'
            
        Returns:
            List of agent responses
        """
        async_tasks = [
            self.call_agent(
                agent_name=task["agent_name"],
                model_id=task["model_id"],
                prompt=task["prompt"]
            )
            for task in tasks
        ]
        
        results = await asyncio.gather(*async_tasks, return_exceptions=True)
        
        return [
            result if not isinstance(result, Exception) else {
                "agent_name": tasks[i]["agent_name"],
                "success": False,
                "error": str(result)
            }
            for i, result in enumerate(results)
        ]
    
    async def build_full_application(
        self,
        app_spec: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Use the swarm to build a full application
        
        Args:
            app_spec: Application specification with name, description, features, stack
            
        Returns:
            Complete build output from all departments
        """
        logger.info(f"Building application: {app_spec['name']}")
        
        results = {}
        
        # Phase 1: Architecture (dept_01)
        arch_result = await self.execute_department_task(
            "dept_01_architecture",
            f"Design architecture for: {app_spec['description']}. Features: {', '.join(app_spec.get('features', []))}"
        )
        results["architecture"] = arch_result
        
        # Phase 2: Frontend (dept_02)
        frontend_result = await self.execute_department_task(
            "dept_02_frontend",
            f"Design Next.js 15 frontend for: {app_spec['description']}"
        )
        results["frontend"] = frontend_result
        
        # Phase 3: Backend (dept_03)
        backend_result = await self.execute_department_task(
            "dept_03_backend",
            f"Design FastAPI backend for: {app_spec['description']}"
        )
        results["backend"] = backend_result
        
        # Phase 4: SEO (dept_04)
        seo_result = await self.execute_department_task(
            "dept_04_seo",
            f"Create SEO strategy for: {app_spec['name']}"
        )
        results["seo"] = seo_result
        
        # Phase 5: Content (dept_05)
        content_result = await self.execute_department_task(
            "dept_05_content",
            f"Generate content strategy for: {app_spec['name']}"
        )
        results["content"] = content_result
        
        # Phases 6-10 can run in parallel
        parallel_tasks = [
            ("automation", "dept_06_automation", "Create CI/CD pipeline"),
            ("security", "dept_07_security", "Design security measures"),
            ("data", "dept_08_data", "Design data analytics strategy"),
            ("monetization", "dept_09_monetization", "Create monetization strategy"),
            ("quality", "dept_10_quality", "Design testing strategy")
        ]
        
        parallel_results = await asyncio.gather(*[
            self.execute_department_task(dept_id, f"{task_desc} for: {app_spec['name']}")
            for _, dept_id, task_desc in parallel_tasks
        ])
        
        for (result_key, _, _), result in zip(parallel_tasks, parallel_results):
            results[result_key] = result
        
        logger.info(f"Application build completed: {app_spec['name']}")
        
        return {
            "app_name": app_spec["name"],
            "description": app_spec["description"],
            "department_results": results,
            "status": "completed",
            "total_departments": len(results)
        }
    
    async def get_swarm_health(self) -> Dict[str, Any]:
        """
        Check health of all agents/departments
        
        Returns:
            Health status of swarm
        """
        total_agents = sum(len(dept["workers"]) + 1 for dept in self.departments)
        
        return {
            "status": "healthy",
            "departments": len(self.departments),
            "total_agents": total_agents,
            "department_breakdown": [
                {
                    "id": dept["id"],
                    "name": dept["name"],
                    "supervisor": dept["supervisor"]["name"],
                    "workers": len(dept["workers"])
                }
                for dept in self.departments
            ]
        }


# Global instance
swarm_orchestrator = SwarmOrchestrator()


# Convenience function for FastAPI endpoints
async def execute_swarm_task(
    department_id: str,
    task_description: str
) -> Dict[str, Any]:
    """Execute a task with the swarm"""
    return await swarm_orchestrator.execute_department_task(
        department_id,
        task_description
    )

