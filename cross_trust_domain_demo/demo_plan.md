# Cross-Trust-Domain Identity Verification Demo

## Overview

This demo showcases how agents from different trust domains (representing different companies or organizations) can securely interact with each other after proper identity verification. The example demonstrates:

1. Two different users with separate API keys creating agents in different trust domains
2. Cross-domain identity verification between these agents
3. Conditional interaction based on successful verification

## Scenario

We have two main agents:

1. **Research Agent**: Created by Company A (Trust Domain: research-company.com)
   - Provides specialized research data and insights
   - Only shares information with verified agents from approved trust domains

2. **Blog Agent**: Created by Company B (Trust Domain: blog-publisher.com)
   - Creates blog content using research data
   - Needs to access research data from the Research Agent

## Demo Flow

### Part 1: Setup and Agent Creation

1. **Research Agent Setup**:
   - User 1 creates a Research Agent using their API key
   - The agent is assigned to the "research-company.com" trust domain
   - The agent is configured with research capabilities and data

2. **Blog Agent Setup**:
   - User 2 creates a Blog Agent using their API key (different from User 1)
   - The agent is assigned to the "blog-publisher.com" trust domain
   - The agent is configured with content creation capabilities

### Part 2: Cross-Domain Verification

1. **Verification Attempt**:
   - The Blog Agent attempts to access research data from the Research Agent
   - Before sharing data, the Research Agent verifies the Blog Agent's identity
   - Verification includes checking the Blog Agent's AZTP ID and trust domain

2. **Verification Outcomes**:
   - **Successful Verification**: If the Blog Agent's identity is verified, the Research Agent shares the requested data
   - **Failed Verification**: If verification fails, the Research Agent denies access

### Part 3: Secure Interaction

1. **Data Exchange**:
   - After successful verification, the Research Agent shares data with the Blog Agent
   - The Blog Agent uses this data to create blog content
   - The interaction is secure and authenticated

## Implementation Details

### File Structure

```
cross_trust_domain_demo/
├── demo_plan.md (this file)
├── src/
│   ├── research_agent.py (Company A's agent)
│   ├── blog_agent.py (Company B's agent)
│   └── demo.py (orchestrates the interaction)
└── README.md (instructions for running the demo)
```

### Environment Setup

Each agent will use a separate .env file with different API keys:

- `.env.research` for the Research Agent
- `.env.blog` for the Blog Agent

### Key Code Components

1. **Agent Creation**:
   - Each agent is created with its own API key and trust domain
   - Agents are created with isGlobalIdentity=False since they have specific trust domains
   - Each agent belongs to its respective trust domain (research-company.com or blog-publisher.com)

2. **Verification Logic**:
   - Implementation of identity verification between trust domains
   - Conditional access based on verification results

3. **Interaction Flow**:
   - Demonstration of secure data exchange after verification
   - Handling of verification failures

## Expected Outcomes

1. Successful verification between agents from different trust domains
2. Secure data exchange between verified agents
3. Access denial when verification fails

## Extensions

Potential extensions to this demo could include:

1. Multiple agents in each trust domain with hierarchical relationships
2. Time-limited verification tokens
3. Revocation of verification privileges
4. Verification based on specific capabilities or roles
