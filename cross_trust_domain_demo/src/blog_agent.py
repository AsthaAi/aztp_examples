#!/usr/bin/env python3
"""
Blog Agent Implementation

This script creates a Blog Agent with its own API key and trust domain.
The agent requests research data from the Research Agent after identity verification.
"""

import os
import asyncio
import argparse
import json
from dotenv import load_dotenv
from aztp_client import Aztp

class BlogAgent:
    """Blog Agent that creates content using research data."""
    
    def __init__(self):
        """Initialize the Blog Agent."""
        # Load environment variables from .env.blog
        env_file = ".env.blog"
        if not os.path.exists(env_file):
            print(f"Warning: {env_file} not found. Please run setup.py to create it.")
            print("For testing purposes, using a sample API key (will not work with actual AZTP services).")
            os.environ["AZTP_API_KEY_BLOG"] = "sample_blog_api_key_987654321"
        else:
            load_dotenv(env_file)
        
        # Get API key
        self.api_key = os.getenv("AZTP_API_KEY_BLOG")
        if not self.api_key:
            raise ValueError(f"AZTP_API_KEY_BLOG environment variable is not set in {env_file}. Run setup.py to configure it.")
        
        # Set trust domain for this agent
        self.trust_domain = "gptapps.ai"
        
        # Initialize agent object
        self.agent = {}
        self.secured_agent = None
        
        print(f"Blog Agent initialized with trust domain: {self.trust_domain}")
    
    async def setup(self):
        """Set up the Blog Agent with AZTP identity."""
        try:
            # Initialize AZTP client
            self.client = Aztp(api_key=self.api_key)
            
            print("\nCreating Blog Agent...")
            self.secured_agent = await self.client.secure_connect(
                self.agent,
                "blog-content-creator-Thursday",  # Agent name
                {
                    "isGlobalIdentity": False, 
                    "trustDomain": self.trust_domain
                }
            )
            
            print(f'Blog Agent AZTP ID: {self.secured_agent.identity.aztp_id}')
            
            # Verify the agent's own identity
            agent_verified = await self.client.verify_identity(self.secured_agent)
            print(f'Blog Agent Identity Self-Verified: {agent_verified}')
            
            return self.secured_agent.identity.aztp_id
            
        except Exception as error:
            print(f'Error setting up Blog Agent: {str(error)}')
            return None
    
    async def request_research_data(self, research_agent_id, topic=None):
        """
        Request research data from the Research Agent.
        
        Args:
            research_agent_id: The AZTP ID of the Research Agent
            topic: Optional topic to filter the research data
            
        Returns:
            dict: Research data if verification succeeds, error message otherwise
        """
        try:
            print(f"\nRequesting research data from agent with ID: {research_agent_id}")
            print(f"Blog Agent ID: {self.secured_agent.identity.aztp_id}")
            print(f"Blog Agent Trust Domain: {self.trust_domain}")
            
            # In a real implementation, this would make an API call to the Research Agent
            # For this demo, we'll simulate the interaction by running the research_agent.py script
            
            import subprocess
            import sys
            
            # Build the command to run the research_agent.py script
            cmd = [
                sys.executable,
                "src/research_agent.py",
                "--verify", self.secured_agent.identity.aztp_id,
                "--trust_domain", self.trust_domain
            ]
            
            # Add topic if provided
            if topic:
                cmd.extend(["--topic", topic])
            
            print(f"Executing command: {' '.join(cmd)}")
            
            # Run the command and capture the output
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # Parse the JSON response from the output
            # Find the JSON part in the output (it starts with {"status":)
            output = result.stdout
            json_start = output.find('{"status":')
            if json_start >= 0:
                json_str = output[json_start:]
                response = json.loads(json_str)
            else:
                # If JSON not found, return the raw output
                response = {
                    "status": "error",
                    "message": "Failed to parse response from Research Agent",
                    "raw_output": output
                }
            
            return response
            
        except Exception as error:
            print(f'Error requesting research data: {str(error)}')
            return {
                "status": "error",
                "message": f"Error: {str(error)}",
                "data": None
            }
    
    def create_blog_content(self, research_data):
        """
        Create blog content using the research data.
        
        Args:
            research_data: Research data from the Research Agent
            
        Returns:
            dict: Blog content
        """
        if not research_data or "data" not in research_data or not research_data["data"]:
            return {
                "status": "error",
                "message": "No research data available to create content",
                "content": None
            }
        
        data = research_data["data"]
        blog_content = {
            "title": "Latest Industry Insights and Trends",
            "author": "Blog Agent",
            "date": "2023-06-15",
            "sections": []
        }
        
        # Create content based on available data
        if "market_trends" in data:
            trends_section = {
                "heading": "Market Trends Analysis",
                "content": "Our latest analysis reveals significant growth in several key markets:\n\n"
            }
            
            for trend in data["market_trends"]:
                trends_section["content"] += f"- {trend['topic']}: {trend['growth_rate']}% growth rate, led by {', '.join(trend['key_players'])}\n"
            
            blog_content["sections"].append(trends_section)
        
        if "industry_insights" in data:
            insights_section = {
                "heading": "Industry Insights",
                "content": "Key insights from our research team:\n\n"
            }
            
            for industry, insight in data["industry_insights"].items():
                insights_section["content"] += f"- {industry.capitalize()}: {insight}\n"
            
            blog_content["sections"].append(insights_section)
        
        if "future_predictions" in data:
            predictions_section = {
                "heading": "Future Outlook",
                "content": "Our experts predict the following trends in the coming years:\n\n"
            }
            
            for prediction in data["future_predictions"]:
                predictions_section["content"] += f"- {prediction}\n"
            
            blog_content["sections"].append(predictions_section)
        
        return {
            "status": "success",
            "message": "Blog content created successfully",
            "content": blog_content
        }

async def main():
    """Main function to run the Blog Agent."""
    parser = argparse.ArgumentParser(description='Blog Agent')
    parser.add_argument('--research_agent_id', required=True, help='AZTP ID of the Research Agent')
    parser.add_argument('--topic', help='Topic to filter the research data')
    args = parser.parse_args()
    
    # Create and set up the Blog Agent
    blog_agent = BlogAgent()
    await blog_agent.setup()
    
    # Request research data from the Research Agent
    print("\nRequesting research data from Research Agent...")
    research_data = await blog_agent.request_research_data(args.research_agent_id, args.topic)
    
    if research_data["status"] == "success":
        print("\nResearch data received successfully!")
        
        # Create blog content using the research data
        print("\nCreating blog content...")
        blog_content = blog_agent.create_blog_content(research_data)
        
        if blog_content["status"] == "success":
            print("\nBlog content created successfully!")
            print("\nBlog Content:")
            print(f"Title: {blog_content['content']['title']}")
            print(f"Author: {blog_content['content']['author']}")
            print(f"Date: {blog_content['content']['date']}")
            
            for section in blog_content['content']['sections']:
                print(f"\n## {section['heading']}")
                print(section['content'])
        else:
            print(f"\nFailed to create blog content: {blog_content['message']}")
    else:
        print(f"\nFailed to get research data: {research_data['message']}")
        if "raw_output" in research_data:
            print("\nRaw output from Research Agent:")
            print(research_data["raw_output"])

if __name__ == "__main__":
    asyncio.run(main()) 