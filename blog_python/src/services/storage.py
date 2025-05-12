"""Storage service for managing blog posts."""

import os
from typing import Dict, Any, List
from datetime import datetime
import yaml

class StorageService:
    def __init__(self):
        """Initialize storage service with blogs directory."""
        self.blog_dir = os.path.join(os.getcwd(), 'blogs')
        self._ensure_blog_directory()

    def _ensure_blog_directory(self):
        """Ensure the blogs directory exists."""
        if not os.path.exists(self.blog_dir):
            os.makedirs(self.blog_dir, exist_ok=True)

    def get_metadata(self):
        """Get service metadata."""
        return {
            "type": "storage",
            "role": "Blog Storage Service"
        }

    def save_blog(self, blog_content: str, metadata: Dict[str, Any] = None) -> str:
        """Save blog content to a file with metadata"""
        timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S-%f') + 'Z'
        
        # Extract title from content
        title = self._extract_title(blog_content)
        sanitized_title = self._sanitize_title(title)
        
        # Create filename
        filename = f"{timestamp}-{sanitized_title}.md"
        filepath = os.path.join(self.blog_dir, filename)
        
        # Prepare metadata
        meta = {
            'title': title,
            'date': timestamp,
            'status': 'draft'
        }
        if metadata:
            meta.update(metadata)
        
        # Format content with YAML frontmatter
        content = self._format_with_frontmatter(blog_content, meta)
        
        # Save to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return filepath

    def list_blogs(self) -> List[str]:
        """List all available blog posts."""
        try:
            return os.listdir(self.blog_dir)
        except Exception as e:
            print(f"Error listing blogs: {e}")
            return []

    def _extract_title(self, content: str) -> str:
        """Extract title from blog content."""
        lines = content.split('\n')
        for line in lines:
            if line.startswith('# '):
                return line[2:].strip()
        return 'Untitled Blog'

    def _sanitize_title(self, title: str) -> str:
        """Convert title to URL-friendly slug."""
        # Convert to lowercase and replace spaces with hyphens
        slug = title.lower().replace(' ', '-')
        # Remove any characters that aren't alphanumeric or hyphens
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        # Remove multiple consecutive hyphens
        while '--' in slug:
            slug = slug.replace('--', '-')
        # Trim hyphens from start and end
        return slug.strip('-')

    def _format_with_frontmatter(self, content: str, metadata: Dict[str, Any]) -> str:
        """Format content with YAML frontmatter."""
        frontmatter = yaml.dump(metadata, default_flow_style=False)
        return f"---\n{frontmatter}---\n\n{content}" 
    
