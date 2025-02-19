r"""
A secure version (using RestrictedPython) of python's stdlib codeop
"""

import __future__
import warnings
from RestrictedPython import compile_restricted as compile

_features = [getattr(__future__, fname)
             for fname in __future__.all_feature_names]

__all__ = ["compile_command", "Compile", "CommandCompiler"]

# The following flags match the values from Include/cpython/compile.h
# Caveat emptor: These flags are undocumented on purpose and depending
# on their effect outside the standard library is **unsupported**.
PyCF_DONT_IMPLY_DEDENT = 0x200          
PyCF_ALLOW_INCOMPLETE_INPUT = 0x4000

def _maybe_compile(compiler, source, filename, symbol):
    # Check for source consisting of only blank lines and comments.
    for line in source.split("\n"):
        line = line.strip()
        if line and line[0] != '#':
            break               # Leave it alone.
    else:
        if symbol != "eval":
            source = "pass"     # Replace it with a 'pass' statement

    try:
        return compiler(source, filename, symbol)
    except SyntaxError:  # Let other compile() errors propagate.
        pass

    # Catch syntax warnings after the first compile
    # to emit warnings (SyntaxWarning, DeprecationWarning) at most once.
    with warnings.catch_warnings():
        warnings.simplefilter("error")

        try:
            compiler(source + "\n", filename, symbol)
        except SyntaxError as e:
            if "incomplete input" in str(e):
                return None
            raise

def _is_syntax_error(err1, err2):
    rep1 = repr(err1)
    rep2 = repr(err2)
    if "was never closed" in rep1 and "was never closed" in rep2:
        return False
    if rep1 == rep2:
        return True
    return False

def _compile(source, filename, symbol):
    return compile(source, filename, symbol, PyCF_DONT_IMPLY_DEDENT | PyCF_ALLOW_INCOMPLETE_INPUT)

def compile_command(source, filename="<input>", symbol="single"):
    r"""Compile a command and determine whether it is incomplete.

    Arguments:

    source -- the source string; may contain \n characters
    filename -- optional filename from which source was read; default
                "<input>"
    symbol -- optional grammar start symbol; "single" (default), "exec"
              or "eval"

    Return value / exceptions raised:

    - Return a code object if the command is complete and valid
    - Return None if the command is incomplete
    - Raise SyntaxError, ValueError or OverflowError if the command is a
      syntax error (OverflowError and ValueError can be produced by
      malformed literals).
    """
    return _maybe_compile(_compile, source, filename, symbol)

class Compile:
    """Instances of this class behave much like the built-in compile
    function, but if one is used to compile text containing a future
    statement, it "remembers" and compiles all subsequent program texts
    with the statement in force."""
    def __init__(self):
        self.flags = PyCF_DONT_IMPLY_DEDENT | PyCF_ALLOW_INCOMPLETE_INPUT

    def __call__(self, source, filename, symbol):
        codeob = compile(source, filename, symbol, self.flags, True)
        for feature in _features:
            if codeob.co_flags & feature.compiler_flag:
                self.flags |= feature.compiler_flag
        return codeob

class CommandCompiler:
    """Instances of this class have __call__ methods identical in
    signature to compile_command; the difference is that if the
    instance compiles program text containing a __future__ statement,
    the instance 'remembers' and compiles all subsequent program texts
    with the statement in force."""

    def __init__(self,):
        self.compiler = Compile()

    def __call__(self, source, filename="<input>", symbol="single"):
        r"""Compile a command and determine whether it is incomplete.

        Arguments:

        source -- the source string; may contain \n characters
        filename -- optional filename from which source was read;
                    default "<input>"
        symbol -- optional grammar start symbol; "single" (default) or
                  "eval"

        Return value / exceptions raised:

        - Return a code object if the command is complete and valid
        - Return None if the command is incomplete
        - Raise SyntaxError, ValueError or OverflowError if the command is a
          syntax error (OverflowError and ValueError can be produced by
          malformed literals).
        """
        return _maybe_compile(self.compiler, source, filename, symbol)