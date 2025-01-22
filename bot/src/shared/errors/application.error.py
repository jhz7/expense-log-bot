class ApplicationError(Exception):
    def __init__(self, code: str, message: str, attributes: dict):
        self.code = code
        self.message = message
        self.attributes = attributes
        super().__init__(f"{self.code}: {self.message}, attributes: {self.attributes}")


def NotFoundError(resource: str, attributes: dict):
    attributes["resource"] = resource
    return ApplicationError(
        "RESOURCE_NOT_FOUND", f"The resource {resource} was not found", attributes
    )
