# AZTP Blog Generation Example (TypeScript)

This example demonstrates how to implement secure agent identities and trust relationships using the AZTP (Agentic Zero Trust Protocol) in a blog generation system.

## AZTP Identity Architecture

```
┌──────────────┐                              ┌──────────────┐
│  Research    │                              │    Blog      │
│   Agent      │    Agentic Zero Trust       │   Agent      │
│  (Child ID)  │◄─────── Protocol ──────────►│ (Global ID)  │
│              │         (AZTP)              │              │
└──────────────┘                              └──────────────┘
```

### Identity Types

1. **Global Identity (Blog Agent)**
   - Root-level identity using `aztp.network` as trust domain
   - Acts as the parent identity for child agents
   - Has full control over blog generation and publishing
   - Establishes trust boundaries for the system

2. **Child Identity (Research Agent)**
   - Operates under the Blog Agent's trust domain
   - Limited scope and permissions
   - Must verify identity with parent for operations
   - Focused on secure data gathering and research

## Prerequisites

- Node.js 16+
- TypeScript 4.5+
- AZTP API Key
- OpenAI API Key

## Identity Configuration

Create a `.env` file with required API keys:
```env
OPENAI_API_KEY=your_openai_api_key
AZTP_API_KEY=your_aztp_api_key
AZTP_ENVIRONMENT=production
```

## AZTP Identity Implementation

### 1. Initialize AZTP Client

```typescript
import aztp from 'aztp-client';

const client = aztp.initialize({
    apiKey: process.env.AZTP_API_KEY
});
```

### 2. Establish Global Identity

```typescript
// Blog agent with global identity
const securedBlog = await client.secureConnect(blogAgent, {
    agentName: "blog-writer-1",  // Unique global identifier
    isGlobalIdentity: true       // Automatically uses aztp.network as trust domain
});
```

### 3. Create Child Identity

```typescript
// Research agent with child identity
const securedResearch = await client.secureConnect(researchAgent, {
    agentName: "research-assistant-1",           // Unique child identifier
    parentIdentity: securedBlog.identity.aztpId, // Link to parent's AZTP ID
    trustDomain: "astha.ai",                     // Custom trust domain
    isGlobalIdentity: false                      // Operates under parent's domain
});
```

### 4. Identity Verification

```typescript
// Verify child identity with parent
const isValid = await securedBlog.verifyIdentity(securedResearch.identity);

if (!isValid) {
    throw new Error("Invalid child identity");
}
```

## Security Features

1. **Zero Trust Architecture**
   - Every agent must prove identity for each operation
   - No implicit trust between agents
   - Cryptographic verification of all communications

2. **Identity Hierarchy**
   - Clear parent-child relationships
   - Scoped permissions and access control
   - Trust domain isolation

3. **Secure Communication**
   - End-to-end encrypted messages
   - Identity-based message signing
   - Tamper-proof data exchange

## Best Practices

1. **Identity Naming**
   - Use unique, descriptive agent names
   - Follow a consistent naming convention
   - Avoid reusing identity names

2. **Trust Domain Management**
   - Keep global identities minimal
   - Group related agents under same trust domain
   - Regularly rotate identity credentials

3. **Error Handling**
   - Always verify identity before operations
   - Handle identity verification failures gracefully
   - Log identity-related events for audit

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
    isGlobalIdentity: true      // Automatically uses aztp.network as trust domain, no need to specify trustDomain
});
```

2. **Child Identity** (for agents under a trust domain):
```typescript
// Research agent as child with trust domain
const securedResearch = await client.secureConnect(researchAgent, {
    agentName: "research-assistant-1",  // Make sure this is unique, just like the parent agent name
    parentIdentity: securedBlog.identity.aztpId,  // Link to parent
    trustDomain: "astha.ai",  // Explicit trust domain required for child identities
    isGlobalIdentity: false
});
```