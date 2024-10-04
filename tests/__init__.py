#!/usr/bin/python3
"""
This module defines a fucntion that clears a stream
"""


def clear_stream(stream):
    """Clear stream"""
    stream.seek(0)
    stream.truncate(0)
