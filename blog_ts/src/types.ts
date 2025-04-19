export interface ResearchMetadata {
    researcher: string;
    timestamp: string;
    verification_status: string;
}

export interface BlogMetadata {
    author: string;
    researcher: string;
    timestamp: string;
    status: string;
}

export interface ResearchResult {
    topic: string;
    findings: string;
    metadata: {
        researcher: string;
        timestamp: string;
        verification_status: string;
    };
}

export interface BlogResult {
    content: string;
    metadata: {
        author: string;
        researcher: string;
        timestamp: string;
        status: string;
    };
}

export interface AztpIdentity {
    aztpId: string;
    verify: boolean;
}

export interface AgentMetadata {
    type: string;
    capabilities: string[];
    topics: string[];
} 