# AZTP Blog Generation Example (Python)

This example demonstrates how to use the AZTP (Agentic Zero Trust Protocol) to create a secure blog generation system with multiple collaborating agents.

## Project Overview


```
┌──────────────┐                              ┌──────────────┐
│  Research    │                              │    Blog      │
│   Agent      │    Agentic Zero Trust       │   Agent      │
│              │◄─────── Protocol ──────────►│              │
│  (OpenAI)    │         (AZTP)              │  (OpenAI)    │
└──────────────┘                              └──────────────┘
```
The project implements a secure blog generation system using two main agents:
- **Blog Agent** (Global Identity): Responsible for creating and formatting blog posts
- **Research Agent** (Child Identity): Handles research and data gathering for blog topics

Both agents are secured using AZTP's identity and trust mechanisms, demonstrating proper hierarchical identity management and secure agent collaboration.

## Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- AZTP API Key
- OpenAI API Key

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd aztp_examples/blog_python
```

2. Create and activate a virtual environment:
```bash
python -m venv blog-env
source blog-env/bin/activate  # On Windows: blog-env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
AZTP_API_KEY=your_aztp_api_key
AZTP_ENVIRONMENT=production
```

## AZTP Integration Guide

### Initializing AZTP Client

```python
from aztp_client import Aztp

client = Aztp(
    api_key=env['aztp_key']
)
```

### Securing Agents with AZTP

The `secure_connect` method is used to establish secure identities for agents. There are two main patterns:

1. **Global Identity** (for root-level agents):
```python
# Blog agent as global identity
secured_blog = await client.secure_connect(
    blog_agent,
    {
        "agentName": "blog-writer-1",  # Make sure this is unique. If you get an error about the agent name, change it.
                                      # Since this example is run multiple times by many people, using the same agent name will cause an error.
        "isGlobalIdentity": True  # Uses aztp.network as a globaltrust domain
    }
)
```

2. **Child Identity** (for agents under a trust domain):
```python
# Research agent as child with trust domain
secured_research = await client.secure_connect(
    research_agent,
     "research-assistant-1"
    {
        "parentIdentity": secured_blog.identity.aztp_id,  # Link to parent
        "trustDomain": "astha.ai",  # Explicit trust domain
        "isGlobalIdentity": False
    }
)
```