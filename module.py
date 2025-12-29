"""
Module representation for UTTR import system.
Represents a loaded module with its own symbol table and exports.
"""

from symbol_table import SymbolTable


class Module:
    """
    Represents a loaded UTTR module.
    
    Attributes:
        name: Module name (without extension)
        path: Absolute path to the module file
        symbol_table: Module's symbol table containing all definitions
        exports: Set of exported symbol names (None means export all)
        source: Module source code
    """
    
    def __init__(self, name, path, symbol_table=None, exports=None, source=None):
        self.name = name
        self.path = path
        self.symbol_table = symbol_table or SymbolTable()
        self.exports = exports  # None means export all, otherwise set of names
        self.source = source
    
    def get_exported_symbols(self):
        """
        Get all exported symbols from the module.
        
        Returns:
            Dictionary of {name: value} for all exported symbols
        """
        exported = {}
        
        if self.exports is None:
            # Export all symbols (except built-ins and those starting with _)
            for name, value in self.symbol_table.symbols.items():
                if not name.startswith('_'):
                    exported[name] = value
        else:
            # Export only explicitly shared symbols
            for name in self.exports:
                value = self.symbol_table.get(name)
                if value is not None:
                    exported[name] = value
        
        return exported
    
    def add_export(self, name):
        """Add a symbol name to the export list."""
        if self.exports is None:
            self.exports = set()
        self.exports.add(name)
    
    def is_exported(self, name):
        """Check if a symbol is exported."""
        if self.exports is None:
            return not name.startswith('_')
        return name in self.exports
    
    def __repr__(self):
        return f'Module({self.name}, {len(self.symbol_table.symbols)} symbols)'
