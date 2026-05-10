"""Custom exceptions for the application."""


class AppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = 500, details: dict | None = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(AppException):
    """Raised when input validation fails."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, status_code=400, details=details)


class NotFoundError(AppException):
    """Raised when a resource is not found."""

    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} not found",
            status_code=404,
            details={"resource": resource, "identifier": identifier},
        )


class UnauthorizedError(AppException):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=401)


class ForbiddenError(AppException):
    """Raised when user lacks permissions."""

    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, status_code=403)


class DuplicateError(AppException):
    """Raised when trying to create duplicate resource."""

    def __init__(self, resource: str, field: str):
        super().__init__(
            message=f"{resource} with this {field} already exists",
            status_code=409,
            details={"resource": resource, "field": field},
        )


class FileProcessingError(AppException):
    """Raised when file processing fails."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, status_code=422, details=details)


class AIAnalysisError(AppException):
    """Raised when AI analysis fails."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, status_code=500, details=details)


class DatabaseError(AppException):
    """Raised when database operation fails."""

    def __init__(self, message: str, details: dict | None = None):
        super().__init__(message, status_code=500, details=details)