"""Main script for blog generation with secured agents."""

import asyncio
import os
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
from aztp_client import Aztp
from agents.research_agent import ResearchAgent
from agents.blog_agent import BlogAgent

# Load environment variables
load_dotenv()

async def verify_agent(client: Aztp, agent: Any, agent_type: str):
    """Verify agent identity."""
    is_valid = await agent.verify()
    identity = await client.get_identity(agent)
    print(f"\n{agent_type} Identity:", identity)
    return is_valid

async def main():
    """Run the blog generation process."""
    try:
        # Get API key from environment
        api_key = os.getenv("AZTP_API_KEY")
        if not api_key:
            raise ValueError("AZTP_API_KEY is required")
        
        # Initialize AZTP client
        client = Aztp(api_key=api_key)
        
        print("\nInitializing agents...")
        # Create base agents
        research_agent = ResearchAgent()
        blog_agent = BlogAgent()
        
        # Secure the agents with AZTP
        secured_research = await client.secure_connect(
            research_agent, 
            name="research-assistant"
        )
        secured_blog = await client.secure_connect(
            blog_agent, 
            name="blog-writer"
        )
        
        # Verify agents
        research_valid = await verify_agent(client, secured_research, "Research")
        blog_valid = await verify_agent(client, secured_blog, "Blog")
        
        if not (research_valid and blog_valid):
            raise ValueError("Agent verification failed")
        
        # Generate blog post
        topic = "Zero Trust Security in AI Systems"
        
        # Research phase
        print(f"\nResearching topic: {topic}")
        research_data = await secured_research.research(topic)
        print(f"Research completed: {research_data['metadata']['timestamp']}")
        
        # Blog writing phase
        print("\nGenerating blog post...")
        blog_data = await secured_blog.create_blog(research_data)
        print(f"Blog created: {blog_data['metadata']['timestamp']}")
        
        # Save blog post
        os.makedirs("output/blogs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"output/blogs/blog_{timestamp}.md"
        
        with open(filename, "w") as f:
            f.write(blog_data["content"])
        
        print(f"\nBlog saved to: {filename}")
        
    except Exception as e:
        print("\nError:", str(e))
        if hasattr(client, 'config'):
            print("\nCurrent configuration:")
            print(f"Base URL: {client.config.base_url}")
            print(f"Environment: {client.config.environment}")

if __name__ == "__main__":
    asyncio.run(main()) 