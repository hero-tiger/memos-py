from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin
from typing import Optional
import re


class MarkdownRenderer:
    def __init__(self):
        self.md = MarkdownIt(
            "commonmark",
            {
                "html": True,
                "linkify": True,
                "typographer": True,
                "breaks": True
            }
        )
        self.md.use(front_matter_plugin)
        self.md.use(tasklists_plugin)
    
    def render(self, markdown_text: str) -> str:
        return self.md.render(markdown_text)
    
    def extract_front_matter(self, markdown_text: str) -> dict:
        front_matter = {}
        lines = markdown_text.split('\n')
        in_front_matter = False
        front_matter_lines = []
        
        for line in lines:
            if line.strip() == '---':
                if not in_front_matter:
                    in_front_matter = True
                else:
                    break
            elif in_front_matter:
                front_matter_lines.append(line)
        
        if front_matter_lines:
            for line in front_matter_lines:
                if ':' in line:
                    key, value = line.split(':', 1)
                    front_matter[key.strip()] = value.strip()
        
        return front_matter
    
    def extract_tags(self, markdown_text: str) -> list:
        tag_pattern = r'#(\w+)'
        tags = re.findall(tag_pattern, markdown_text)
        return list(set(tags))
    
    def extract_links(self, markdown_text: str) -> list:
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = re.findall(link_pattern, markdown_text)
        return [{"text": text, "url": url} for text, url in links]
    
    def get_preview(self, markdown_text: str, max_length: int = 200) -> str:
        rendered = self.render(markdown_text)
        plain_text = re.sub(r'<[^>]+>', '', rendered)
        plain_text = ' '.join(plain_text.split())
        
        if len(plain_text) <= max_length:
            return plain_text
        
        return plain_text[:max_length] + '...'


markdown_renderer = MarkdownRenderer()
