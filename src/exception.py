import sys
import logging

logging.basicConfig(level=logging.INFO)

def error_message_details(error, error_detail: sys):
    _, _, ex_tb = error_detail.exc_info()

    file_name = ex_tb.tb_frame.f_code.co_filename
    line_number = ex_tb.tb_lineno

    error_message = (
        f"Error occurred in python script name [{file_name}] "
        f"line number [{line_number}] error message [{error}]"
    )
    return error_message


class custom_Exception(Exception):
    def __init__(self, error_message, error_detail=sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message


if __name__ == "__main__":
    try:
        a = 1 / 0
    except Exception as e:
        logging.info("Divided by Zero")  # This will print now
        raise custom_Exception(e, sys)
