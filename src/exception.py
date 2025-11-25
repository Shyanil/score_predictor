import sys

def error_message_details(error , error_detail:sys):
    _,_,ex_tb = error_detail.exc_info()
    file_name = ex_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, ex_tb.line_no, str(error)
    )
    return error_message

class custom_Exception(Exception):
    def __init__(self, error_message, error_detail=sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail=error_detail)
    
    def __str__(self):
        return self.error_message