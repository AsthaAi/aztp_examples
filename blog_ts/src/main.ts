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

        // First, secure the blog agent as root
        console.log("\n1. Securing Blog Agent");
        const securedBlogAgent = await aztpClient.secureConnect(
            blogAgent,
            "BlogAgent-Hackathon1",
            {
                isGlobalIdentity: true,
            }
        );
        console.log("Blog Agent AZTP ID:", securedBlogAgent.identity.aztpId);

        // Then, secure the research agent as child of blog agent
        console.log("\n2. Securing Research Agent");
        const securedResearchAgent = await aztpClient.secureConnect(
            researchAgent,
            "ResearchAgent-Hackathon1",
            { 
                isGlobalIdentity: false,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                parentIdentity: securedBlogAgent.identity.aztpId,
                linkTo: [securedBlogAgent.identity.aztpId]
            }
        );
        console.log("Research Agent AZTP ID:", securedResearchAgent.identity.aztpId);

        // Update blog agent with research agent link
        console.log("\n3. Updating Blog Agent with Research Agent link");
        const updatedBlogAgent = await aztpClient.secureConnect(
            blogAgent,
            "BlogAgent-Hackathon1",
            {
                isGlobalIdentity: true,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                linkTo: [securedResearchAgent.identity.aztpId]
            }
        );
        console.log("Updated Blog Agent AZTP ID:", updatedBlogAgent.identity.aztpId);

        // Secure the storage service as child of blog agent
        console.log("\n4. Securing Storage Service");
        const securedStorage = await aztpClient.secureConnect(
            storage,
            "StorageService-Hackathon1",
            {
                isGlobalIdentity: false,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                parentIdentity: updatedBlogAgent.identity.aztpId,
                linkTo: [updatedBlogAgent.identity.aztpId]
            }
        );
        console.log("Storage Service AZTP ID:", securedStorage.identity.aztpId);

        // Final update to blog agent to link with storage service
        console.log("\n5. Final Update to Blog Agent with Storage Service link");
        const finalBlogAgent = await aztpClient.secureConnect(
            blogAgent,
            "BlogAgent-Hackathon1",
            {
                isGlobalIdentity: true,
                trustDomain: whiteListTrustDomains["gptarticles.xyz"],
                linkTo: [securedResearchAgent.identity.aztpId, securedStorage.identity.aztpId]
            }
        );
        console.log("Final Blog Agent AZTP ID:", finalBlogAgent.identity.aztpId);

        // Verify both identities
        console.log("\nVerifying agent identities:");
        
        const isResearchAgentValid = await aztpClient.verifyIdentity(securedResearchAgent);
        console.log("Research Agent Valid:", isResearchAgentValid);
        
        const isBlogAgentValid = await aztpClient.verifyIdentity(finalBlogAgent);
        console.log("Blog Agent Valid:", isBlogAgentValid);

        if (!isResearchAgentValid || !isBlogAgentValid) {
            throw new Error("Agent identity verification failed");
        }

        // Verify bi-directional connections
        console.log("\nVerifying bi-directional connections:");
        
        // Check Research -> Blog connection
        console.log("Checking Research -> Blog connection:");
        const researchToBlog = await aztpClient.verifyIdentityConnection(
            securedResearchAgent.identity.aztpId,
            finalBlogAgent.identity.aztpId
        );
        console.log("Research -> Blog Connection Valid:", researchToBlog);

        // Check Blog -> Research connection
        console.log("\nChecking Blog -> Research connection:");
        const blogToResearch = await aztpClient.verifyIdentityConnection(
            finalBlogAgent.identity.aztpId,
            securedResearchAgent.identity.aztpId
        );
        console.log("Blog -> Research Connection Valid:", blogToResearch);

        // Check Blog -> Storage connection
        console.log("\nChecking Blog -> Storage connection:");
        const blogToStorage = await aztpClient.verifyIdentityConnection(
            finalBlogAgent.identity.aztpId,
            securedStorage.identity.aztpId
        );
        console.log("Blog -> Storage Connection Valid:", blogToStorage);

        // Check Storage -> Blog connection
        console.log("\nChecking Storage -> Blog connection:");
        const storageToBlog = await aztpClient.verifyIdentityConnection(
            securedStorage.identity.aztpId,
            finalBlogAgent.identity.aztpId
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
            securedResearchAgent.identity.aztpId,
            finalBlogAgent.identity.aztpId
        );
        if (!researchConnectionValid) {
            throw new Error("Research -> Blog connection broken before research phase");
        }
        const researchTopic = "Zero Trust Architecture in AI Systems";
        const researchResult = await researchAgent.research(researchTopic);
        console.log("Research completed by:", securedResearchAgent.identity.aztpId);

        // 2. Blog creation phase - verify connections before blog creation
        console.log("\n2. Creating blog post");
        console.log("Verifying Blog -> Research connection before blog creation...");
        const blogConnectionValid = await aztpClient.verifyIdentityConnection(
            finalBlogAgent.identity.aztpId,
            securedResearchAgent.identity.aztpId
        );
        if (!blogConnectionValid) {
            throw new Error("Blog -> Research connection broken before blog creation phase");
        }
        const blogResult = await blogAgent.createBlog(researchResult);
        console.log("Blog created by:", finalBlogAgent.identity.aztpId);

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
