class WeatherAPIError(Exception):
    """Exception thrown when there is an error in the weather API"""
    pass

class LLMServiceError(Exception):
    """Exception thrown when there is an error in the LLM service."""
    pass

class LLMAPIError(Exception):
    """Exception thrown when there is an error in the LLM API."""
    pass

class MailchimpServiceError(Exception):
    """General errors on Mailchimp services."""
    pass

class MailchimpAPIError(Exception):
    """Exception thrown when there is an error in the Mailchimp API."""
    pass

class MissingEnvVarError(Exception):
    """Raised when an expected environment variable is missing."""
    pass

class ProcessingError(Exception):
    """Raised during the generation of the surf report or email."""
    pass

class FileNotFoundError(Exception):
    """Raised during the generation of the surf report or email."""
    pass