from pydantic import BaseModel


class ErrorSchema(BaseModel):
    """ Define a apresentação da mensagem de erro
    """
    message: str