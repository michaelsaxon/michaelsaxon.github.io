"""
Markdown extension for smart quotation marks.
Converts straight quotes to curly quotes when there's an even number of them on a line.
Only processes text content, not code blocks or inline code.
"""

import re
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor


class SmartQuotesPreprocessor(Preprocessor):
    """Preprocessor to convert straight quotes to smart quotes."""
    
    def __init__(self, config):
        # Use hardcoded values for now to avoid config issues
        self.double_quote_open = '&ldquo;'
        self.double_quote_close = '&rdquo;'
        self.single_quote_open = '&lsquo;'
        self.single_quote_close = '&rsquo;'
        
        # Patterns to identify code blocks and inline code
        self.code_block_pattern = re.compile(r'^```.*$', re.MULTILINE)
        self.inline_code_pattern = re.compile(r'`[^`]+`')
        
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
    
    def process_quotes_in_line(self, line):
        """Process quotes in a single line, avoiding inline code."""
        # Find all inline code spans
        inline_code_spans = []
        for match in self.inline_code_pattern.finditer(line):
            inline_code_spans.append((match.start(), match.end()))
        
        # Process double quotes
        line = self.process_quote_type(line, '"', self.double_quote_open, self.double_quote_close, inline_code_spans)
        
        # Process single quotes
        line = self.process_quote_type(line, "'", self.single_quote_open, self.single_quote_close, inline_code_spans)
        
        return line
    
    def process_quote_type(self, line, quote_char, open_char, close_char, inline_code_spans):
        """Process a specific type of quote (single or double)."""
        # Count quotes that are not in inline code
        quote_positions = []
        for i, char in enumerate(line):
            if char == quote_char:
                # Check if this quote is inside inline code
                in_inline_code = False
                for start, end in inline_code_spans:
                    if start <= i < end:
                        in_inline_code = True
                        break
                
                if not in_inline_code:
                    quote_positions.append(i)
        
        # Only process if we have an even number of quotes
        if len(quote_positions) % 2 != 0:
            return line
        
        # Convert quotes to smart quotes
        result = list(line)
        for i, pos in enumerate(quote_positions):
            if i % 2 == 0:
                # Opening quote
                result[pos] = open_char
            else:
                # Closing quote
                result[pos] = close_char
        
        return ''.join(result)
    
    def run(self, lines):
        """Process lines to convert straight quotes to smart quotes."""
        # Find code block ranges
        code_blocks = self.find_code_blocks(lines)
        
        processed_lines = []
        
        for i, line in enumerate(lines):
            # Skip if we're in a code block
            if self.is_in_code_block(i, code_blocks):
                processed_lines.append(line)
                continue
            
            # Process quotes in the line
            processed_line = self.process_quotes_in_line(line)
            processed_lines.append(processed_line)
        
        return processed_lines


class SmartQuotesExtension(Extension):
    """Markdown extension for smart quotation marks."""
    
    def __init__(self, **kwargs):
        self.config = {
            'double_quote_open': ['"', 'Opening double quote character'],
            'double_quote_close': ['"', 'Closing double quote character'],
            'single_quote_open': [''', 'Opening single quote character'],
            'single_quote_close': [''', 'Closing single quote character'],
        }
        super(SmartQuotesExtension, self).__init__(**kwargs)
    
    def extendMarkdown(self, md):
        """Register the preprocessor with the markdown instance."""
        processor = SmartQuotesPreprocessor(self.getConfigs())
        md.preprocessors.register(processor, 'smart_quotes', 20)


def makeExtension(**kwargs):
    """Return an instance of the extension."""
    return SmartQuotesExtension(**kwargs)
