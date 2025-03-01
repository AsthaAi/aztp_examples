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
    agentName: "blog-writer-1",
    isGlobalIdentity: true  // Uses aztp.network as trust domain
});
```

2. **Child Identity** (for agents under a trust domain):
```typescript
// Research agent as child with trust domain
const securedResearch = await client.secureConnect(researchAgent, {
    agentName: "research-assistant-1",
    parentIdentity: securedBlog.identity.aztpId,  // Link to parent
    trustDomain: "astha.ai",  // Explicit trust domain
    isGlobalIdentity: false
});
```

### Verifying Agent Identities

AZTP provides straightforward methods for identity verification:

1. **Direct Verification**:
```typescript
// Verify agent identity
const isValid = await client.verifyIdentity(agent);
```

2. **Get Identity Details**:
```typescript
// Get detailed identity information
const identity = await client.getIdentity(agent);
console.log('AZTP ID:', identity.aztpId);
console.log('Trust Domain:', identity.workloadInfo.trustDomain);
console.log('Status:', identity.status);
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
blog_ts/
├── src/
│   ├── agents/
│   │   ├── blog-agent.ts     # Blog writing agent
│   │   └── research-agent.ts # Research agent
│   └── main.ts              # Main application script
├── output/
│   └── blogs/               # Generated blog posts
├── package.json            # Project dependencies
├── tsconfig.json          # TypeScript configuration
└── README.md              # This file
```

## Usage

1. Build the project:
```bash
npm run build
```

2. Run the main script:
```bash
npm start
```

The script will:
1. Initialize and secure both agents using AZTP
2. Verify agent identities and trust relationships
3. Research the specified topic
4. Generate a blog post based on the research
5. Save the blog post to the output directory

## Security Features

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

### Key Security Features
- **Global Identity**: Blog Agent uses a global identity under `aztp.network`
- **Child Identity**: Research Agent operates under a specific trust domain
- **Identity Verification**: Both agents' identities are verified before operation
- **Trust Domain**: Proper trust domain separation and hierarchy
- **Secure Communication**: All agent interactions are secured through AZTP

## Error Handling

### Common AZTP Errors

1. **Invalid Trust Domain**:
   ```typescript
   try {
       await client.secureConnect(agent, {
           trustDomain: "invalid-domain",  // Will throw error
           // ...
       });
   } catch (error) {
       console.error("Trust domain validation failed:", error);
   }
   ```

2. **Identity Verification Failures**:
   ```typescript
   const isValid = await client.verifyIdentity(agent);
   if (!isValid) {
       throw new Error("Agent identity verification failed");
   }
   ```

3. **Parent Identity Issues**:
   ```typescript
   // Always verify parent identity exists before creating child
   const parentValid = await client.verifyIdentity(parentAgent);
   if (!parentValid) {
       throw new Error("Parent agent identity invalid");
   }
   ```

## Type Definitions

Key TypeScript interfaces for AZTP integration:

```typescript
interface SecureConnectOptions {
    agentName: string;
    isGlobalIdentity?: boolean;
    trustDomain?: string;
    parentIdentity?: string;
}

interface AztpIdentity {
    aztpId: string;
    workloadInfo: {
        trustDomain: string;
        workloadId: string;
        environment: string;
    };
    status: string;
}
```

## Contributing

Feel free to submit issues and enhancement requests! 