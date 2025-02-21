# prompt/output_formatting.py
import re
from typing import Optional

import markdown


class ResponseFormatter:
    """Handles post-generation formatting and sanitization of LLM responses."""

    def __init__(self, markdown_extensions: Optional[list] = None, strip_patterns: Optional[list] = None):
        """
        Args:
            markdown_extensions: List of markdown extensions to use
            strip_patterns: List of regex patterns to clean from output
        """
        self.markdown_extensions = markdown_extensions or ["fenced_code", "mdx_math"]
        self.strip_patterns = strip_patterns or [
            r"!\[.*?\]\((.*?)\)"  # Default pattern to clean markdown images
        ]

    def format(self, raw_response: str) -> str:
        """Processes raw LLM output into final formatted text."""
        cleaned_response = self._clean_response(raw_response)
        return self._convert_to_html(cleaned_response)

    def _clean_response(self, text: str) -> str:
        """Applies regex cleaning patterns to the raw response."""
        for pattern in self.strip_patterns:
            text = re.sub(pattern, r"\1", text)
        return text.strip()

    def _convert_to_html(self, text: str) -> str:
        """Converts markdown formatted text to HTML."""
        return markdown.markdown(text, extensions=self.markdown_extensions)
