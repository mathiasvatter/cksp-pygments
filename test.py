from pygments import highlight
from pygments_lexers.cksp_lexer import CKSPLexer
from pygments.formatters import TerminalFormatter

code = """
on init
    declare x: int, y: int := 42
    declare str: string := "Hello, World!"
    test(x)
end on

function test(x: int, y: int)
    if (x > 10 and y < 20)
        return true
    else
        return false
    end if
end function
"""

lexer = CKSPLexer()
formatter = TerminalFormatter()
highlighted = highlight(code, lexer, formatter)

print(highlighted)