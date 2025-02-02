# AZTP Examples

> Secure your AI agents with enterprise-grade zero-trust security.

```
┌──────────────┐                              ┌──────────────┐
│              │                              │    Blog      │
│   Agent A    │    Agentic Zero Trust       │   Agent      │
│              │◄─────── Protocol ──────────►│              │
│              │         (AZTP)              │              │
└──────────────┘                              └──────────────┘
       ▲                                           ▲
       │                                           │
       └─────────────► Identity  ◄─────────────----┘
```

## 🛡️ Security Features

AZTP (Agentic Zero Trust Protocol) brings enterprise security to AI agents through:
- 🔐 **Identity Management** with SPIFFE
- 🤝 **Secure Communication** between agents
- 📝 **Audit Logging** for all operations

## 🎯 Core Design Principles

AZTP follows a key design principle: **transparent security wrapping**. Here's how it works:

1. **Transparent Method Delegation**
   - AZTP wraps AI agents without modifying their core functionality
   - All agent methods work exactly as they would without AZTP
   - The security layer is completely transparent to the agent's operation

2. **Separation of Concerns**
   - Your code handles agent functionality
   - AZTP adds security without changing behavior
   - Use agent methods normally - AZTP is invisible to functionality

3. **What AZTP Adds**
   - Identity management (SPIFFE IDs)
   - Identity verification capabilities
   - Zero-trust security model
   
4. **What AZTP Doesn't Do**
   - Modify agent behavior
   - Change method signatures
   - Interfere with agent functionality
   - Alter agent outputs
   - Handle communication between agents (this happens at application level)

## 🚀 Getting Started

1. Get your API key at [astha.ai](https://astha.ai)
2. Follow the example-specific setup instructions

## 📚 Available Examples

### Blog Generation System
A multi-agent system that generates blog posts using AI agents:
- Research Agent: Gathers information on topics
- Blog Agent: Transforms research into blog posts
- Demonstrates secure agent-to-agent communication

## 💬 Need Help?

- 📧 [Support Email](mailto:dev@astha.ai)


