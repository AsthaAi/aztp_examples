# AZTP Parent-Child Identity Hierarchy Demo (Python)

This example demonstrates how to use the AZTP (Agentic Zero Trust Protocol) to create a secure hierarchical identity structure with multiple levels of parent-child relationships between agents and tools.

## Project Overview

```
┌─────────────────┐
│   SDRAgent      │
│   (Global)      │
└───────┬─────────┘
        │
        ├─────────────────┬─────────────────┐
        │                 │                 │
┌───────▼─────────┐ ┌─────▼───────┐ ┌───────▼─────────┐
│ CustomerService │ │ SalesAgent  │ │ SupportAgent   │
│     Agent       │ │             │ │                │
└───────┬─────────┘ └─────┬───────┘ └───────┬────────┘
        │                 │                 │
        │                 │                 ├─────────────┐
        │                 │                 │             │
┌───────▼─────────┐ ┌─────▼───────┐ ┌───────▼────────┐   │
│     Tools:      │ │RegionalSales│ │ TechSupport1   │   │
│ jira, slack,    │ │   Agents    │ │                │   │
│ notion, airtable│ └─────┬───────┘ └───────┬────────┘   │
└─────────────────┘       │                 │        ┌───▼────────────┐
                          │                 │        │ TechSupport2   │
                    ┌─────▼───────┐  ┌──────▼─────┐  │                │
                    │ LocalSales  │  │   Tools:    │  └───────┬───────┘
                    │   Agents    │  │jira_service,│          │
                    └─────┬───────┘  │github, etc. │  ┌───────▼─────┐
                          │          └─────────────┘  │   Tools:    │
                    ┌─────▼───────┐                   │jira_service,│
                    │   Tools:    │                   │github, etc. │
                    │figma, mem0, │                   └─────────────┘
                    │docusign, etc│
                    └─────────────┘
```

The project implements a complex hierarchical identity structure using AZTP's identity and trust mechanisms, demonstrating:
- Global identity for the root agent (SDRAgent)
- Multiple levels of parent-child relationships
- Trust domain management
- Identity verification at each level
- Tool security through parent-child relationships

## Prerequisites

- Python 3.8+
- Virtual environment (recommended)
- AZTP API Key

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd aztp_examples/parent_child_Identity_demo
```

2. Create and activate a virtual environment:
```bash
python -m venv parent-child-env
source parent-child-env/bin/activate  # On Windows: parent-child-env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

If you already have aztp_client installed, upgrade to latest
```bash
pip install --upgrade aztp-client
```

## Configuration

1. Create a `.env` file in the project root with the following variables:
```env
AZTP_API_KEY=your_aztp_api_key
```
:: Note: You can get API key from www.astha.ai

Check for more details:
https://pypi.org/project/aztp-client/

## AZTP Integration Guide

### Initializing AZTP Client

```python
from aztp_client import Aztp

client = Aztp(api_key=API_KEY)
trust_domain = "gptarticles.xyz"  # Your whitelisted trust domain
```

### Creating a Global Identity (Root Agent)

```python
# SDRAgent as global identity (root)
secured_sdr = await client.secure_connect(
    sdr_agent,  # Your agent object
    'sdrAgent',  # Agent name
    {
        "isGlobalIdentity": True  # No parent, global identity
    }
)

# Verify the identity
sdr_verified = await client.verify_identity(secured_sdr)
```

### Creating Child Agents (Level 1)

```python
# Create a child agent with the global agent as parent
secured_customer_service = await client.secure_connect(
    customer_service_agent,  # Your agent object
    'customer-service-1',  # Agent name
    {
        "parentIdentity": secured_sdr.identity.aztp_id,  # Link to parent
        "trustDomain": trust_domain,  # Trust domain
        "isGlobalIdentity": False  # Not a global identity
    }
)

# Verify the identity
cs_verified = await client.verify_identity(secured_customer_service)
```

### Creating Tools for Agents

```python
# Create a tool for the customer service agent
secured_jira = await client.secure_connect(
    jira,  # Your tool object
    'jira',  # Tool name
    {
        "parentIdentity": secured_customer_service.identity.aztp_id,  # Link to parent agent
        "trustDomain": trust_domain,
        "isGlobalIdentity": False
    }
)

# Verify the tool identity
jira_verified = await client.verify_identity(secured_jira)
```

### Creating Deeper Hierarchies (Level 2 and beyond)

```python
# Create a level 2 agent (child of a child)
secured_regional = await client.secure_connect(
    regional_sales,
    "regional-sales-1",
    {
        "parentIdentity": secured_sales.identity.aztp_id,  # Link to parent (which is itself a child)
        "trustDomain": trust_domain,
        "isGlobalIdentity": False
    }
)

# Verify the identity
regional_verified = await client.verify_identity(secured_regional)
```

## Running the Example

Execute the main script to see the full hierarchy in action:

```bash
python src/main.py
```

The script will:
1. Create a global SDRAgent
2. Create multiple child agents at different levels
3. Create tools for each agent
4. Verify all identities
5. Display the complete hierarchy

## Security Benefits

This hierarchical structure provides several security benefits:
- Clear parent-child relationships for access control
- Identity verification at each level
- Trust domain enforcement
- Secure tool access through parent agents
- Audit trail of all agent and tool activities (Coming Soon)

## 💬 Need Help?

- 📧 [Support Email](mailto:dev@astha.ai) 