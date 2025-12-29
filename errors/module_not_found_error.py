from errors.error import Error
from strings_with_arrows import string_with_arrows


class ModuleNotFoundError(Error):
    def __init__(self, pos_start, pos_end, details, search_paths=None):
        super().__init__(pos_start, pos_end, 'Module Not Found', details)
        self.search_paths = search_paths or []

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        
        if self.search_paths:
            result += '\n\nSearched in:'
            for path in self.search_paths:
                result += f'\n  - {path}'
        
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
