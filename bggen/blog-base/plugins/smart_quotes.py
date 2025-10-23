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
        """Process quotes in a single line, avoiding inline code and HTML tags."""
        # Find all inline code spans
        inline_code_spans = []
        for match in self.inline_code_pattern.finditer(line):
            inline_code_spans.append((match.start(), match.end()))
        
        # Find all HTML tag spans
        html_tag_spans = []
        html_tag_pattern = re.compile(r'<[^>]*>')
        for match in html_tag_pattern.finditer(line):
            html_tag_spans.append((match.start(), match.end()))
        
        
        # Combine all exclusion spans
        exclusion_spans = inline_code_spans + html_tag_spans
        
        # Process double quotes
        line = self.process_quote_type(line, '"', self.double_quote_open, self.double_quote_close, exclusion_spans)
        
        # Process single quotes
        line = self.process_quote_type(line, "'", self.single_quote_open, self.single_quote_close, exclusion_spans)
        
        return line
    
    def process_quote_type(self, line, quote_char, open_char, close_char, exclusion_spans):
        """Process a specific type of quote (single or double)."""
        # Count quotes that are not in exclusion spans and meet positioning constraints
        quote_positions = []
        for i, char in enumerate(line):
            if char == quote_char:
                # Check if this quote is inside any exclusion span (inline code or HTML tags)
                in_exclusion_span = False
                for start, end in exclusion_spans:
                    if start <= i < end:
                        in_exclusion_span = True
                        break
                
                if not in_exclusion_span:
                    # Check if this is an apostrophe in a contraction (surrounded by alphanumerics)
                    if self.is_apostrophe_in_contraction(line, i):
                        continue  # Skip this quote
                    
                    # Check positioning constraints
                    if self.is_valid_quote_position(line, i, quote_char, open_char, close_char):
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
    
    def is_apostrophe_in_contraction(self, line, pos):
        """Check if a quote is an apostrophe in a contraction (surrounded by alphanumerics)."""
        if pos == 0 or pos == len(line) - 1:
            return False
        
        # Check if surrounded by alphanumeric characters
        char_before = line[pos - 1]
        char_after = line[pos + 1]
        
        return (char_before.isalnum() and char_after.isalnum())
    
    def is_valid_quote_position(self, line, pos, quote_char, open_char, close_char):
        """Check if a quote is in a valid position for smart quote conversion."""
        # We'll determine if this is an opening or closing quote based on context
        # For now, just check that it's not in a contraction (already handled above)
        # and that it's not immediately adjacent to alphanumeric characters on both sides
        if pos > 0 and pos < len(line) - 1:
            char_before = line[pos - 1]
            char_after = line[pos + 1]
            # If surrounded by alphanumeric characters, it's likely an apostrophe
            if char_before.isalnum() and char_after.isalnum():
                return False
        
        return True
    
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
