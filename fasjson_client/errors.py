from bravado.exception import HTTPError


class BaseError(Exception):
    """
    Base exception class that is in inherited from all other exceptions.
    """

    def __init__(self, message, code, data=None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.data = data

    def __repr__(self):
        """
        String representation of the class for debugging purposes,
        returned when using the repr function.
        """
        return (
            f"<{self.__class__.__name__} code={self.code} "
            f"message={self.message} data={self.data}>"
        )

    def __str__(self):
        """
        value returned by the str() function.
        """
        return self.message


class ClientError(BaseError):
    """
    Client exception whcih is raised in case of openapi spec and client setup issues.
    """


class APIError(BaseError):
    """
    Error returned by the API
    """

    @classmethod
    def from_bravado_error(cls, error):
        if not isinstance(error, HTTPError):
            raise ValueError(
                "{!r} is not an instance of bravado.exception.HTTPError".format(error)
            )
        try:
            api_message = error.response.json()["message"]
        except (KeyError, ValueError):
            api_message = str(error)
        try:
            body = error.response.json()
        except ValueError:
            body = error.response.text
        return cls(
            api_message,
            error.status_code,
            data={
                "response": error.response,
                "body": body,
                "swagger_result": error.swagger_result,
            },
        )
