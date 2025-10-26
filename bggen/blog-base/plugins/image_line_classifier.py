"""
Pelican plugin to add 'image_line' class to paragraphs containing only a single image.
"""

import re
from pelican import signals


def add_image_line_class(content):
    """Add 'image_line' class to paragraphs containing only a single image."""
    if content._content is None:
        return
    
    # Pattern to match <p><img .../></p> exactly
    # This matches a paragraph that contains only whitespace and a single img tag
    pattern = re.compile(r'<p>\s*<img[^>]*/>\s*</p>', re.IGNORECASE)
    
    # Replace with <p class="image_line"><img .../></p>
    def replace_func(match):
        # Extract the img tag from the match
        img_tag = re.search(r'<img[^>]*/>', match.group(0), re.IGNORECASE)
        if img_tag:
            return f'<p class="image-line">{img_tag.group(0)}</p>'
        return match.group(0)
    
    # Apply the replacement
    content._content = pattern.sub(replace_func, content._content)


def register():
    """Register the plugin with Pelican."""
    signals.content_object_init.connect(add_image_line_class)
