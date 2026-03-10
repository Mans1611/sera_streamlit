import requests
import time
import json
from typing import Dict, List, Any, Tuple
import numpy as np
from open_ai import OPENAI

class APIClient:
    """Client for making API requests to models"""
    
    @staticmethod
    def stt_inference(audio_data: bytes, model_url: str, timeout: int = 30) -> Tuple[Dict, float]:
        """
        Send audio to STT model API
        Returns: (response_dict, latency_ms)
        """
        start_time = time.time()
        try:
            files = {'file': ('audio.wav', audio_data, 'audio/wav')}
            response = requests.post(model_url, files=files, timeout=timeout)
            
            latency = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code == 200:
                return response.json(), latency
            else:
                return {"error": f"API Error: {response.status_code}"}, latency
                
        except requests.exceptions.Timeout:
            return {"error": "Request timeout"}, (time.time() - start_time) * 1000
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}, (time.time() - start_time) * 1000
    
    @staticmethod
    def llm_inference(prompt: str, model_url: str, timeout: int = 30) -> Tuple[str, float]:
        """
        Send text to LLM model API
        Returns: (response_text, latency_ms)
        """
        start_time = time.time()
        try:
            
            response,msg_content = OPENAI().infer(input=prompt)
            print("the response is ",response)
            latency = (time.time() - start_time) * 1000  # Convert to ms
            
         
            return msg_content, latency
                
        except requests.exceptions.Timeout:
            return "Request timeout", (time.time() - start_time) * 1000
        except requests.exceptions.RequestException as e:
            return str(e), (time.time() - start_time) * 1000
    
    @staticmethod
    def tts_inference(text: str, model_url: str, timeout: int = 30) -> Tuple[bytes, float]:
        """
        Send text to TTS model API
        Returns: (audio_bytes, latency_ms)
        """
        start_time = time.time()
        
        try:
            payload = {"input": text}
            response = requests.post(model_url, json=payload, timeout=timeout)
            print(response)
            latency = (time.time() - start_time) * 1000  # Convert to ms
            
            if response.status_code == 200:
                return response.content, latency
            else:
                return None, latency
                
        except requests.exceptions.Timeout:
            return None, (time.time() - start_time) * 1000
        except requests.exceptions.RequestException as e:
            return None, (time.time() - start_time) * 1000


class MetricsCalculator:
    """Calculate inference metrics"""
    
    @staticmethod
    def calculate_throughput(num_requests: int, total_time_ms: float) -> float:
        """Calculate throughput in requests per second"""
        if total_time_ms <= 0:
            return 0
        return (num_requests / total_time_ms) * 1000
    
    @staticmethod
    def calculate_avg_latency(latencies: List[float]) -> float:
        """Calculate average latency"""
        if not latencies:
            return 0
        return np.mean(latencies)
    
    @staticmethod
    def calculate_p95_latency(latencies: List[float]) -> float:
        """Calculate 95th percentile latency"""
        if not latencies:
            return 0
        return np.percentile(latencies, 95)
