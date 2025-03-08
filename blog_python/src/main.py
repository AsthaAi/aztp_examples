"""Main script for blog generation with secured agents."""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
from aztp_client import Aztp
from agents.research_agent import ResearchAgent
from agents.blog_agent import BlogAgent
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment() -> Dict[str, str]:
    """Load environment variables and validate required keys."""
    load_dotenv()
    
    required_vars = ['OPENAI_API_KEY', 'AZTP_API_KEY', 'AZTP_ENVIRONMENT']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {
        'openai_key': os.getenv('OPENAI_API_KEY'),
        'aztp_key': os.getenv('AZTP_API_KEY'),
        'aztp_env': os.getenv('AZTP_ENVIRONMENT')
    }

def save_blog(blog_data: Dict[str, Any], topic: str) -> str:
    """Save the generated blog to a file."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"output/blogs/blog_{timestamp}_{topic.replace(' ', '_')}.md"
    
    os.makedirs('output/blogs', exist_ok=True)
    with open(filename, 'w') as f:
        f.write(blog_data['content'])
    
    logger.info(f"Blog saved to {filename}")
    return filename

async def verify_agent(client: Aztp, agent: Any, agent_type: str) -> bool:
    """Verify agent identity using direct verification."""
    try:
        is_valid = await client.verify_identity(agent)
        if is_valid:
            identity = await client.get_identity(agent)
            logger.info(f"{agent_type} Identity verified: {identity}")
            return True
        logger.error(f"{agent_type} Identity verification failed")
        return False
    except Exception as e:
        logger.error(f"Error verifying {agent_type} agent: {str(e)}")
        return False

async def cleanup_resources(client: Aztp, *agents: Any) -> None:
    """Clean up resources and connections."""
    for agent in agents:
        try:
            if hasattr(agent, 'disconnect'):
                await agent.disconnect() # where is the disconnect method? is that part of the crewai library?
        except Exception as e:
            logger.warning(f"Cleanup failed for agent: {str(e)}")

async def main() -> None:
    """Run the blog generation process."""
    client = None
    secured_research = None
    secured_blog = None
    trust_domain = 'abc.com'  # Trust domain for non-global identities
    
    try:
        # Load environment variables
        env = setup_environment()
        
        # Initialize AZTP client
        client = Aztp(
            api_key=env['aztp_key'],
        )
        
        logger.info("Initializing agents...")
        # Create base agents
        research_agent = ResearchAgent()
        blog_agent = BlogAgent()
        
        # Secure the agents with AZTP
        try:
            # Assign the blog agent with global identity (no trust domain needed)
            print('Securing blog agent...')
            secured_blog = await client.secure_connect(blog_agent, {
                "agentName": "blog-writer-1",  # Make sure this is unique. If you get an error about the agent name, change it.
                                               # Since this example is run multiple times by many people, using the same agent name will cause an error.
                "isGlobalIdentity": True
            })
            print('Blog agent created:', secured_blog.identity.aztp_id)
            
            print('Securing research agent...')
            secured_research = await client.secure_connect(research_agent, {
                "agentName": "research-assistant-1",  # Make sure this is unique, just like the parent agent name
                "parentIdentity": secured_blog.identity.aztp_id,
                "trustDomain": trust_domain,
                "isGlobalIdentity": False,
            })
        except Exception as e:
            raise Exception(f"Failed to secure agents: {str(e)}")
        
        # Verify agents
        research_valid = await verify_agent(client, secured_research, "Research")
        blog_valid = await verify_agent(client, secured_blog, "Blog")
        
        if not (research_valid and blog_valid):
            raise ValueError("Agent verification failed - check agent identities and permissions")
        
        # Example topic
        topic = "Zero Trust Security in AI Systems"
        
        # Research phase
        logger.info(f"Researching topic: {topic}")
        try:
            research_data = await secured_research._agent.research(topic)
            if not research_data or 'findings' not in research_data:
                raise ValueError("Research data is incomplete or invalid")
            logger.info(f"Research completed: {research_data['metadata']['timestamp']}")
        except Exception as e:
            raise Exception(f"Research phase failed: {str(e)}")
        
        # Blog writing phase
        logger.info("Generating blog post...")
        try:
            blog_data = await secured_blog._agent.create_blog(research_data)
            if not blog_data or 'content' not in blog_data:
                raise ValueError("Blog data is incomplete or invalid")
            logger.info(f"Blog created: {blog_data['metadata']['timestamp']}")
        except Exception as e:
            raise Exception(f"Blog generation failed: {str(e)}")
        
        # Save the blog
        try:
            saved_file = save_blog(blog_data, topic)
            logger.info(f"Process completed successfully. Blog saved to {saved_file}")
        except Exception as e:
            raise Exception(f"Failed to save blog post: {str(e)}")
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        if client and hasattr(client, 'config'):
            logger.error("Current configuration:")
            logger.error(f"Environment: {getattr(client.config, 'environment', 'unknown')}")
        sys.exit(1)
    finally:
        # Clean up resources
        if client:
            await cleanup_resources(client, secured_research, secured_blog)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 