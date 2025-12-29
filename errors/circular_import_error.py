from errors.error import Error
from strings_with_arrows import string_with_arrows


class CircularImportError(Error):
    def __init__(self, pos_start, pos_end, details, import_chain=None):
        super().__init__(pos_start, pos_end, 'Circular Import', details)
        self.import_chain = import_chain or []

    def as_string(self):
        result = f'{self.error_name}: {self.details}\n'
        result += f'File {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        
        if self.import_chain:
            result += '\n\nImport chain:'
            for i, module in enumerate(self.import_chain):
                result += f'\n  {i+1}. {module}'
        
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
