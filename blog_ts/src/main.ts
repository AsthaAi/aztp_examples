import aztp, { whiteListTrustDomains } from "aztp-client";
import dotenv from "dotenv";
import { ResearchAgent } from "./agents/research-agent";
import { BlogAgent } from "./agents/blog-agent";
import { StorageService } from "./services/storage";

// Load environment variables from .env file
dotenv.config();

async function main() {
    // Initialize API keys from environment
    const AZTP_API_KEY = process.env.AZTP_API_KEY;
    const OPENAI_API_KEY = process.env.OPENAI_API_KEY;

    if (!AZTP_API_KEY || !OPENAI_API_KEY) {
        throw new Error("AZTP_API_KEY and OPENAI_API_KEY must be set in .env file");
    }

    // Initialize services
    const aztpClient = aztp.initialize({
        apiKey: AZTP_API_KEY,
    });
    const storage = new StorageService();

    try {
        // Create agents
        const researchAgent = new ResearchAgent(OPENAI_API_KEY);
        const blogAgent = new BlogAgent(OPENAI_API_KEY);

        // First, secure the research agent
        console.log("\n1. Securing Research Agent");
        const securedResearchAgent = await aztpClient.secureConnect(
            researchAgent,
            "ResearchAgent-Hackathon",
            { 
                isGlobalIdentity: false,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"]
            }
        );
        console.log("Research Agent AZTP ID:", securedResearchAgent.identity.aztpId);

        // Then, secure the blog agent and link it to research agent
        console.log("\n2. Securing Blog Agent");
        const securedBlogAgent = await aztpClient.secureConnect(
            blogAgent,
            "BlogAgent-Hackathon",
            {
                isGlobalIdentity: false,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                linkTo: [securedResearchAgent.identity.aztpId],
                parentIdentity: securedResearchAgent.identity.aztpId
            }
        );
        console.log("Blog Agent AZTP ID:", securedBlogAgent.identity.aztpId);

        // Update research agent with blog agent link
        console.log("\n3. Updating Research Agent with Blog Agent link");
        const updatedResearchAgent = await aztpClient.secureConnect(
            researchAgent,
            "ResearchAgent-Hackathon",
            { 
                isGlobalIdentity: false,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                linkTo: [securedBlogAgent.identity.aztpId]
            }
        );
        console.log("Updated Research Agent AZTP ID:", updatedResearchAgent.identity.aztpId);

        // Secure the storage service
        console.log("\n4. Securing Storage Service");
        const securedStorage = await aztpClient.secureConnect(
            storage,
            "StorageService-Hackathon",
            {
                isGlobalIdentity: false,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                linkTo: [securedBlogAgent.identity.aztpId],
                parentIdentity: securedBlogAgent.identity.aztpId
            }
        );
        console.log("Storage Service AZTP ID:", securedStorage.identity.aztpId);

        // Update blog agent to link with storage service
        console.log("\n5. Updating Blog Agent with Storage Service link");
        const updatedBlogAgent = await aztpClient.secureConnect(
            blogAgent,
            "BlogAgent-Hackathon",
            {
                isGlobalIdentity: false,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                linkTo: [updatedResearchAgent.identity.aztpId, securedStorage.identity.aztpId],
                parentIdentity: updatedResearchAgent.identity.aztpId
            }
        );
        console.log("Updated Blog Agent AZTP ID:", updatedBlogAgent.identity.aztpId);

        // Verify both identities
        console.log("\nVerifying agent identities:");
        
        const isResearchAgentValid = await aztpClient.verifyIdentity(updatedResearchAgent);
        console.log("Research Agent Valid:", isResearchAgentValid);
        
        const isBlogAgentValid = await aztpClient.verifyIdentity(updatedBlogAgent);
        console.log("Blog Agent Valid:", isBlogAgentValid);

        if (!isResearchAgentValid || !isBlogAgentValid) {
            throw new Error("Agent identity verification failed");
        }

        // Verify bi-directional connections
        console.log("\nVerifying bi-directional connections:");
        
        // Check Research -> Blog connection
        console.log("Checking Research -> Blog connection:");
        const researchToBlog = await aztpClient.verifyIdentityConnection(
            updatedResearchAgent.identity.aztpId,
            updatedBlogAgent.identity.aztpId
        );
        console.log("Research -> Blog Connection Valid:", researchToBlog);

        // Check Blog -> Research connection
        console.log("\nChecking Blog -> Research connection:");
        const blogToResearch = await aztpClient.verifyIdentityConnection(
            updatedBlogAgent.identity.aztpId,
            updatedResearchAgent.identity.aztpId
        );
        console.log("Blog -> Research Connection Valid:", blogToResearch);

        // Check Blog -> Storage connection
        console.log("\nChecking Blog -> Storage connection:");
        const blogToStorage = await aztpClient.verifyIdentityConnection(
            updatedBlogAgent.identity.aztpId,
            securedStorage.identity.aztpId
        );
        console.log("Blog -> Storage Connection Valid:", blogToStorage);

        // Check Storage -> Blog connection
        console.log("\nChecking Storage -> Blog connection:");
        const storageToBlog = await aztpClient.verifyIdentityConnection(
            securedStorage.identity.aztpId,
            updatedBlogAgent.identity.aztpId
        );
        console.log("Storage -> Blog Connection Valid:", storageToBlog);

        if (!researchToBlog || !blogToResearch) {
            throw new Error("Failed to establish secure bi-directional connection between Research and Blog agents");
        }

        if (!blogToStorage || !storageToBlog) {
            throw new Error("Failed to establish secure bi-directional connection between Blog and Storage services");
        }

        // Execute the workflow with secured agents
        console.log("\nStarting secured workflow:");
        
        // 1. Research phase - verify connection before research
        console.log("\n1. Conducting research");
        console.log("Verifying Research -> Blog connection before research...");
        const researchConnectionValid = await aztpClient.verifyIdentityConnection(
            updatedResearchAgent.identity.aztpId,
            updatedBlogAgent.identity.aztpId
        );
        if (!researchConnectionValid) {
            throw new Error("Research -> Blog connection broken before research phase");
        }
        const researchTopic = "Zero Trust Architecture in AI Systems";
        const researchResult = await researchAgent.research(researchTopic);
        console.log("Research completed by:", updatedResearchAgent.identity.aztpId);

        // 2. Blog creation phase - verify connections before blog creation
        console.log("\n2. Creating blog post");
        console.log("Verifying Blog -> Research connection before blog creation...");
        const blogConnectionValid = await aztpClient.verifyIdentityConnection(
            updatedBlogAgent.identity.aztpId,
            updatedResearchAgent.identity.aztpId
        );
        if (!blogConnectionValid) {
            throw new Error("Blog -> Research connection broken before blog creation phase");
        }
        const blogResult = await blogAgent.createBlog(researchResult);
        console.log("Blog created by:", updatedBlogAgent.identity.aztpId);

        // 3. Save the blog post
        console.log("\n3. Saving blog post");
        const savedPath = await storage.saveBlog(blogResult);
        console.log("Blog saved to:", savedPath);

        // List all blogs
        console.log("\nListing available blog posts:");
        const blogs = await storage.listBlogs();
        blogs.forEach(blog => console.log(`- ${blog}`));

    } catch (error) {
        console.error("\nError:", error);
        process.exit(1);
    }
}

// Execute the main function
main().catch((error) => {
    console.error("Unhandled error:", error);
    process.exit(1);
});
