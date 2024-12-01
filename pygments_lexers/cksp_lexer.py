from pygments.lexer import RegexLexer, bygroups
from pygments.token import Text, Keyword, Name, String, Number, Operator, Comment, Whitespace, Punctuation

class CKSPLexer(RegexLexer):
    name = 'CKSP'
    aliases = ['cksp']
    filenames = ['*.cksp', '*.ksp', '*.txt']

    var_name = r'[0-9#]*[a-zA-Z_#]+[0-9a-zA-Z_#.]*'

    tokens = {
        'root': [

            # Comments
            (r'//.*$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'{.*?}', Comment.Multiline),

            # Parentheses
            (r'\(', Punctuation, '#push'),  # Betritt den aktuellen State erneut
            (r'\)', Punctuation, '#pop'),  # Verlässt den aktuellen State
            (r'\[', Punctuation, '#push'),  # Betritt den aktuellen State erneut
            (r'\]', Punctuation, '#pop'),  # Verlässt den aktuellen State

            # Numbers
            (r'\b0x[0-9a-fA-F]+\b', Number.Hex),
            (r'\b\d+\.\d+\b', Number.Float),
            (r'\b\d+\b', Number.Integer),

            # Strings
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),

            # Keywords
            (r'\b(continue|break|return|for|in|to|steps|end\s+for|if|else|end\s+if|'
             r'select|case|end\s+select|while|end\s+while)\b', Keyword.Control),

            # Constants
            (r'\b(true|false|nil)\b', Name.Constant),

            # Built-in Functions
            (r'\b(abs|acos|sin|cos|tan|pow|sqrt|log|exp|floor|ceil|round)\b', Name.Builtin),

            # Built-in Constants (abgekürzt)
            (r'\b(message|ALL_EVENTS|CC_NUM|EVENT_PAR|FILTER_TYPE_AR_BP2|'
             r'LOOP_PAR_START|NI_WAVEFORM_TYPE)\b', Name.Builtin),

            # Operators
            (r'(-|\+|\/|\*|\*\*|>>|<<|=|<|>|<=|>=|\#)', Operator),

            # Preprocessor Directives and Defines
            (r'\b(START_INC|END_INC|SET_CONDITION|#pragma|define|import)\b', Keyword.Preproc),

            # Callbacks
            (r'\bon\s+(async_complete|controller|init|listener|note|persistence_changed|'
             r'pgs_changed|poly_at|release|rpn|nrpn|ui_control|ui_update|midi_in)\b', Keyword),
            (r'\bend\s+on\b', Keyword),

            # Macros
            (r'\bmacro\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', Keyword, 'macro'),
            (r'\bend\s+macro\b', Keyword),

            # (r'(function)(\s+)',
            # bygroups(Keyword.Declaration, Text), 'funcname'),

            # Structs and Functions
            (r'\b(struct|end\s+struct|function|end\s+function)\b', Keyword),
            # (r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', Name.Function),

            # Variable with Type
            (r'('+var_name+r')(\s*:\s*)(int|float|string)',
                bygroups(Name.Variable, Text, Keyword.Type)),

            # Variable declarations
            (r'\b(declare|delete|local|global|pers|instpers|const)\b', Keyword.Declaration),

            # Variable References
            (var_name, Name.Variable),
            (r'[,;:]', Text),
            (r'[\s+]', Whitespace)
        ],
        
        # Macro-specific tokens
        'macro': [
            (r'\)', Text, '#pop'),  # End of macro definition
            (r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', Name.Variable),  # Macro parameters
            (r'\s+', Text)  # Allow whitespace
        ]
    }
