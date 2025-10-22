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
    
    def run(self, lines):
        """Process lines to convert dash shortcuts."""
        processed_lines = []
        
        for line in lines:
            processed_line = line
            for pattern, replacement in self.patterns:
                processed_line = pattern.sub(replacement, processed_line)
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
