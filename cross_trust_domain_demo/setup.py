#!/usr/bin/env python3
"""
Setup script for the Cross-Trust-Domain Identity Verification Demo.

This script helps users create the necessary .env files with their API keys.
"""

import os
import sys
import shutil

def create_env_file(file_name, api_key_var, api_key_value=None):
    """Create an environment file with the given API key."""
    if os.path.exists(file_name):
        overwrite = input(f"The file {file_name} already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print(f"Skipping {file_name}")
            return False
    
    if not api_key_value:
        api_key_value = input(f"Enter your {api_key_var} value: ")
    
    with open(file_name, 'w') as f:
        f.write(f"# Environment file for the Cross-Trust-Domain Demo\n")
        f.write(f"{api_key_var}={api_key_value}\n")
    
    print(f"Created {file_name} with {api_key_var}")
    return True

def main():
    """Main function to set up the demo environment."""
    print("=" * 80)
    print("Cross-Trust-Domain Demo Setup")
    print("=" * 80)
    print("\nThis script will help you set up the necessary environment files for the demo.")
    print("You will need two different AZTP API keys (one for each agent).")
    
    # Check if sample files exist and create them if needed
    if not os.path.exists('.env.research.sample'):
        with open('.env.research.sample', 'w') as f:
            f.write("# Sample .env file for the Research Agent\n")
            f.write("# Rename this file to .env.research and replace with your actual API key\n\n")
            f.write("AZTP_API_KEY_RESEARCH=your_research_agent_api_key_here\n")
    
    if not os.path.exists('.env.blog.sample'):
        with open('.env.blog.sample', 'w') as f:
            f.write("# Sample .env file for the Blog Agent\n")
            f.write("# Rename this file to .env.blog and replace with your actual API key\n\n")
            f.write("AZTP_API_KEY_BLOG=your_blog_agent_api_key_here\n")
    
    # Option to use sample values for quick testing
    use_sample = input("\nDo you want to use sample API keys for testing? (y/n): ")
    
    if use_sample.lower() == 'y':
        print("\nUsing sample API keys. Note: These are for demonstration only and won't work with actual AZTP services.")
        research_key = "sample_research_api_key_123456789"
        blog_key = "sample_blog_api_key_987654321"
        
        create_env_file('.env.research', 'AZTP_API_KEY_RESEARCH', research_key)
        create_env_file('.env.blog', 'AZTP_API_KEY_BLOG', blog_key)
    else:
        print("\nSetting up Research Agent environment:")
        create_env_file('.env.research', 'AZTP_API_KEY_RESEARCH')
        
        print("\nSetting up Blog Agent environment:")
        create_env_file('.env.blog', 'AZTP_API_KEY_BLOG')
    
    print("\nSetup complete!")
    print("\nYou can now run the demo with:")
    print("  python src/demo.py")
    print("\nOr run the agents separately:")
    print("  python src/research_agent.py")
    print("  python src/blog_agent.py --research_agent_id <AZTP-ID>")
    print("\nFor more information, see the README.md file.")

if __name__ == "__main__":
    main() 