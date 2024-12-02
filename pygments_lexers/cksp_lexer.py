from pygments.lexer import RegexLexer, bygroups, include
from pygments.token import Text, Keyword, Name, String, Number, Operator, Comment, Whitespace, Punctuation
import os

class CKSPLexer(RegexLexer):
    name = 'CKSP'
    aliases = ['cksp']
    filenames = ['*.cksp', '*.ksp', '*.txt']

    var_name = r'[0-9#]*[a-zA-Z_#]+[0-9a-zA-Z_#.]*'

    def load_builtin_functions(filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        functions = []
        with open(filepath, 'r') as f:
            for line in f:
                # Entferne alles nach "//" (Kommentare)
                line = line.split('//', 1)[0].strip()
                
                # Überspringe leere Zeilen
                if not line:
                    continue
                
                # Schneide alles nach der ersten Klammer ab
                function = line.split('(', 1)[0].strip()
                
                # Füge die Funktion zur Liste hinzu (falls nicht leer)
                if function:
                    functions.append(function)
        return functions
    
    def load_builtin_variables(filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        vars = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.split('//', 1)[0].strip()
                
                # Überspringe leere Zeilen
                if not line:
                    continue
                
                types = ['$', '%', '~', '?', '@']
                var = line.strip()
                if(var[0] in types):
                    var = var[1:]
            
                vars.append(var)
        return vars
    
    def load_builtin_widgets(filename):
        filepath = os.path.join(os.path.dirname(__file__), filename)
        widgets = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.split('//', 1)[0].strip()
                
                # Überspringe leere Zeilen
                if not line:
                    continue

                widget = line.split(' ', 1)[0].strip()            
                widgets.append(widget)
        return widgets
    
    builtin_functions_file = "cksp_builtins/engine_functions.txt"
    builtin_variables_file = "cksp_builtins/engine_variables.txt"
    builtin_widgets_file = "cksp_builtins/engine_widgets.txt"
    builtin_funcs = load_builtin_functions(builtin_functions_file)
    builtin_vars = load_builtin_variables(builtin_variables_file)
    builtin_widgets = load_builtin_widgets(builtin_widgets_file)

    tokens = {
        'root': [

            # Comments
            (r'//.*$', Comment.Single),
            (r'/\*.*?\*/', Comment.Multiline),
            (r'{.*?}', Comment.Multiline),

            # Numbers
            (r'\b0x[0-9a-fA-F]+\b', Number.Hex),
            (r'\b\d+\.\d+\b', Number.Float),
            (r'\b\d+\b', Number.Integer),

            # Strings
            (r'"(\\\\|\\"|[^"])*"', String.Double),
            (r"'(\\\\|\\'|[^'])*'", String.Single),

            # Keywords
            (r'\b(continue|break|return|for|in|to|steps|end\s+for|if|else|end\s+if|'
             r'select|case|end\s+select|while|end\s+while)\b', Keyword.Constant),

            # Import
            (r'\b(import)(\s+)', bygroups(Keyword, Text)),

            # Operators
            (r'(-|\+|\/|\*|\*\*|>>|<<|=|<|>|<=|>=|\#|->)', Operator),
            (r'(and|or|not|xor|.and.|.or.|.not.|.xor.)\b', Operator.Word),

            # Constants
            (r'\b(true|false|nil)\b', Name.Constant),

            # Preprocessor Directives and Defines
            (r'\b(START_INC|END_INC|SET_CONDITION|RESET_CONDITION|#pragma|import)\b', Keyword.Preproc),

            include('builtins'),
            include('widgets'),

            # Callbacks
            (r'\bon\s+(async_complete|controller|init|listener|note|persistence_changed|'
             r'pgs_changed|poly_at|release|rpn|nrpn|ui_control|ui_update|midi_in)\b', Keyword),
            (r'\bend\s+on\b', Keyword),

            # Function Call
            (r'\b(call)\s+('+var_name+r')(\()', bygroups(Keyword.Declaration, Name.Function, Text)),
            (r'\b('+var_name+r')(\()', bygroups(Name.Function, Text)),  # Ohne "call"

            # Defines
            (r'\b(define)(\s+)', bygroups(Keyword.Declaration, Text), 'macroname'),

            # Macros
            (r'\b(macro)(\s+)', bygroups(Keyword.Declaration, Text), 'macroname'),
            (r'\bend\s+macro\b', Keyword.Declaration),

            # Functions
            (r'\b(function)(\s+)', bygroups(Keyword.Declaration, Text), 'funcname'),
            (r'\b(end\s+function)', Keyword.Declaration),

            # Structs
            (r'\b(struct)(\s+)', bygroups(Keyword.Declaration, Text), 'structname'),
            (r'\b(end\s+struct)', Keyword.Declaration),

            (r'(self)(?:(.)?)\b', bygroups(Name.Builtin.Pseudo, Text)),
            
            # Type
            (r'\b(:\s*)(int|real|string|bool|void)\b', bygroups(Text, Keyword.Type)),
            (r'(\$|\!|\%|\~|\?|\@)', Keyword.Type),

            # everything with letters after : is a type
            (r'(:\s*)('+var_name+r')', bygroups(Text, Keyword.Type)),

            # Variable declarations
            (r'\b(declare|delete|local|global|pers|instpers|const|polyphonic)\b', Keyword.Declaration),

            # Variable References
            (var_name, Name.Variable),
            (r'[,;:]', Text),
            (r'[\s+]', Whitespace),
            # Parentheses
            (r'\(', Punctuation, '#push'),  # Betritt den aktuellen State erneut
            (r'\)', Punctuation, '#pop'),  # Verlässt den aktuellen State
            (r'\[', Punctuation, '#push'),  # Betritt den aktuellen State erneut
            (r'\]', Punctuation, '#pop'),  # Verlässt den aktuellen State

        ],
        
        # Macro-specific tokens
        'macroname': [
            (var_name, Name.Macro, '#pop'),
        ],

        'structname': [
            (var_name, Name.Class, '#pop'),
        ],

        'funcname': [
            (var_name, Name.Function, '#pop'),
        ],

        'builtins': [
            (r'\b(' + '|'.join(builtin_funcs) + r')\b', Name.Builtin),
            (r'\b(' + '|'.join(builtin_vars) + r')\b', Name.Builtin),
        ],

        'widgets': [
            (r'\b(' + '|'.join(builtin_widgets) + r')(\s+)('+var_name+r')\b', 
             bygroups(Keyword.Builtin, Text, Name.Variable)),
        ]
    }
