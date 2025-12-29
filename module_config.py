"""
Module configuration for UTTR import system.
Defines module search paths and resolution rules.
"""

import os

# Get the directory of this file (the UTTR root directory)
UTTR_ROOT = os.path.dirname(os.path.abspath(__file__))

# Standard library directory
STDLIB_DIR = os.path.join(UTTR_ROOT, 'stdlib')

# Module file extension
MODULE_EXTENSION = '.uttr'

def get_module_search_paths(current_file_path=None):
    """
    Get list of paths to search for modules, in order of precedence.
    
    Args:
        current_file_path: Path to the file doing the import (for relative imports)
    
    Returns:
        List of directory paths to search
    """
    search_paths = []
    
    # 1. Current directory of the importing file (for relative imports)
    if current_file_path:
        current_dir = os.path.dirname(os.path.abspath(current_file_path))
        search_paths.append(current_dir)
    
    # 2. Current working directory
    search_paths.append(os.getcwd())
    
    # 3. Standard library directory
    search_paths.append(STDLIB_DIR)
    
    return search_paths
