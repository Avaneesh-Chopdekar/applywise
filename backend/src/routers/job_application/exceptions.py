from fastapi import HTTPException, status


class JobApplicationError(HTTPException):
    """Base exception for job application-related errors"""

    pass


class InvalidIDFormatError(JobApplicationError):
    """Exception raised when an invalid ID format is provided."""

    def __init__(self, id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid ID format: {id}.",
        )


class JobApplicationNotFoundError(JobApplicationError):
    """Exception raised when a job application is not found."""

    def __init__(self, id: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Job application with id {id} not found."
                if id
                else "Job application not found."
            ),
        )


class JobApplicationAlreadyExistsError(JobApplicationError):
    """Exception raised when a job application already exists for a user."""

    def __init__(self, id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Job application with id {id} already exists.",
        )
