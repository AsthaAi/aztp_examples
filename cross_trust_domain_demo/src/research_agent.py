#!/usr/bin/env python3
"""
Research Agent Implementation

This script creates a Research Agent with its own API key and trust domain.
The agent provides research data to verified agents from approved trust domains.
"""

import os
import asyncio
import argparse
import json
from dotenv import load_dotenv
from aztp_client import Aztp

# Research data that will be shared with verified agents
RESEARCH_DATA = {
    "market_trends": [
        {"topic": "AI in Healthcare", "growth_rate": 28.5, "key_players": ["Company X", "Company Y", "Company Z"]},
        {"topic": "Renewable Energy", "growth_rate": 15.2, "key_players": ["Green Co", "SunPower", "WindTech"]},
        {"topic": "Cybersecurity", "growth_rate": 22.1, "key_players": ["SecureTech", "CyberShield", "DataGuard"]}
    ],
    "industry_insights": {
        "healthcare": "AI-driven diagnostics are revolutionizing patient care with 35% faster diagnosis times.",
        "energy": "Solar efficiency has increased by 12% in the last year, driving adoption in commercial sectors.",
        "technology": "Quantum computing is expected to disrupt cryptography within the next 5-7 years."
    },
    "future_predictions": [
        "Remote work technologies will see continued investment through 2025",
        "Blockchain applications beyond cryptocurrency will grow by 40% annually",
        "Personalized medicine will become standard practice by 2030"
    ]
}

