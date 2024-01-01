#!/usr/bin/env python3
"""Deletion-resilient hypermedia pagination"""

import csv
import math
from typing import List, Dict


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

    def indexed_dataset(self) -> Dict[int, List]:
        """Dataset indexed by sorting position, starting at 0
        """
        if self.__indexed_dataset is None:
            dataset = self.dataset()
            truncated_dataset = dataset[:1000]
            self.__indexed_dataset = {
                i: dataset[i] for i in range(len(dataset))
            }
        return self.__indexed_dataset

    def get_hyper(self, index: int = None, page_size: int = 10) -> Dict:
        """retrieve information about a page"""
        if self.__indexed_dataset is None:
            self.indexed_dataset()

        assert isinstance(index, int) and \
                0 <= index <= len(self.__indexed_dataset)
        assert isinstance(page_size, int) and page_size > 0

        start_index = index if index is not None else 0
        end_index = start_index + page_size

        data_page = [
                self.__indexed_dataset[i]
                for i in range(start_index, end_index)
        ]

        next_index = \
            end_index if end_index < len(self.__indexed_dataset) else None

        return {
                'page_size': len(data_page),
                'page': start_index // page_size + 1,
                'data': data_page,
                'next_page': next_index // page_size + 1 if \
                        next_index is not None else None,
                'prev_page': start_index // page_size if \
                        start_index > 0 else None,
                'total_pages': math.ceil(
                    len(self.__indexed_dataset) / page_size)
        }
