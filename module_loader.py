"""
Module loader for UTTR import system.
Handles finding, loading, and caching modules.
"""

import os
from module_config import get_module_search_paths, MODULE_EXTENSION


class ModuleLoader:
    """
    Loads and caches UTTR modules.
    """
    
    def __init__(self):
        self.module_cache = {}  # Cache loaded modules to prevent re-execution
        self.loading_stack = []  # Track currently loading modules for circular import detection
    
    def find_module(self, module_name, current_file_path=None):
        """
        Find a module file by name.
        
        Args:
            module_name: Name of the module (without extension)
            current_file_path: Path to the file doing the import
        
        Returns:
            Tuple of (module_path, None) on success or (None, error_info) on failure
        """
        search_paths = get_module_search_paths(current_file_path)
        searched_paths = []
        
        for search_dir in search_paths:
            module_path = os.path.join(search_dir, module_name + MODULE_EXTENSION)
            searched_paths.append(module_path)
            
            if os.path.isfile(module_path):
                return os.path.abspath(module_path), None
        
        return None, {
            'searched_paths': searched_paths,
            'message': f"Module '{module_name}' not found"
        }
    
    def load_module_source(self, module_path):
        """
        Load module source code from file.
        
        Args:
            module_path: Absolute path to the module file
        
        Returns:
            Tuple of (source_code, None) on success or (None, error_message) on failure
        """
        try:
            with open(module_path, 'r', encoding='utf-8') as f:
                return f.read(), None
        except Exception as e:
            return None, f"Failed to read module file: {str(e)}"
    
    def is_loading(self, module_path):
        """Check if a module is currently being loaded (circular import detection)."""
        return module_path in self.loading_stack
    
    def get_loading_chain(self):
        """Get the current chain of loading modules."""
        return self.loading_stack.copy()
    
    def begin_loading(self, module_path):
        """Mark a module as being loaded."""
        self.loading_stack.append(module_path)
    
    def end_loading(self, module_path):
        """Mark a module as finished loading."""
        if module_path in self.loading_stack:
            self.loading_stack.remove(module_path)
    
    def cache_module(self, module_path, module_obj):
        """Cache a loaded module."""
        self.module_cache[module_path] = module_obj
    
    def get_cached_module(self, module_path):
        """Get a cached module if it exists."""
        return self.module_cache.get(module_path)
    
    def is_cached(self, module_path):
        """Check if a module is already cached."""
        return module_path in self.module_cache


# Global module loader instance
module_loader = ModuleLoader()
