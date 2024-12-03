from pygments import highlight
from pygments_lexers.cksp_lexer import CKSPLexer
from pygments.formatters import TerminalFormatter

code = """
#pragma output_path("Samples/resources/scripts/time-textures-2.txt")

import "Samples/resources/scripts/other-script.txt"
struct List
    declare value: string
    declare next: List

    function __init__(self, value: int, next: List)
        self.value := value
        self.next := next
    end function
end struct

define GLOBAL_VAR := 42

on init
    declare ui_slider sli_test(0,1000)
    declare x: int, y: int := 42
    declare str: string := "Hello, 'other string' World!"
    test($x)
    message(EVENT_NOTE, 3, 5, ALL_EVENTS[0])
end on

on note
    play_note(EVENT_NOTE, EVENT_VELOCITY, 0, -1)
end on

on ui_control(sli_test)
    message("Slider value: ", sli_test)
end on

function test(x: int, y: int)
    if (x > 10 and y < 20)
        return true
    else
        message("Hello, World")
        return false
    end if
end function


"""

lexer = CKSPLexer()
formatter = TerminalFormatter()
highlighted = highlight(code, lexer, formatter)

print(highlighted)