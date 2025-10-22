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
        
    def sanitize_html_comments(self, lines):
        """Remove HTML comments from the lines, handling both inline and multi-line comments."""
        # Join all lines into a single string for easier processing
        content = '\n'.join(lines)
        
        # Use regex to find and replace HTML comments
        # This pattern matches <!-- ... --> including multi-line comments
        comment_pattern = r'<!--.*?-->'
        content = re.sub(comment_pattern, '', content, flags=re.DOTALL)
        
        # Check for unclosed comments (comments without -->)
        unclosed_pattern = r'<!--(?!.*?-->).*$'
        unclosed_matches = re.findall(unclosed_pattern, content, flags=re.DOTALL)
        if unclosed_matches:
            for match in unclosed_matches:
                warnings.warn(f"Unclosed HTML comment found: {match[:50]}...")
            # Remove unclosed comments
            content = re.sub(unclosed_pattern, '', content, flags=re.DOTALL)
        
        # Split back into lines
        return content.split('\n')
    
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
