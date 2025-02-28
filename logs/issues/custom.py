from ..core.registry import register


@register(code="W1001")
class MyCustomWarning(Warning):
    pass
