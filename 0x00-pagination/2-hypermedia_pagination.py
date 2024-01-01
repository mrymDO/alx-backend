#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination"""

import csv
import math
from typing import List, Dict


def index_range(page, page_size):
    """return a tuple containing start index and end index"""
    page = max(1, page)
    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    return start_index, end_index


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None
        self.__indexed_dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        """retrieve a page from dataset"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        start, end = index_range(page, page_size)
        dataset = self.dataset()

        if start >= len(dataset):
            return []

        return dataset[start:min(end, len(dataset))]

    def get_hyper(self, page: int = None, page_size: int = 10) -> Dict:
        """retrieve information about a page"""
        assert isinstance(page, int) and page > 0
        assert isinstance(page_size, int) and page_size > 0

        data_page = self.get_page(page, page_size)
        start_index, end_index = index_range(page, page_size)

        next_index = start_index + page_size if \
            end_index < len(self.dataset()) else None

        return {
            'page_size': len(data_page),
            'page': page,
            'data': data_page,
            'next_index': next_index,
            'total_pages': math.ceil(len(self.dataset()) / page_size)
        }
