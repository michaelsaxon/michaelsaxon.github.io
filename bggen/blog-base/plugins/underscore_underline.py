"""
Markdown extension for underscore-based underline formatting.
Converts _ _ to <u> tags instead of emphasis.
"""

import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class UnderscoreUnderlinePreprocessor(Preprocessor):
    """Preprocessor to convert underscore formatting to HTML underline tags."""
    
    def __init__(self, config):
        self.config = config
        # Pattern to match _ _ content _ _ (underscore, space, content, space, underscore)
        # Use a simpler approach: match any content between _ _ and _ _
        self.underscore_pattern = re.compile(r'_ _ ([^_]+?) _ _')
        
    def run(self, lines):
        """Process lines to convert underscore formatting to HTML underline tags."""
        processed_lines = []
        
        for line in lines:
            # Process the line to convert underscore formatting
            processed_line = self.process_line(line)
            processed_lines.append(processed_line)
        
        return processed_lines
    
    def process_line(self, line):
        """Process a single line to convert underscore formatting."""
        # Use a simple regex that matches the pattern _ _ content _ _
        # The key is to use a non-greedy match that stops at the first _ _ pattern
        pattern = re.compile(r'_ _ ([^_]+?) _ _')
        
        # Keep processing until no more matches are found
        while True:
            match = pattern.search(line)
            if not match:
                break
            
            content = match.group(1).strip()
            replacement = f'<u>{content}</u>'
            line = line[:match.start()] + replacement + line[match.end():]
        
        return line


class UnderscoreUnderlineExtension(Extension):
    """Markdown extension for underscore-based underline formatting."""
    
    def __init__(self, **kwargs):
        self.config = {
            'enabled': [True, 'Enable underscore underline processing'],
        }
        super(UnderscoreUnderlineExtension, self).__init__(**kwargs)
    
    def extendMarkdown(self, md):
        """Register the preprocessor with the markdown instance."""
        processor = UnderscoreUnderlinePreprocessor(self.getConfigs())
        # Use priority 15 to run before other processors
        md.preprocessors.register(processor, 'underscore_underline', 15)


def makeExtension(**kwargs):
    """Return an instance of the extension."""
    return UnderscoreUnderlineExtension(**kwargs)
