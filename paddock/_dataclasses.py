from dataclasses import is_dataclass
from typing import TypeVar, Type, Callable, List, Dict, Any


__all__ = [
    "require_kwargs_on_init",
    "require_positional_args_on_init",
]

_T = TypeVar("_T")
_Self = TypeVar("_Self")
_VarArgs = List[Any]
_KWArgs = Dict[str, Any]


def _kwarg_only_init_wrapper(
        self: _Self,
        init: Callable[..., None],
        *args: _VarArgs,
        **kwargs: _KWArgs
) -> None:
    if len(args) > 0:
        raise TypeError(
            f"{type(self).__name__}.__init__(self, ...) only allows keyword "
            f"arguments. Found the following positional arguments: {args}"
        )
    init(self, **kwargs)


def _positional_arg_only_init_wrapper(
        self: _Self,
        init: Callable[..., None],
        *args: _VarArgs,
        **kwargs: _KWArgs
) -> None:
    if len(kwargs) > 0:
        raise TypeError(
            f"{type(self).__name__}.__init__(self, ...) only allows "
            f"positional arguments. Found the following keyword "
            f"arguments: {kwargs}"
        )
    init(self, *args)


def require_kwargs_on_init(cls: Type[_T]) -> Type[_T]:
    """
    Force a dataclass's init function to only work if called with
    keyword arguments.

    If parameters are not positional-only, a TypeError is thrown with a
    helpful message.

    This function may only be used on dataclasses.

    This works by wrapping the __init__ function and dynamically replacing it.
    Therefore, stacktraces for calls to the new __init__ might look a bit
    strange. Fear not though, all is well.

    Note: although this may be used as a decorator, this is not advised as
    IDEs will no longer suggest parameters in the constructor. Instead, this is
    the recommended usage::

        from dataclasses import dataclass

        @dataclass
        class Foo:
            bar: str

        require_kwargs_on_init(Foo)
    """
    if cls is None:
        raise TypeError("Cannot call with cls=None")
    if not is_dataclass(cls):
        raise TypeError(
            f"This decorator only works on dataclasses. "
            f"{cls.__name__} is not a dataclass."
        )

    original_init = cls.__init__

    def new_init(self: _Self, *args: _VarArgs, **kwargs: _KWArgs) -> None:
        _kwarg_only_init_wrapper(self, original_init, *args, **kwargs)

    # noinspection PyTypeHints
    cls.__init__ = new_init  # type: ignore

    return cls


def require_positional_args_on_init(cls: Type[_T]) -> Type[_T]:
    """
    Force a dataclass's init function to only work if called with
    positional arguments.

    If parameters are not positional-only, a TypeError is thrown with a
    helpful message.

    This function may only be used on dataclasses.

    This works by wrapping the __init__ function and dynamically replacing it.
    Therefore, stacktraces for calls to the new __init__ might look a bit
    strange. Fear not though, all is well.

    Note: although this may be used as a decorator, this is not advised as IDEs
    will no longer suggest parameters in the constructor. Instead, this is the
    recommended usage::

        from dataclasses import dataclass

        @dataclass
        class Foo:
            bar: str

        require_positional_args_on_init(Foo)
    """
    if cls is None:
        raise TypeError("Cannot call with cls=None")
    if not is_dataclass(cls):
        raise TypeError(
            f"This decorator only works on dataclasses. "
            f"{cls.__name__} is not a dataclass."
        )

    original_init = cls.__init__

    def new_init(self: _Self, *args: _VarArgs, **kwargs: _KWArgs) -> None:
        _positional_arg_only_init_wrapper(self, original_init, *args, **kwargs)

    # noinspection PyTypeHints
    cls.__init__ = new_init  # type: ignore

    return cls
