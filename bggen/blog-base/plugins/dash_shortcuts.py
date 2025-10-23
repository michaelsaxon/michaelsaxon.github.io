"""
Markdown extension for dash shortcuts.
Converts --- to em-dash (&mdash;) and -- to en-dash (&ndash;).
"""

import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class DashShortcutsPreprocessor(Preprocessor):
    """Preprocessor to convert dash shortcuts to HTML entities."""
    
    def __init__(self, config):
        # Default mappings
        self.mappings = config.get('mappings', {
            '---': '&mdash;',  # em-dash
            '--': '&ndash;',   # en-dash
        })
        
        # Create regex patterns, ordered by length (longest first)
        # to avoid partial matches
        self.patterns = []
        for shortcut, replacement in sorted(self.mappings.items(), 
                                          key=lambda x: len(x[0]), 
                                          reverse=True):
            # Escape special regex characters in the shortcut
            escaped_shortcut = re.escape(shortcut)
            self.patterns.append((re.compile(escaped_shortcut), replacement))
    
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
    
    def process_dash_shortcuts_in_line(self, line):
        """Process dash shortcuts in a single line, avoiding inline code."""
        # Find all inline code spans
        inline_code_spans = []
        inline_code_pattern = re.compile(r'`[^`]+`')
        for match in inline_code_pattern.finditer(line):
            inline_code_spans.append((match.start(), match.end()))
        
        # Process each shortcut
        processed_line = line
        for pattern, replacement in self.patterns:
            # Find all matches for this pattern
            matches = list(pattern.finditer(processed_line))
            
            # Process matches in reverse order to avoid index shifting
            for match in reversed(matches):
                # Check if this match is inside inline code
                in_inline_code = False
                for start, end in inline_code_spans:
                    if start <= match.start() < end:
                        in_inline_code = True
                        break
                
                if not in_inline_code:
                    # Replace the match
                    processed_line = processed_line[:match.start()] + replacement + processed_line[match.end():]
        
        return processed_line
    
    def run(self, lines):
        """Process lines to convert dash shortcuts."""
        # Find code block ranges
        code_blocks = self.find_code_blocks(lines)
        
        processed_lines = []
        
        for i, line in enumerate(lines):
            # Skip if we're in a code block
            if self.is_in_code_block(i, code_blocks):
                processed_lines.append(line)
                continue
            
            # Process dash shortcuts in the line
            processed_line = self.process_dash_shortcuts_in_line(line)
            processed_lines.append(processed_line)
        
        return processed_lines


class DashShortcutsExtension(Extension):
    """Markdown extension for dash shortcuts."""
    
    def __init__(self, **kwargs):
        self.config = {
            'mappings': [
                {
                    '---': '&mdash;',
                    '--': '&ndash;',
                },
                'Dictionary of shortcut to HTML entity mappings'
            ],
        }
        super(DashShortcutsExtension, self).__init__(**kwargs)
    
    def extendMarkdown(self, md):
        """Register the preprocessor with the markdown instance."""
        processor = DashShortcutsPreprocessor(self.getConfigs())
        md.preprocessors.register(processor, 'dash_shortcuts', 25)


def makeExtension(**kwargs):
    """Return an instance of the extension."""
    return DashShortcutsExtension(**kwargs)
