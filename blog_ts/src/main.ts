import * as dotenv from 'dotenv';
import * as fs from 'fs/promises';
import * as path from 'path';
import aztp from 'aztp-client';
import { ResearchAgent } from './agents/research-agent';
import { BlogAgent } from './agents/blog-agent';

// Load environment variables
dotenv.config();

async function main() {
    try {
        // Get API keys from environment
        const aztpApiKey = process.env.AZTP_API_KEY;
        const openaiApiKey = process.env.OPENAI_API_KEY;

        if (!aztpApiKey || !openaiApiKey) {
            throw new Error('AZTP_API_KEY and OPENAI_API_KEY are required');
        }

        // Initialize AZTP client
        const client = aztp.initialize({
            apiKey: aztpApiKey
        });

        console.log('\nInitializing agents...');
        // Create base agents
        const researchAgent = new ResearchAgent(openaiApiKey);
        const blogAgent = new BlogAgent(openaiApiKey);

        // Secure the agents with AZTP
        console.log('Securing research agent...');
        const securedResearch = await client.secureConnect(researchAgent, {
            name: "research-assistant"
        });
        
        console.log('Securing blog agent...');
        const securedBlog = await client.secureConnect(blogAgent, {
            name: "blog-writer"
        });

        // Verify agents
        console.log('\nVerifying research agent...');
        const researchValid = await client.verifyIdentity(securedResearch);
        console.log('Research Agent Identity Valid:', researchValid);
        const researchIdentity = await client.getIdentity(securedResearch);
        console.log('Research Agent Identity:', researchIdentity);

        console.log('\nVerifying blog agent...');
        const blogValid = await client.verifyIdentity(securedBlog);
        console.log('Blog Agent Identity Valid:', blogValid);
        const blogIdentity = await client.getIdentity(securedBlog);
        console.log('Blog Agent Identity:', blogIdentity);

        if (!(researchValid && blogValid)) {
            throw new Error("Agent verification failed");
        }

        // Generate blog post
        const topic = "Zero Trust Security in AI Systems";

        // Research phase
        console.log(`\nResearching topic: ${topic}`);
        const researchData = await securedResearch.research(topic);
        console.log(`Research completed: ${researchData.metadata.timestamp}`);

        // Blog writing phase
        console.log('\nGenerating blog post...');
        const blogData = await securedBlog.createBlog(researchData);
        console.log(`Blog created: ${blogData.metadata.timestamp}`);

        // Save blog post
        const outputDir = path.join(process.cwd(), 'output', 'blogs');
        await fs.mkdir(outputDir, { recursive: true });

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = path.join(outputDir, `blog_${timestamp}.md`);

        await fs.writeFile(filename, blogData.content);
        console.log(`\nBlog saved to: ${filename}`);

    } catch (error) {
        console.error('\nError:', error);
        process.exit(1);
    }
}

main(); 