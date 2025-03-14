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
        print(f"\nEnter your {api_key_var} value.")
        print("This should be a valid AZTP API key with permissions to issue identities.")
        print("Example format: 03bdae20400108817dsdsasdadsasd3a1124ad39021411743154de1f8e3")
        api_key_value = input(f"{api_key_var}=")
    
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
    print("\nIMPORTANT: You will need two different AZTP API keys (one for each agent).")
    print("These must be valid API keys with permissions to issue identities.")
    print("Sample or fake API keys will result in 403 Forbidden errors.")
    
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