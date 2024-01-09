class DJFileValidatorError(Exception):
    pass


class InvalidManifestError(DJFileValidatorError):
    pass


class InvalidRuleError(DJFileValidatorError):
    pass


class InvalidQueryError(DJFileValidatorError):
    pass
