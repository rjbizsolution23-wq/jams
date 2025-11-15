"""
Jukeyman Autonomous Media Station (JAMS) - ComfyUI Service
Handles image generation via ComfyUI API
"""
import json
import uuid
import urllib.request
import urllib.error
import time
import websocket
import logging
from typing import Optional, Dict, Any
import os
import tempfile

from app.core.config import settings

logger = logging.getLogger(__name__)


class ComfyUIService:
    """
    Service for interacting with ComfyUI for image generation
    """
    
    def __init__(self, server_address: str = None):
        self.server_address = server_address or settings.COMFYUI_URL
        self.client_id = str(uuid.uuid4())
    
    def queue_prompt(self, prompt: Dict[str, Any]) -> str:
        """
        Queue a prompt for generation
        
        Args:
            prompt: ComfyUI workflow prompt dictionary
            
        Returns:
            Prompt ID
        """
        p = {"prompt": prompt, "client_id": self.client_id}
        data = json.dumps(p).encode('utf-8')
        
        try:
            req = urllib.request.Request(f"{self.server_address}/prompt", data=data)
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            return result['prompt_id']
        except urllib.error.URLError as e:
            logger.error(f"Failed to queue prompt: {e}")
            raise Exception(f"ComfyUI connection error: {str(e)}")
    
    def get_image(self, filename: str, subfolder: str = "", folder_type: str = "output") -> bytes:
        """
        Get generated image from ComfyUI
        
        Args:
            filename: Image filename
            subfolder: Subfolder in output directory
            folder_type: Type of folder (output, input, temp)
            
        Returns:
            Image bytes
        """
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        
        try:
            with urllib.request.urlopen(f"{self.server_address}/view?{url_values}") as response:
                return response.read()
        except urllib.error.URLError as e:
            logger.error(f"Failed to get image: {e}")
            raise Exception(f"Failed to retrieve image: {str(e)}")
    
    def get_history(self, prompt_id: str) -> Dict:
        """
        Get generation history/status
        
        Args:
            prompt_id: Prompt ID from queue_prompt
            
        Returns:
            History dictionary
        """
        try:
            with urllib.request.urlopen(f"{self.server_address}/history/{prompt_id}") as response:
                return json.loads(response.read())
        except urllib.error.URLError as e:
            logger.error(f"Failed to get history: {e}")
            return {}
    
    def wait_for_completion(self, prompt_id: str, timeout: int = 300) -> Dict:
        """
        Wait for generation to complete
        
        Args:
            prompt_id: Prompt ID
            timeout: Maximum wait time in seconds
            
        Returns:
            Generation result with image info
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            history = self.get_history(prompt_id)
            
            if prompt_id in history:
                return history[prompt_id]
            
            time.sleep(1)
        
        raise TimeoutError(f"Generation timed out after {timeout} seconds")
    
    def generate_image(
        self,
        prompt: str,
        negative_prompt: str = "",
        model: str = "RealVisXL_V4.0.safetensors",
        width: int = 1024,
        height: int = 1024,
        steps: int = 30,
        cfg: float = 7.0,
        sampler: str = "euler_ancestral",
        scheduler: str = "normal",
        seed: int = -1,
        safety_checker: bool = False
    ) -> Dict[str, Any]:
        """
        Generate an image using ComfyUI
        
        Args:
            prompt: Positive prompt
            negative_prompt: Negative prompt
            model: Model checkpoint name
            width: Image width
            height: Image height
            steps: Number of sampling steps
            cfg: CFG scale
            sampler: Sampler name
            scheduler: Scheduler name
            seed: Random seed (-1 for random)
            safety_checker: Whether to enable safety checker (NSFW filter)
            
        Returns:
            Dictionary with generation info and image path
        """
        if seed == -1:
            seed = int(time.time())
        
        # Build ComfyUI workflow
        workflow = self._build_workflow(
            prompt=prompt,
            negative_prompt=negative_prompt,
            model=model,
            width=width,
            height=height,
            steps=steps,
            cfg=cfg,
            sampler=sampler,
            scheduler=scheduler,
            seed=seed
        )
        
        # Queue the prompt
        prompt_id = self.queue_prompt(workflow)
        logger.info(f"Queued ComfyUI prompt: {prompt_id}")
        
        # Wait for completion
        result = self.wait_for_completion(prompt_id)
        
        # Extract image info
        outputs = result.get('outputs', {})
        images = []
        
        for node_id, node_output in outputs.items():
            if 'images' in node_output:
                for image_info in node_output['images']:
                    # Download image
                    image_bytes = self.get_image(
                        image_info['filename'],
                        image_info.get('subfolder', ''),
                        image_info.get('type', 'output')
                    )
                    
                    # Save to temp file
                    temp_file = tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix='.png'
                    )
                    temp_file.write(image_bytes)
                    temp_file.close()
                    
                    images.append(temp_file.name)
        
        return {
            'prompt_id': prompt_id,
            'images': images,
            'seed': seed,
            'metadata': {
                'prompt': prompt,
                'negative_prompt': negative_prompt,
                'model': model,
                'width': width,
                'height': height,
                'steps': steps,
                'cfg': cfg,
                'sampler': sampler,
                'scheduler': scheduler,
            }
        }
    
    def _build_workflow(
        self,
        prompt: str,
        negative_prompt: str,
        model: str,
        width: int,
        height: int,
        steps: int,
        cfg: float,
        sampler: str,
        scheduler: str,
        seed: int
    ) -> Dict:
        """
        Build ComfyUI workflow JSON
        This is a simplified workflow - can be customized for different models/nodes
        """
        return {
            "3": {
                "inputs": {
                    "seed": seed,
                    "steps": steps,
                    "cfg": cfg,
                    "sampler_name": sampler,
                    "scheduler": scheduler,
                    "denoise": 1,
                    "model": ["4", 0],
                    "positive": ["6", 0],
                    "negative": ["7", 0],
                    "latent_image": ["5", 0]
                },
                "class_type": "KSampler"
            },
            "4": {
                "inputs": {
                    "ckpt_name": model
                },
                "class_type": "CheckpointLoaderSimple"
            },
            "5": {
                "inputs": {
                    "width": width,
                    "height": height,
                    "batch_size": 1
                },
                "class_type": "EmptyLatentImage"
            },
            "6": {
                "inputs": {
                    "text": prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "7": {
                "inputs": {
                    "text": negative_prompt,
                    "clip": ["4", 1]
                },
                "class_type": "CLIPTextEncode"
            },
            "8": {
                "inputs": {
                    "samples": ["3", 0],
                    "vae": ["4", 2]
                },
                "class_type": "VAEDecode"
            },
            "9": {
                "inputs": {
                    "filename_prefix": "ComfyUI",
                    "images": ["8", 0]
                },
                "class_type": "SaveImage"
            }
        }


# Global instance
comfyui_service = ComfyUIService()

