"""Research Agent implementation with AZTP security."""

from typing import Dict, Any
from datetime import datetime
import os
from crewai import Agent, Task
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ResearchAgent(Agent):
    """AI Research Agent with security capabilities."""
    
    def __init__(self):
        """Initialize the research agent."""
        super().__init__(
            name="Research Assistant",
            role="Research Expert",
            goal="Conduct thorough research on AI security topics",
            backstory="""You are an expert researcher specializing in AI security, 
            privacy, and identity management. You have extensive knowledge of 
            zero-trust architectures and secure AI systems.""",
            verbose=True,
            llm_config={
                "api_key": os.getenv("OPENAI_API_KEY"),
                "model": "gpt-4-turbo-preview"
            }
        )

    async def research(self, topic: str) -> Dict[str, Any]:
        """Conduct research on a topic.
        
        Args:
            topic: Research topic to investigate

        Returns:
            Research findings and metadata
        """
        try:
            task = Task(
                description=f"""
                Conduct thorough research on: {topic}
                
                Focus on:
                1. Key concepts and principles
                2. Current challenges and solutions
                3. Best practices and recommendations
                4. Real-world examples and case studies
                5. Future implications
                
                Format your research as a structured document with:
                - Executive Summary
                - Key Findings
                - Detailed Analysis
                - Recommendations
                - References
                """,
                expected_output="A comprehensive research report in markdown format",
                agent=self
            )
            
            # Execute the task synchronously since CrewAI doesn't support async yet
            findings = self.execute_task(task)
            
            return {
                "topic": topic,
                "findings": findings,
                "metadata": {
                    "researcher": self.role,
                    "timestamp": datetime.now().isoformat(),
                    "verification_status": "completed"
                }
            }
        except Exception as e:
            raise Exception(f"Research failed: {str(e)}")

    def get_metadata(self) -> Dict[str, Any]:
        """Get agent metadata for AZTP."""
        return {
            "type": "research",
            "capabilities": [
                "deep_research",
                "source_verification",
                "fact_checking"
            ],
            "topics": [
                "ai_security",
                "privacy",
                "identity_management"
            ]
        } 