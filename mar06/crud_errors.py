class PayloadError(Exception):
    pass

class PayloadMissingRequiredData(PayloadError):
    pass

class CategoryError(Exception):
    pass

class CategoryNotFoundError(CategoryError):
    pass

class InvalidCategoryDeleteError(CategoryError):
    pass

class ProductError(Exception):
    pass

class ProductNotFoundError(ProductError):
    pass

class InvalidProductDeleteError(ProductError):
    pass