# Refactoring Plan for Parent-Child Identity Demo

## Goals
- Improve code readability and maintainability
- Reduce code duplication
- Better organize the agent hierarchy
- Improve error handling
- Make the code more configurable
- Keep everything in a single file to maintain clear visibility of the hierarchy

## 1. Code Organization and Structure

### Add Clear Section Headers
```python
# =====================================================================
# SECTION: SDR AGENT (GLOBAL PARENT)
# =====================================================================
```

### Group Related Code
- Ensure all code related to a specific agent and its tools are grouped together
- Use consistent patterns for each agent branch

## 2. Extract Helper Functions

### Create Verification Helper
```python
async def verify_and_log(client, secured_entity, entity_name):
    """Verify an entity's identity and log the result."""
    verified = await client.verify_identity(secured_entity)
    print(f'{entity_name} Identity Verified: {verified}')
    return verified
```

### Create Secure Connect Helper
```python
async def secure_connect_entity(client, entity_obj, entity_name, parent_id, trust_domain, is_global=False):
    """Securely connect an entity with proper configuration."""
    config = {
        "isGlobalIdentity": is_global
    }
    
    if not is_global:
        config["parentIdentity"] = parent_id
        config["trustDomain"] = trust_domain
    
    secured_entity = await client.secure_connect(
        entity_obj,
        entity_name,
        config
    )
    print(f'{entity_name} AZTP ID: {secured_entity.identity.aztp_id}')
    return secured_entity
```

### Create Branch Functions
```python
async def create_customer_service_branch(client, parent_id, trust_domain):
    """Create the customer service branch including the agent and all its tools."""
    # Function implementation
    return secured_customer_service

async def create_sales_branch(client, parent_id, trust_domain):
    """Create the sales branch including all agents and tools in the hierarchy."""
    # Function implementation
    return secured_sales

async def create_support_branch(client, parent_id, trust_domain):
    """Create the support branch including all agents and tools in the hierarchy."""
    # Function implementation
    return secured_support
```

## 3. Improve Variable Naming and Documentation

### Add File-Level Docstring
```python
"""
Parent-Child Identity Demo

This script demonstrates the creation of a hierarchical structure of agents and tools
using the AZTP client for secure identity management. It creates a tree of agents with
the SDR agent as the global parent, and multiple branches of child agents and their tools.

The hierarchy is as follows:
- SDR Agent (Global)
  ├── Customer Service Agent
  │   └── Tools: Jira, Slack, Notion, Airtable
  ├── Sales Agent
  │   ├── Tools: Salesforce, Asana, Tableau, Gmail
  │   ├── Regional Sales Agents
  │   │   ├── Tools: Trello, Hubspot, Clickup, Zoom
  │   │   └── Local Sales Agents
  │   │       └── Tools: Figma, Mem0, DocuSign, LinkedIn
  └── Support Agent
      ├── Tools: Zendesk, Confluence, Teams, Monday
      └── Tech Support Agents
          └── Tools: Jira Service, GitHub, Notion, Slack
"""
```

### Add Function Docstrings
- Add comprehensive docstrings to all functions
- Explain parameters, return values, and side effects

## 4. Reduce Duplication

### Use Arrays/Dictionaries for Similar Items
```python
# Agent name definitions
AGENT_NAMES = {
    "sdr": "sdr-maestro",
    "customer_service": "customer-guardian",
    "sales": "sales-champion",
    "support": "support-sentinel",
    "regional_sales": ["regional-east-captain", "regional-west-captain"],
    "tech_support": ["tech-wizard", "tech-guru"],
    "local_sales": [
        "local-northeast-rep", "local-southeast-rep", 
        "local-northwest-rep", "local-southwest-rep"
    ]
}

# Tool name definitions
TOOL_NAMES = {
    "customer_service": {
        "jira": "jira-wizard",
        "slack": "slack-messenger",
        "notion": "notion-scribe",
        "airtable": "airtable-organizer"
    },
    "sales": {
        "salesforce": "salesforce-dynamo",
        "asana": "asana-taskmaster",
        "tableau": "tableau-visualizer",
        "gmail": "gmail-communicator"
    },
    # ... more tool definitions
}
```

### Use Loops for Repetitive Tasks
```python
# Create and secure tools for an agent
async def create_tools_for_agent(client, agent_id, trust_domain, tool_objects, tool_names):
    secured_tools = {}
    for tool_key, tool_obj in tool_objects.items():
        tool_name = tool_names[tool_key]
        secured_tool = await secure_connect_entity(
            client, tool_obj, tool_name, agent_id, trust_domain
        )
        verified = await verify_and_log(client, secured_tool, f"{tool_name} Tool")
        secured_tools[tool_key] = secured_tool
    return secured_tools
```

## 5. Improve Error Handling

### Add Try-Except Blocks for Each Major Section
```python
try:
    # Create Customer Service branch
    secured_customer_service = await create_customer_service_branch(client, secured_sdr.identity.aztp_id, trust_domain)
except Exception as e:
    print(f"Error creating Customer Service branch: {str(e)}")
    # Decide whether to continue or exit
```

### Add Validation
```python
def validate_config(api_key, trust_domain):
    """Validate configuration before proceeding."""
    if not api_key:
        raise ValueError("AZTP_API_KEY environment variable is not set")
    if not trust_domain:
        raise ValueError("Trust domain must be specified")
```

## 6. Configuration Management

### Extract Configuration to Constants
```python
# Configuration constants
TRUST_DOMAIN = "vcagents.ai"
DEBUG_MODE = False  # Set to True for more verbose output
```

### Use Environment Variables with Defaults
```python
# Load environment variables with defaults
API_KEY = os.getenv("AZTP_API_KEY", "")
TRUST_DOMAIN = os.getenv("AZTP_TRUST_DOMAIN", "vcagents.ai")
```

## 7. Visualization and Reporting

### Improve the Final Hierarchy Display
- Add more detailed information
- Consider using a library for tree visualization if appropriate
- Add statistics about successful connections

## Implementation Plan

1. **Phase 1: Reorganize Code Structure**
   - Add section headers
   - Group related code
   - Add docstrings

2. **Phase 2: Extract Helper Functions**
   - Create verification helper
   - Create secure connect helper
   - Create branch functions

3. **Phase 3: Reduce Duplication**
   - Define name constants
   - Create loops for repetitive tasks

4. **Phase 4: Improve Error Handling and Configuration**
   - Add try-except blocks
   - Extract configuration to constants
   - Add validation

5. **Phase 5: Enhance Visualization and Reporting**
   - Improve hierarchy display
   - Add progress indicators
   - Add summary statistics 