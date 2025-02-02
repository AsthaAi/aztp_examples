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
    metadata: ResearchMetadata;
}

export interface BlogResult {
    content: string;
    metadata: BlogMetadata;
} 