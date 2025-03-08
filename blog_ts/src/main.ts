/// <reference types="node" />
import { config } from 'dotenv';
import { mkdir, writeFile } from 'fs/promises';
import { join } from 'path';
import aztp from 'aztp-client';
import { ResearchAgent } from './agents/research-agent';
import { BlogAgent } from './agents/blog-agent';

// Load environment variables
config();

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

        // Constants
        const trustDomain = "vcagents.ai";  // Trust domain for non-global identities

        // Secure the blog agent with global identity (no trust domain needed)
        console.log('Securing blog agent...');
        const securedBlog = await client.secureConnect(blogAgent, {
            agentName: "blog-writer-1",  // Make sure this is unique. If you get an error about the agent name, change it.
                                        // Since this example is run multiple times by many people, using the same agent name will cause an error.
            isGlobalIdentity: true
        });
        console.log('Blog agent created:', securedBlog.identity.aztpId);

        // Secure the research agent as child with explicit trust domain
        console.log('Securing research agent...');
        const securedResearch = await client.secureConnect(researchAgent, {
            agentName: "research-assistant-1",  // Make sure this is unique, just like the parent agent name
            parentIdentity: securedBlog.identity.aztpId,
            trustDomain: trustDomain,
            isGlobalIdentity: false,
        });
        console.log('Research agent created:', securedResearch.identity.aztpId);

        // Verify agents using direct verification
        console.log('\nVerifying research agent...');
        const researchValid = await client.verifyIdentity(securedResearch);
        console.log('Research Agent Identity Valid:', researchValid);
        if (researchValid) {
            const researchIdentity = await client.getIdentity(securedResearch);
            console.log('Research Agent Identity:', researchIdentity);
        }

        console.log('\nVerifying blog agent...');
        const blogValid = await client.verifyIdentity(securedBlog);
        console.log('Blog Agent Identity Valid:', blogValid);
        if (blogValid) {
            const blogIdentity = await client.getIdentity(securedBlog);
            console.log('Blog Agent Identity:', blogIdentity);
        }

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
        const outputDir = join(process.cwd(), 'output', 'blogs');
        await mkdir(outputDir, { recursive: true });

        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const filename = join(outputDir, `blog_${timestamp}.md`);

        await writeFile(filename, blogData.content);
        console.log(`\nBlog saved to: ${filename}`);

    } catch (error) {
        console.error('\nError:', error);
        process.exit(1);
    }
}

main(); 