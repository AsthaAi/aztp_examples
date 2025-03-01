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
        "agentName": "blog-writer-1",
        "isGlobalIdentity": True  # Uses aztp.network as trust domain
    }
)
```

2. **Child Identity** (for agents under a trust domain):
```python
# Research agent as child with trust domain
secured_research = await client.secure_connect(
    research_agent,
    {
        "agentName": "research-assistant-1",
        "parentIdentity": secured_blog.identity.aztp_id,  # Link to parent
        "trustDomain": "astha.ai",  # Explicit trust domain
        "isGlobalIdentity": False
    }
)
```

### Verifying Agent Identities

AZTP provides multiple methods for identity verification:

1. **Direct Verification**:
```python
# Simplest and recommended method
is_valid = await client.verify_identity(agent)
```

2. **Identity Details**:
```python
# Get detailed identity information
identity = await client.get_identity(agent)
print(f"AZTP ID: {identity.aztpId}")
print(f"Trust Domain: {identity.workloadInfo.trustDomain}")
print(f"Status: {identity.status}")
```

### Understanding AZTP IDs

AZTP IDs follow this format:
```
aztp://<trust_domain>/<agent_name>
```

Examples:
- Global Identity: `aztp://blog-writer-1`
- Domain Identity: `aztp://astha.ai/research-assistant-1`

## Project Structure

```
blog_python/
├── src/
│   ├── agents/
│   │   ├── blog_agent.py     # Blog writing agent
│   │   └── research_agent.py # Research agent
│   └── main.py              # Main application script
├── output/
│   └── blogs/               # Generated blog posts
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Usage

Run the main script:
```bash
python src/main.py
```

The script will:
1. Initialize and secure both agents using AZTP
2. Verify agent identities and trust relationships
3. Research the specified topic
4. Generate a blog post based on the research
5. Save the blog post to the output directory

## Security Features

- **Global Identity**: Blog Agent uses a global identity under `aztp.network`
- **Child Identity**: Research Agent operates under a specific trust domain with parent-child relationship
- **Identity Verification**: Both agents' identities are verified before operation
- **Trust Domain**: Proper trust domain separation and hierarchy
- **Secure Communication**: All agent interactions are secured through AZTP

### Identity Hierarchy

```
┌─────────────────────┐
│    Blog Agent       │
│  (Global Identity)  │
│   aztp.network     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Research Agent    │
│   (Child Identity)  │
│     astha.ai       │
└─────────────────────┘
```

## Dependencies

- 🔐 Agent identity management with SPIFFE
- 🤝 Secure agent-to-agent communication
- ✅ Identity verification before operations
- 📝 Automatic method delegation

## Output

Generated blogs are saved in the `output/blogs/` directory with timestamps and topic-based filenames.

## Error Handling

The system includes comprehensive error handling for:
- Missing environment variables
- Agent verification failures
- Research and blog generation errors
- File system operations

### Common AZTP Errors

1. **Invalid Trust Domain**:
   - Ensure trust domains match the expected format
   - Verify parent-child relationships are properly established

2. **Identity Verification Failures**:
   - Check if the agent was properly secured with `secure_connect`
   - Verify the AZTP API key is valid
   - Ensure the parent identity exists for child agents

3. **Connection Issues**:
   - Verify network connectivity
   - Check AZTP service status
   - Validate API key permissions

## Contributing

Feel free to submit issues and enhancement requests! 
