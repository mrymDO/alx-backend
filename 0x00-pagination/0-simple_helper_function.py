#!/usr/bin/env python3
"""Simple helper function"""


def index_range(page, page_size):
    """return a tuple containing start index and end index"""
    page = max(1, page)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size - 1
    return start_index, end_index    
