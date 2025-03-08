# AZTP Blog Generation Example (TypeScript)

This example demonstrates how to use the AZTP (Agentic Zero Trust Protocol) to create a secure blog generation system with multiple collaborating agents in TypeScript.

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

## Prerequisites

- Node.js 16+
- TypeScript 4.5+
- AZTP API Key
- OpenAI API Key

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd aztp_examples/blog_ts
```

2. Install dependencies:
```bash
npm install
```

## Configuration

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key
AZTP_API_KEY=your_aztp_api_key
AZTP_ENVIRONMENT=production
```

## AZTP Integration Guide

### Initializing AZTP Client

```typescript
import aztp from 'aztp-client';

const client = aztp.initialize({
    apiKey: process.env.AZTP_API_KEY
});
```

### Securing Agents with AZTP

The `secureConnect` method is used to establish secure identities for agents. Here are the two main patterns:

1. **Global Identity** (for root-level agents):
```typescript
// Blog agent as global identity
const securedBlog = await client.secureConnect(blogAgent, {
    agentName: "blog-writer-1",  // Make sure this is unique. If you get an error about the agent name, change it.
                                // Since this example is run multiple times by many people, using the same agent name will cause an error.
    isGlobalIdentity: true  // Uses aztp.network as trust domain
});
```

2. **Child Identity** (for agents under a trust domain):
```typescript
// Research agent as child with trust domain
const securedResearch = await client.secureConnect(researchAgent, {
    agentName: "research-assistant-1",  // Make sure this is unique, just like the parent agent name
    parentIdentity: securedBlog.identity.aztpId,  // Link to parent
    trustDomain: "astha.ai",  // Explicit trust domain
    isGlobalIdentity: false
});
```