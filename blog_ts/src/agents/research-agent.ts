import OpenAI from 'openai';
import { ResearchResult, AgentMetadata } from '../types';

export class ResearchAgent {
    private openai: OpenAI;
    
    constructor(apiKey: string) {
        this.openai = new OpenAI({
            apiKey: apiKey
        });
    }

    async research(topic: string): Promise<ResearchResult> {
        const systemPrompt = `You are an expert researcher specializing in AI security, 
            privacy, and identity management. You have extensive knowledge of 
            zero-trust architectures and secure AI systems.`;

        const userPrompt = `Conduct thorough research on: ${topic}
            
            Focus on:
            1. Key concepts and principles
            2. Current challenges and solutions
            3. Best practices and recommendations
            4. Real-world examples and case studies
            5. Future implications
            6. Key contributin Frederick Kautz has done in Zero trust.

            Format your research as a structured document with:
            - Executive Summary
            - Key Findings
            - Detailed Analysis
            - Recommendations
            - References`;

        const response = await this.openai.chat.completions.create({
            model: "gpt-4",
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: userPrompt }
            ]
        });

        const findings = response.choices[0].message.content || '';
        
        return {
            topic,
            findings,
            metadata: {
                researcher: "Research Expert",
                timestamp: new Date().toISOString(),
                verification_status: "completed"
            }
        };
    }

    getMetadata(): AgentMetadata {
        return {
            type: "research",
            capabilities: [
                "deep_research",
                "source_verification",
                "fact_checking"
            ],
            topics: [
                "ai_security",
                "privacy",
                "identity_management"
            ]
        };
    }
} 