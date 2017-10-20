#!/usr/bin/env python3

"""
The main driver for Telephone, a simple simulation of an information network
formed from telephone contact lists used to search for information.
"""
import sys

from .server import server


def main():
    """
    The application entry point.

    :return: An exit code.
    """
    server.port = 8521
    server.launch()


if __name__ == "__main__":
    sys.exit(main())
