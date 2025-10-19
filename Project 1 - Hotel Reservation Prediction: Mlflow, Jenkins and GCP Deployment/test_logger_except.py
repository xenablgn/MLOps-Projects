from src.logger import get_logger
from src.custom_exception import CustomException
import sys 


logger = get_logger(__name__)

def divine_number(num: int) -> float:
    try:
        result = 100 / num
        logger.info(f"Divided 100 by {num}, result is {result}")
        return result
    except Exception as e:
        logger.error("An error occurred")
        #raise CustomException(str(e), sys) from e
        raise CustomException("Division by zero is not allowed", sys) 
    

if __name__ == "__main__": #whenever this file is run directly, this block will be executed
    try:
        logger.info("Starting division operation")
        divine_number(0)  # This will raise a division by zero exception
    except CustomException as ce:
        logger.error(str(ce))
        #logger.critical(f"Critical error: {ce}")