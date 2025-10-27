"""
Pelican plugin to make Bsky_URI metadata accessible in Jinja templates.
"""

from pelican import signals


def add_bsky_metadata(content):
    """Add Bsky_URI metadata to content for template access."""
    if content._content is None:
        return
    
    # Check if the content has Bsky_URI metadata
    if hasattr(content, 'bsky_uri'):
        # Make it accessible in templates by ensuring it's set on the content object
        # This preserves the original value (including empty strings)
        content.bsky_uri = getattr(content, 'bsky_uri', None)
    else:
        # Set to None if not present
        setattr(content, 'bsky_uri', None)

def register():
    """Register the plugin with Pelican."""
    signals.content_object_init.connect(add_bsky_metadata)
