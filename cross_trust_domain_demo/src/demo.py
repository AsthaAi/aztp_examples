#!/usr/bin/env python3
"""
Cross-Trust-Domain Demo

This script demonstrates the interaction between agents from different trust domains.
It creates both a Research Agent and a Blog Agent, and shows how they verify each other's
identities before exchanging data.
"""

import os
import asyncio
import argparse
import json
import time
from dotenv import load_dotenv

# Import the agent classes
from research_agent import ResearchAgent
from blog_agent import BlogAgent

async def run_demo(topic=None, should_verify=True):
    """
    Run the cross-trust-domain demo.
    
    Args:
        topic: Optional topic to filter the research data
        should_verify: Whether to perform verification (set to False to demonstrate failed verification)
    """
    print("=" * 80)
    print("CROSS-TRUST-DOMAIN IDENTITY VERIFICATION DEMO")
    print("=" * 80)
    print("\nThis demo shows how agents from different trust domains can verify each other's")
    print("identities before exchanging data.")
    print("\nScenario:")
    print("1. Research Agent (trust domain: research-company.com)")
    print("2. Blog Agent (trust domain: blog-publisher.com)")
    print("3. Blog Agent requests data from Research Agent")
    print("4. Research Agent verifies Blog Agent's identity before sharing data")
    print("=" * 80)
    
    # Step 1: Create and set up the Research Agent
    print("\nSTEP 1: Creating Research Agent (Company A)")
    print("-" * 50)
    
    research_agent = ResearchAgent()
    research_agent_id = await research_agent.setup()
    
    if not research_agent_id:
        print("Failed to set up Research Agent. Exiting demo.")
        return
    
    print(f"\nResearch Agent created with ID: {research_agent_id}")
    print(f"Trust Domain: {research_agent.trust_domain}")
    
    # Step 2: Create and set up the Blog Agent
    print("\nSTEP 2: Creating Blog Agent (Company B)")
    print("-" * 50)
    
    blog_agent = BlogAgent()
    blog_agent_id = await blog_agent.setup()
    
    if not blog_agent_id:
        print("Failed to set up Blog Agent. Exiting demo.")
        return
    
    print(f"\nBlog Agent created with ID: {blog_agent_id}")
    print(f"Trust Domain: {blog_agent.trust_domain}")
    
    # Step 3: Blog Agent requests data from Research Agent
    print("\nSTEP 3: Blog Agent requests data from Research Agent")
    print("-" * 50)
    
    print("Blog Agent: I need research data to create a blog post.")
    print(f"Blog Agent: Requesting data from Research Agent with ID: {research_agent_id}")
    
    # If we want to demonstrate failed verification, modify the trust domain
    if not should_verify:
        print("\n[DEMO] Modifying trust domain to demonstrate failed verification")
        original_domain = blog_agent.trust_domain
        blog_agent.trust_domain = "untrusted-domain.com"
        print(f"[DEMO] Trust domain changed from {original_domain} to {blog_agent.trust_domain}")
    
    # Step 4: Research Agent verifies Blog Agent's identity
    print("\nSTEP 4: Research Agent verifies Blog Agent's identity")
    print("-" * 50)
    
    print("Research Agent: Before sharing data, I need to verify your identity.")
    
    # Perform verification
    is_verified = await research_agent.verify_requesting_agent(
        blog_agent_id, 
        blog_agent.trust_domain
    )
    
    # Step 5: Data exchange based on verification result
    print("\nSTEP 5: Data exchange based on verification result")
    print("-" * 50)
    
    if is_verified:
        print("Research Agent: Identity verified successfully. Sharing research data...")
        
        # Get research data
        research_data = research_agent.get_research_data(topic)
        
        # Create a response
        response = {
            "status": "success",
            "message": "Agent verified successfully",
            "data": research_data
        }
        
        print("\nResearch data shared:")
        if topic:
            print(f"Topic: {topic}")
        else:
            print("All topics")
        
        # Step 6: Blog Agent creates content with the research data
        print("\nSTEP 6: Blog Agent creates content with the research data")
        print("-" * 50)
        
        print("Blog Agent: Thank you for the data. Creating blog content...")
        
        # Create blog content
        blog_content = blog_agent.create_blog_content(response)
        
        if blog_content["status"] == "success":
            print("\nBlog content created successfully!")
            print("\nBLOG CONTENT:")
            print("=" * 80)
            print(f"Title: {blog_content['content']['title']}")
            print(f"Author: {blog_content['content']['author']}")
            print(f"Date: {blog_content['content']['date']}")
            
            for section in blog_content['content']['sections']:
                print(f"\n## {section['heading']}")
                print(section['content'])
            
            print("=" * 80)
        else:
            print(f"\nFailed to create blog content: {blog_content['message']}")
    else:
        print("Research Agent: Identity verification failed. Access denied.")
        print("Blog Agent: I couldn't access the research data due to verification failure.")
    
    # Demo summary
    print("\nDEMO SUMMARY")
    print("-" * 50)
    print(f"Research Agent ID: {research_agent_id}")
    print(f"Research Agent Trust Domain: {research_agent.trust_domain}")
    print(f"Blog Agent ID: {blog_agent_id}")
    print(f"Blog Agent Trust Domain: {blog_agent.trust_domain}")
    print(f"Verification Result: {'Success' if is_verified else 'Failed'}")
    print(f"Data Exchange: {'Completed' if is_verified else 'Denied'}")
    
    print("\nDEMO COMPLETED")
    print("=" * 80)

async def main():
    """Main function to run the demo."""
    parser = argparse.ArgumentParser(description='Cross-Trust-Domain Demo')
    parser.add_argument('--topic', help='Topic to filter the research data')
    parser.add_argument('--fail', action='store_true', help='Demonstrate failed verification')
    args = parser.parse_args()
    
    await run_demo(args.topic, not args.fail)

if __name__ == "__main__":
    asyncio.run(main()) 