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
        
        # Create a content string with placeholders for both fenced code blocks and inline code
        content = '\n'.join(lines)
        
        # Replace fenced code blocks with placeholders to protect them
        code_block_placeholders = []
        for i, (start, end) in enumerate(code_blocks):
            placeholder = f"__CODE_BLOCK_PLACEHOLDER_{i}__"
            code_block_placeholders.append((placeholder, lines[start:end+1]))
            
            # Replace the code block with placeholder
            code_block_content = '\n'.join(lines[start:end+1])
            content = content.replace(code_block_content, placeholder)
        
        # Replace inline code with placeholders to protect them
        inline_code_placeholders = []
        inline_code_pattern = re.compile(r'`[^`]+`')
        for i, match in enumerate(inline_code_pattern.finditer(content)):
            placeholder = f"__INLINE_CODE_PLACEHOLDER_{i}__"
            inline_code_placeholders.append((placeholder, match.group()))
            content = content.replace(match.group(), placeholder)
        
        # Now remove multi-line comments from the content (outside code blocks)
        comment_pattern_multiline = re.compile(r'<!--.*?-->', re.DOTALL)
        content = re.sub(comment_pattern_multiline, '', content)
        
        # Restore inline code first
        for placeholder, code_content in inline_code_placeholders:
            content = content.replace(placeholder, code_content)
        
        # Restore fenced code blocks
        for placeholder, code_block_lines in code_block_placeholders:
            code_block_content = '\n'.join(code_block_lines)
            content = content.replace(placeholder, code_block_content)
        
        # Split back into lines for line-by-line processing
        lines_after_multiline_removal = content.split('\n')
        
        processed_lines = []
        
        for i, line in enumerate(lines_after_multiline_removal):
            # Skip if we're in a code block (use original line numbers)
            if self.is_in_code_block(i, code_blocks):
                processed_lines.append(line)
                continue
            
            # Process any remaining inline HTML comments in the line
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
