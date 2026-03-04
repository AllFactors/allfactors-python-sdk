class ValidationError(Exception):
    """Raised when input validation fails. Use `field` to identify which parameter failed."""

    def __init__(self, message: str, field: str | None = None) -> None:
        super().__init__(message)
        self.field = field
