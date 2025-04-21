"""Main script for blog generation with secured agents."""

import os
import sys
from typing import Dict, Any
from dotenv import load_dotenv
from aztp_client import Aztp
from agents.research_agent import ResearchAgent
from agents.blog_agent import BlogAgent
from services.storage import StorageService
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_environment() -> Dict[str, str]:
    """Load environment variables and validate required keys."""
    load_dotenv()
    
    required_vars = ['OPENAI_API_KEY', 'AZTP_API_KEY']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return {
        'openai_key': os.getenv('OPENAI_API_KEY'),
        'aztp_key': os.getenv('AZTP_API_KEY')
    }

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
                await agent.disconnect()
        except Exception as e:
            logger.warning(f"Cleanup failed for agent: {str(e)}")

async def main() -> None:
    """Run the blog generation process."""
    client = None
    secured_research = None
    secured_blog = None
    secured_storage = None
    trust_domain = 'gptarticles.xyz'
    
    try:
        # Load environment variables
        env = setup_environment()
        
        # Initialize AZTP client
        client = Aztp(
            api_key=env['aztp_key']
        )
        
        logger.info("Initializing components...")
        # Create base components
        research_agent = ResearchAgent()
        blog_agent = BlogAgent()
        storage = StorageService()
        
        # Secure the components with AZTP
        try:
            # 1. Secure Blog Agent first (as root/parent)
            logger.info('Securing blog agent...')
            secured_blog = await client.secure_connect(
                blog_agent,
                "blog-writer-1",
                {
                    "isGlobalIdentity": True,  # Make this the root identity
                }
            )
            logger.info(f'Blog agent created: {secured_blog.identity.aztp_id}')
            
            # 2. Secure Research Agent as child of Blog
            logger.info('Securing research agent...')
            secured_research = await client.secure_connect(
                research_agent,
                "research-assistant-1",
                {
                    "isGlobalIdentity": False,
                    "trustDomain": trust_domain,
                    "parentIdentity": secured_blog.identity.aztp_id,
                    "linkTo": [secured_blog.identity.aztp_id]
                }
            )
            logger.info(f'Research agent created: {secured_research.identity.aztp_id}')

            # 3. Update Blog Agent with Research link
            logger.info('Updating blog agent with research agent link...')
            updated_blog = await client.secure_connect(
                blog_agent,
                "blog-writer-1",
                {
                    "isGlobalIdentity": True,
                    "linkTo": [secured_research.identity.aztp_id]
                }
            )
            logger.info(f'Updated blog agent created: {updated_blog.identity.aztp_id}')

            # 4. Secure Storage Service as child of Blog
            logger.info('Securing storage service...')
            secured_storage = await client.secure_connect(
                storage,
                "storage-service-1",
                {
                    "isGlobalIdentity": False,
                    "trustDomain": trust_domain,
                    "parentIdentity": updated_blog.identity.aztp_id,
                    "linkTo": [updated_blog.identity.aztp_id]  # Link to parent Blog Agent
                }
            )
            logger.info(f'Storage service created: {secured_storage.identity.aztp_id}')

            # 5. Final update to Blog Agent to link with Storage
            logger.info('Updating blog agent with storage service link...')
            final_blog = await client.secure_connect(
                blog_agent,
                "blog-writer-1",
                {
                    "isGlobalIdentity": True,
                    "linkTo": [secured_research.identity.aztp_id, secured_storage.identity.aztp_id]  # Only global identity and links
                }
            )
            logger.info(f'Final blog agent created: {final_blog.identity.aztp_id}')

            # Verify the connections
            logger.info('Verifying connections...')
            
            # Check Research <-> Blog connections
            research_to_blog = await client.verify_identity_connection(
                secured_research.identity.aztp_id,
                final_blog.identity.aztp_id
            )
            logger.info(f'Research -> Blog connection valid: {research_to_blog}')

            blog_to_research = await client.verify_identity_connection(
                final_blog.identity.aztp_id,
                secured_research.identity.aztp_id
            )
            logger.info(f'Blog -> Research connection valid: {blog_to_research}')

            # Check Storage <-> Blog connections
            storage_to_blog = await client.verify_identity_connection(
                secured_storage.identity.aztp_id,
                final_blog.identity.aztp_id
            )
            logger.info(f'Storage -> Blog connection valid: {storage_to_blog}')

            blog_to_storage = await client.verify_identity_connection(
                final_blog.identity.aztp_id,
                secured_storage.identity.aztp_id
            )
            logger.info(f'Blog -> Storage connection valid: {blog_to_storage}')

            if not all([research_to_blog, blog_to_research, storage_to_blog, blog_to_storage]):
                raise Exception("Connection verification failed - check trust chain")

        except Exception as e:
            raise Exception(f"Failed to secure components: {str(e)}")
        
        # Verify components
        research_valid = await verify_agent(client, secured_research, "Research")
        blog_valid = await verify_agent(client, updated_blog, "Blog")
        storage_valid = await verify_agent(client, secured_storage, "Storage")
        
        if not all([research_valid, blog_valid, storage_valid]):
            raise ValueError("Component verification failed - check identities and permissions")
        
        # Example topic
        topic = "Zero Trust Security in AI Systems"
        
        # Research phase
        logger.info(f"\nResearching topic: {topic}")
        try:
            research_data = await secured_research._agent.research(topic)
            if not research_data or 'findings' not in research_data:
                raise ValueError("Research data is incomplete or invalid")
            logger.info(f"Research completed: {research_data['metadata']['timestamp']}")
        except Exception as e:
            raise Exception(f"Research phase failed: {str(e)}")
        
        # Blog writing phase
        logger.info("\nGenerating blog post...")
        try:
            blog_data = await secured_blog._agent.create_blog(research_data)
            if not blog_data or 'content' not in blog_data:
                raise ValueError("Blog data is incomplete or invalid")
            logger.info(f"Blog created: {blog_data['metadata']['timestamp']}")
        except Exception as e:
            raise Exception(f"Blog generation failed: {str(e)}")
        
        # Save the blog post
        logger.info('\nSaving blog post...')
        blog_metadata = {
            'author': 'Technical Blog Writer',
            'researcher': 'Research Expert',
            'date': blog_data['metadata']['timestamp'],
            'status': 'draft'
        }
        saved_path = secured_storage.save_blog(blog_data['content'], blog_metadata)
        logger.info(f'Blog saved to: {saved_path}')

        # List available blog posts
        logger.info('\nListing available blog posts:')
        blogs = secured_storage.list_blogs()
        for blog in blogs:
            logger.info(f'- {blog}')
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up resources
        if client:
            await cleanup_resources(client, secured_research, updated_blog, secured_storage)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 