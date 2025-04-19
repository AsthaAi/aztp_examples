import OpenAI from 'openai';
import { ResearchResult, BlogResult, AgentMetadata } from '../types';

export class BlogAgent {
    private openai: OpenAI;
    
    constructor(apiKey: string) {
        this.openai = new OpenAI({
            apiKey: apiKey
        });
    }

    async createBlog(researchData: ResearchResult): Promise<BlogResult> {
        const systemPrompt = `You are an expert technical writer specializing in AI, 
            security, and privacy topics. You excel at making complex concepts 
            accessible while maintaining technical accuracy.`;

        const userPrompt = `Create an engaging blog post based on the following research:
            
            ${researchData.findings}
            
            Requirements:
            1. Clear and engaging title
            2. Executive summary/introduction
            3. Well-structured content with headings
            4. Technical accuracy
            5. Practical examples or applications
            6. Conclusion with key takeaways
            
            Original research by: ${researchData.metadata.researcher}`;

        const response = await this.openai.chat.completions.create({
            model: "gpt-4",
            messages: [
                { role: "system", content: systemPrompt },
                { role: "user", content: userPrompt }
            ]
        });

        const content = response.choices[0].message.content || '';
        
        return {
            content,
            metadata: {
                author: "Technical Blog Writer",
                researcher: researchData.metadata.researcher,
                timestamp: new Date().toISOString(),
                status: "draft"
            }
        };
    }

    getMetadata(): AgentMetadata {
        return {
            type: "blog",
            capabilities: [
                "blog_writing",
                "technical_writing",
                "content_creation"
            ],
            topics: [
                "ai_security",
                "privacy",
                "identity_management"
            ]
        };
    }
} 