from pygments.lexer import RegexLexer
from pygments.token import Text, Keyword, Name, String, Number, Operator

class CKSPLexer(RegexLexer):
    name = 'CKSP'
    aliases = ['cksp']
    filenames = ['*.cksp']

    tokens = {
        'root': [
            (r'\b(declare|function|struct|return|if|else|for|while)\b', Keyword),
            (r'\b(ndarray|int|float|string|bool)\b', Keyword.Type),
            (r'\b(true|false|null)\b', Keyword.Constant),
            (r'[a-zA-Z_][a-zA-Z0-9_]*', Name),
            (r'"(\\\\|\\"|[^"])*"', String),
            (r'\d+\.\d*|\.\d+|\d+', Number),
            (r'[+\-*/=<>!&|]', Operator),
            (r'\s+', Text),
        ],
    }