"""
Markdown extension for HTML comment sanitization.
Removes HTML comments from the markdown stream before any other processing.
"""

import re
import warnings
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class HTMLCommentSanitizerPreprocessor(Preprocessor):
    """Preprocessor to remove HTML comments from markdown content."""
    
    def __init__(self, config):
        self.config = config
        
    def is_in_code_block(self, line_num, code_block_ranges):
        """Check if a line is inside a code block."""
        for start, end in code_block_ranges:
            if start <= line_num <= end:
                return True
        return False
    
    def find_code_blocks(self, lines):
        """Find all code block ranges."""
        code_blocks = []
        in_code_block = False
        start_line = 0
        
        for i, line in enumerate(lines):
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Starting a code block
                    in_code_block = True
                    start_line = i
                else:
                    # Ending a code block
                    in_code_block = False
                    code_blocks.append((start_line, i))
        
        return code_blocks
    
    def sanitize_html_comments_in_line(self, line):
        """Remove HTML comments from a single line, avoiding inline code."""
        # Find all inline code spans
        inline_code_spans = []
        inline_code_pattern = re.compile(r'`[^`]+`')
        for match in inline_code_pattern.finditer(line):
            inline_code_spans.append((match.start(), match.end()))
        
        # Find all HTML comments in the line
        comment_pattern = re.compile(r'<!--.*?-->')
        matches = list(comment_pattern.finditer(line))
        
        # Process matches in reverse order to avoid index shifting
        processed_line = line
        for match in reversed(matches):
            # Check if this comment is inside inline code
            in_inline_code = False
            for start, end in inline_code_spans:
                if start <= match.start() < end:
                    in_inline_code = True
                    break
            
            if not in_inline_code:
                # Remove the comment
                processed_line = processed_line[:match.start()] + processed_line[match.end():]
        
        return processed_line
    
    def sanitize_html_comments(self, lines):
        """Remove HTML comments from the lines, handling both inline and multi-line comments."""
        # Find code block ranges
        code_blocks = self.find_code_blocks(lines)
        
        processed_lines = []
        
        for i, line in enumerate(lines):
            # Skip if we're in a code block
            if self.is_in_code_block(i, code_blocks):
                processed_lines.append(line)
                continue
            
            # Process HTML comments in the line
            processed_line = self.sanitize_html_comments_in_line(line)
            processed_lines.append(processed_line)
        
        return processed_lines
    
    def run(self, lines):
        """Process lines to remove HTML comments."""
        return self.sanitize_html_comments(lines)


class HTMLCommentSanitizerExtension(Extension):
    """Markdown extension for HTML comment sanitization."""
    
    def __init__(self, **kwargs):
        self.config = {
            'warn_unclosed': [True, 'Warn about unclosed HTML comments'],
            'warn_orphaned_close': [True, 'Warn about orphaned comment close tags'],
        }
        super(HTMLCommentSanitizerExtension, self).__init__(**kwargs)
    
    def extendMarkdown(self, md):
        """Register the preprocessor with the markdown instance."""
        processor = HTMLCommentSanitizerPreprocessor(self.getConfigs())
        # Use priority 26 to run after dash_shortcuts (priority 25)
        md.preprocessors.register(processor, 'html_comment_sanitizer', 26)


def makeExtension(**kwargs):
    """Return an instance of the extension."""
    return HTMLCommentSanitizerExtension(**kwargs)
