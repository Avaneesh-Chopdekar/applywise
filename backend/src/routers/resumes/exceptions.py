from fastapi import HTTPException, status


class ResumeError(HTTPException):
    """Base exception for resume-related errors"""

    pass


class ResumeAlreadyExistsError(ResumeError):
    """Exception raised when a resume already exists for a user."""

    def __init__(self, id: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resume with id {id} already exists.",
        )


class ResumeNotFoundError(ResumeError):
    """Exception raised when a resume is not found."""

    def __init__(self, id: str | None = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Resume with id {id} not found." if id else "Resume not found.",
        )


class ResumeUpdateError(ResumeError):
    """Exception raised when there is an error updating a resume."""

    def __init__(self, id: str | None = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=(
                f"Failed to update resume with id {id}."
                if id
                else "Failed to update resume."
            ),
        )
