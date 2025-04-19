import fs from 'fs';
import path from 'path';
import { BlogResult } from '../types';

export class StorageService {
    private readonly blogDir: string;

    constructor() {
        this.blogDir = path.join(process.cwd(), 'blogs');
        this.ensureBlogDirectory();
    }

    private ensureBlogDirectory() {
        if (!fs.existsSync(this.blogDir)) {
            fs.mkdirSync(this.blogDir, { recursive: true });
        }
    }

    getMetadata() {
        return {
            type: "storage",
            role: "Blog Storage Service"
        };
    }

    async saveBlog(blog: BlogResult): Promise<string> {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const sanitizedTitle = this.extractTitle(blog.content).toLowerCase().replace(/[^a-z0-9]+/g, '-');
        const filename = `${timestamp}-${sanitizedTitle}.md`;
        const filepath = path.join(this.blogDir, filename);

        const blogContent = this.formatBlogContent(blog);
        await fs.promises.writeFile(filepath, blogContent, 'utf8');

        return filepath;
    }

    async listBlogs(): Promise<string[]> {
        try {
            return await fs.promises.readdir(this.blogDir);
        } catch (error) {
            console.error('Error listing blogs:', error);
            return [];
        }
    }

    private extractTitle(content: string): string {
        // Try to find a title in the content (assumes first line might be a title)
        const firstLine = content.split('\n')[0];
        const title = firstLine.replace(/^#\s*/, '').trim();
        return title || 'untitled-blog';
    }

    private formatBlogContent(blog: BlogResult): string {
        return `---
title: ${this.extractTitle(blog.content)}
author: ${blog.metadata.author}
researcher: ${blog.metadata.researcher}
date: ${blog.metadata.timestamp}
status: ${blog.metadata.status}
---

${blog.content}
`;
    }
} 