class ResearchAgent:
    """Research Agent that provides data to verified agents."""
    
    def __init__(self):
        """Initialize the Research Agent."""
        # Load environment variables from .env.research
        env_file = ".env.research"
        if not os.path.exists(env_file):
            print(f"ERROR: {env_file} not found.")
            print(f"Please run 'python setup.py' to create the {env_file} file with a valid API key.")
            print("A valid AZTP API key with identity issuance permissions is required.")
            raise ValueError(f"Missing {env_file} file. Run setup.py first.")
        
        load_dotenv(env_file)
        
        # Get API key
        self.api_key = os.getenv("AZTP_API_KEY_RESEARCH")
        if not self.api_key:
            print(f"ERROR: AZTP_API_KEY_RESEARCH environment variable is not set in {env_file}.")
            print(f"Please run 'python setup.py' to configure a valid API key.")
            raise ValueError(f"AZTP_API_KEY_RESEARCH not found in {env_file}")
        
        # Set trust domain for this agent
        self.trust_domain = "gptarticles.xyz"
        
        # Initialize agent object
        self.agent = {}
        self.secured_agent = None
        
        # Approved trust domains that can access research data
        self.approved_trust_domains = ["gptapps.ai", "gptarticles.xyz"]
        
        print(f"Research Agent initialized with trust domain: {self.trust_domain}")
        print(f"API Key: {self.api_key[:8]}...")
    
    async def setup(self):
        """Set up the Research Agent with AZTP identity."""
        try:
            # Initialize AZTP client
            self.client = Aztp(api_key=self.api_key)
            
            print("\nCreating Research Agent...")
            self.secured_agent = await self.client.secure_connect(
                self.agent,
                "research-data-provider-thursday",  # Agent name
                {
                    "isGlobalIdentity": False, 
                    "trustDomain": self.trust_domain,
                    'approvedTrustDomains': ['gptapps.ai', 'gptarticles.xyz']
                }
            )
            
            print(f'Research Agent AZTP ID: {self.secured_agent.identity.aztp_id}')
            
            # Verify the agent's own identity
            agent_verified = await self.client.verify_identity(self.secured_agent)
            print(f'Research Agent Identity Self-Verified: {agent_verified}')
            
            return self.secured_agent.identity.aztp_id
            
        except Exception as error:
            print(f'Error setting up Research Agent: {str(error)}')
            if "403" in str(error) or "Forbidden" in str(error) or "Unauthorized" in str(error):
                print("\nAUTHORIZATION ERROR: Your API key was rejected by the AZTP service.")
                print("Please ensure you're using a valid API key with the correct permissions.")
                print("Run 'python setup.py' to update your API key.")
            return None
    
    async def verify_requesting_agent(self, agent_id, agent_trust_domain):
        """
        Verify the identity of an agent requesting data.
        
        Args:
            agent_id: The AZTP ID of the requesting agent
            agent_trust_domain: The trust domain of the requesting agent
            
        Returns:
            bool: True if verification succeeds, False otherwise
        """
        try:
            print(f"\nVerifying agent with ID: {agent_id} from trust domain: {agent_trust_domain}")
            
            # First check if the trust domain is in our approved list
            if agent_trust_domain not in self.approved_trust_domains:
                print(f"Trust domain {agent_trust_domain} is not in the approved list")
                return False
            
            # Extract the agent name from the AZTP ID
            # Format is typically: aztp://domain/workload/production/node/agent-name
            agent_parts = agent_id.split('/')
            if len(agent_parts) >= 6:
                agent_name = agent_parts[-1]  # Get the last part which should be the agent name
                print(f"Extracted agent name: {agent_name}")
                
                # Verify the agent's identity using its name and trust domain
                is_verified = await self.client.verify_identity_using_agent_name(
                    agent_name,
                    trust_domain=agent_trust_domain
                )
                
                print(f"Agent verification result: {is_verified}")
                return is_verified
            else:
                print(f"Could not extract agent name from ID: {agent_id}")
                return False
            
        except Exception as error:
            print(f'Error verifying agent: {str(error)}')
            return False
    
    def get_research_data(self, topic=None):
        """
        Get research data, optionally filtered by topic.
        
        Args:
            topic: Optional topic to filter the data
            
        Returns:
            dict: Research data
        """
        if topic:
            # Filter data by topic
            filtered_data = {}
            
            if topic.lower() == "market_trends":
                filtered_data["market_trends"] = RESEARCH_DATA["market_trends"]
            elif topic.lower() == "industry_insights":
                filtered_data["industry_insights"] = RESEARCH_DATA["industry_insights"]
            elif topic.lower() == "future_predictions":
                filtered_data["future_predictions"] = RESEARCH_DATA["future_predictions"]
            else:
                # Topic not found
                return {"error": f"Topic '{topic}' not found in research data"}
            
            return filtered_data
        else:
            # Return all data
            return RESEARCH_DATA
    
    async def handle_data_request(self, agent_id, agent_trust_domain, topic=None):
        """
        Handle a data request from another agent.
        
        Args:
            agent_id: The AZTP ID of the requesting agent
            agent_trust_domain: The trust domain of the requesting agent
            topic: Optional topic to filter the data
            
        Returns:
            dict: Research data if verification succeeds, error message otherwise
        """
        # Verify the requesting agent
        is_verified = await self.verify_requesting_agent(agent_id, agent_trust_domain)
        
        if is_verified:
            print(f"Agent verified successfully. Providing research data...")
            return {
                "status": "success",
                "message": "Agent verified successfully",
                "data": self.get_research_data(topic)
            }
        else:
            print(f"Agent verification failed. Denying access to research data.")
            return {
                "status": "error",
                "message": "Agent verification failed. Access denied.",
                "data": None
            }

async def main():
    """Main function to run the Research Agent."""
    parser = argparse.ArgumentParser(description='Research Agent')
    parser.add_argument('--verify', help='Verify and respond to an agent with the given ID')
    parser.add_argument('--trust_domain', help='Trust domain of the agent to verify')
    parser.add_argument('--topic', help='Topic to filter the research data')
    args = parser.parse_args()
    
    # Create and set up the Research Agent
    research_agent = ResearchAgent()
    agent_id = await research_agent.setup()
    
    if args.verify and args.trust_domain:
        # Handle verification and data request
        result = await research_agent.handle_data_request(
            args.verify, 
            args.trust_domain,
            args.topic
        )
        print("\nResponse to agent request:")
        print(json.dumps(result, indent=2))
    else:
        # Just print the agent ID for use by other agents
        print("\nResearch Agent is ready to receive verification requests.")
        print(f"Use this AZTP ID when connecting from other agents: {agent_id}")
        print("Approved trust domains:", research_agent.approved_trust_domains)

if __name__ == "__main__":
    asyncio.run(main()) 