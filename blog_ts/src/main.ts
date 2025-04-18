import aztp, { whiteListTrustDomains } from "aztp-client";

async function main() {
  // Initialize the client with API key from environment
  const API_KEY = process.env.AZTP_API_KEY;
  if (!API_KEY) {
    throw new Error("AZTP_API_KEY is not set");
  }

  const client = aztp.initialize({
    apiKey: API_KEY,
  });

  // Create base agents
  const crewAgent = {};
  const otherAgentA = {};
  const otherAgentB = {};
  const agentName = "MyAgent-01";
  const otherAgentNameA = "MyAgent-01-A";
  const otherAgentNameB = "MyAgent-01-B";

  try {
    // Initialize AZTP client with all configuration
    const aztpClient = aztp.initialize({
      apiKey: API_KEY,
    });

    // Check available trusted domains
    console.log("Available trusted domains:", whiteListTrustDomains);

    // Issue identity
    // Example 1: Identity will be issued with global identity
    console.log("1. Issuing identity for agent:", agentName);
    const securedAgent = await aztpClient.secureConnect(crewAgent, agentName, {
      isGlobalIdentity: true,
    });
    console.log("AZTP ID:", securedAgent);

    // Example 2: Issue identity with linked identity
    console.log("2. Issuing identity with linked identity:", otherAgentNameA);
    const otherSecuredAgentA = await aztpClient.secureConnect(
      otherAgentA,
      otherAgentNameA,
      {
        linkTo: [securedAgent.identity.aztpId],
        isGlobalIdentity: false,
      }
    );
    console.log("Other AZTP ID with linked identity:", otherSecuredAgentA);

    // Example 3: Issue identity with trust domain, linked identity and parent identity
    // Identity will be issued with trust domain, linked identity and parent identity
    // Trust domain must be verified in astha.ai
    console.log(
      "3. Issuing identity with trust domain and linked identity:",
      otherAgentNameB
    );
    const otherSecuredAgentWithTrustDomain = await aztpClient.secureConnect(
      otherAgentB,
      otherAgentNameB,
      {
        trustDomain: whiteListTrustDomains["gptarticles.xyz"],
        linkTo: [otherSecuredAgentA.identity.aztpId],
        parentIdentity: securedAgent.identity.aztpId,
        isGlobalIdentity: false,
      }
    );
    console.log(
      "Other AZTP ID with trust domain and linked identity:",
      otherSecuredAgentWithTrustDomain
    );

    // Verify identity
    console.log("\nVerify identity", "AgentName:", agentName);
    const isValid = await aztpClient.verifyIdentity(securedAgent);
    console.log("Identity Valid:", isValid);

    // Verify identity connection
    console.log(
      "\nVerify identity connection from agent",
      agentName,
      "to agent",
      otherAgentNameB
    );
    const isValidConnection = await aztpClient.verifyIdentityConnection(
      securedAgent.identity.aztpId,
      otherSecuredAgentWithTrustDomain.identity.aztpId
    );
    console.log("Valid Connection:", isValidConnection);

    // Get existing identity
    console.log("\nGet identity for", "AgentName:", agentName);
    const existingIdentity = await aztpClient.getIdentity(securedAgent);
    console.log("Get Identity:", existingIdentity);

    // Discoverable identities
    // Discoverable identities are identities that are discoverable by other agents
    console.log("\nDiscoverable identities");
    const discoveredIdentities = await aztpClient.discoverIdentity();
    console.log("Discovered Identities:", discoveredIdentities);

    // Discover identity with trust domain
    // Discoverable identities with trust domain are identities that are discoverable by other agents
    // Trust domain must be verified in astha.ai
    console.log("\nDiscoverable identities with trust domain");
    const discoveredIdentitiesWithTrustDomain =
      await aztpClient.discoverIdentity({
        trustDomain: whiteListTrustDomains["gptarticles.xyz"],
        requestorIdentity: securedAgent.identity.aztpId,
      });
    console.log(
      "Discovered Identities with Trust Domain:",
      discoveredIdentitiesWithTrustDomain
    );
  } catch (error) {
    console.error("Error:", error);
  }
}
