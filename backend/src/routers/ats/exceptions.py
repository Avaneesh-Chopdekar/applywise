from fastapi import HTTPException, status


class ATSError(HTTPException):
    """Base exception for ATS-related errors"""

    pass


class DataValidationError(ATSError):
    """Exception raised when there is a data validation error."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


class InvalidJSONFormatError(ATSError):
    """Exception raised when the provided JSON is invalid."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )


class ATSAnalysisNotFoundError(ATSError):
    """Exception raised when an ATS analysis is not found."""

    def __init__(self, id: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"ATS Analysis with id {id} not found."
                if id
                else "ATS Analysis not found."
            ),
        )
