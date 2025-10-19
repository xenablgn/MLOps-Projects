import traceback

class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: Exception):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message: str, error_detail: Exception):
        """Extract detailed traceback info (filename, line, message) from exception."""
        tb = error_detail.__traceback__
        file_name = tb.tb_frame.f_code.co_filename
        line_number = tb.tb_lineno
        return f"Error occurred in script: {file_name} at line {line_number} with message: {error_message}"

    def __str__(self):
        return self.error_message
