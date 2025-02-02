"""Blog Generation Agent implementation with AZTP security."""

from typing import Dict, Any
from datetime import datetime
from crewai import Agent, Task

class BlogAgent(Agent):
    """AI Blog Generation Agent with security capabilities."""
    
    def __init__(self):
        """Initialize the blog agent."""
        super().__init__(
            name="Blog Writer",
            role="Technical Blog Writer",
            goal="Create engaging and informative technical blog posts",
            backstory="""You are an expert technical writer specializing in AI, 
            security, and privacy topics. You excel at making complex concepts 
            accessible while maintaining technical accuracy.""",
            verbose=True
        )

    async def create_blog(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a blog post from research data.
        
        Args:
            research_data: Dictionary containing research findings and metadata

        Returns:
            Blog post content and metadata
        """
        task = Task(
            description=f"""
            Create an engaging blog post based on the following research:
            
            {research_data['findings']}
            
            Requirements:
            1. Clear and engaging title
            2. Executive summary/introduction
            3. Well-structured content with headings
            4. Technical accuracy
            5. Practical examples or applications
            6. Conclusion with key takeaways
            
            Original research by: {research_data['metadata']['researcher']}
            """,
            expected_output="A complete blog post in markdown format",
            agent=self
        )
        
        content = self.execute_task(task)
        
        return {
            "content": content,
            "metadata": {
                "author": self.role,
                "researcher": research_data['metadata']['researcher'],
                "timestamp": datetime.now().isoformat(),
                "status": "draft"
            }
        }

    def get_metadata(self) -> Dict[str, Any]:
        """Get agent metadata for AZTP."""
        return {
            "type": "blog",
            "capabilities": [
                "blog_writing",
                "technical_writing",
                "content_creation"
            ],
            "topics": [
                "ai_security",
                "privacy",
                "identity_management"
            ]
        } 