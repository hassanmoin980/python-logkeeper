from typing import Optional, Type, Union


class IssueRegistry:
    """
    Registry to hold references to custom warnings, errors, or exceptions.
    This is a thread-safe, class-level registry, so everything that
    imports it gets consistent references.
    """

    _issues: dict[str, Type] = {}

    @classmethod
    def get(cls, name: str) -> Optional[Type]:
        """
        Retrieve a class from the registry by name.

        Args:
            name (str): Issue name.

        Returns:
            Optional[Type]: The registered class, or None if not found.
        """
        return cls._issues.get(name)

    @classmethod
    def register(
        cls,
        name_or_class: Union[str, Type, None] = None,
        class_obj: Optional[Type] = None,
        *,
        code: Optional[str] = None,
    ):
        """
        A versatile method to register custom exceptions or warnings.

        Usage:

        1. **Direct method call with a name and class:**
            ```python
            IssueRegistry.register("MyCustomError", MyCustomErrorClass, code="E1001")
            ```

        2. **As a decorator factory with a custom name:**
            ```python
            @IssueRegistry.register("MyCustomError", code="E1002")
            class MyCustomError(Exception):
                pass
            ```

        3. **As a decorator with no arguments (class name as key):**
            ```python
            @IssueRegistry.register
            class MyCustomError(Exception):
                pass
            ```

        4. **As a decorator with only `code` provided (uses class name as registry key):**
            ```python
            @IssueRegistry.register(code="E1003")
            class AutoNamedError(Exception):
                pass
            ```

        If `code` is provided, it will be stored as `_error_code` in the class.
        """

        # Direct method call: register("Name", SomeClass, code="E1001")
        if isinstance(name_or_class, str) and class_obj:
            cls._issues[name_or_class] = class_obj
            if code is not None:
                setattr(class_obj, "_error_code", code)
            return class_obj

        # Decorator factory: @IssueRegistry.register("Name", code="E1001")
        if isinstance(name_or_class, str) and class_obj is None:

            def decorator(decorated_class: Type) -> Type:
                cls._issues[name_or_class] = decorated_class
                if code is not None:
                    setattr(decorated_class, "_error_code", code)
                return decorated_class

            return decorator

        # Decorator with no arguments: @IssueRegistry.register
        if isinstance(name_or_class, type) and class_obj is None:
            decorated_class = name_or_class
            cls._issues[decorated_class.__name__] = decorated_class
            if code is not None and not hasattr(decorated_class, "_error_code"):
                setattr(decorated_class, "_error_code", code)
            return decorated_class

        # Decorator with only `code` provided: @IssueRegistry.register(code="E1001")
        if name_or_class is None and class_obj is None and code is not None:

            def decorator(decorated_class: Type) -> Type:
                cls._issues[decorated_class.__name__] = decorated_class
                setattr(decorated_class, "_error_code", code)
                return decorated_class

            return decorator

        # Raise an error for incorrect usage
        raise TypeError(
            "Invalid usage. Expected either:\n"
            "1) register('Name', class_obj, code='...'),\n"
            "2) @register('Name', code='...'),\n"
            "3) @register (no arguments), or\n"
            "4) @register(code='...') where class name is used."
        )

    @classmethod
    def get_all_issues(cls) -> dict[str, dict[str, Optional[Union[Type, str]]]]:
        """
        Returns a dictionary of all registered issues with their associated error codes (if any).

        Example output:
        ```python
        {
            "MyCustomError": {"class": <class '__main__.MyCustomError'>, "code": "E1001"},
            "AnotherError": {"class": <class '__main__.AnotherError'>, "code": None}
        }
        ```
        """
        return {
            name: {
                "class": issue_class,
                "code": getattr(issue_class, "_error_code", None),
            }
            for name, issue_class in cls._issues.items()
        }


# Alias for convenient decorator usage
register = IssueRegistry.register
