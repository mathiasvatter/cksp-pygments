import os

from pygments.lexer import RegexLexer, bygroups, include, words, default
from pygments.token import Text, Keyword, Name, String, Number, Operator, Comment, Whitespace, Punctuation

# Built-ins are copied unchanged from cksp-compiler/Builtins, so keeping them current is a copy.
BUILTIN_DIR = os.path.join(os.path.dirname(__file__), 'cksp_builtins')
SIGILS = '$%~?@!'


def _entries(filename):
	with open(os.path.join(BUILTIN_DIR, filename), 'r') as f:
		for line in f:
			line = line.split('//', 1)[0].strip()
			if line:
				yield line


def load_functions(filename):
	"""One signature per line: <name(params): type>."""
	return sorted({line.split('(', 1)[0].strip() for line in _entries(filename)} - {''})


def load_names(*filenames):
	"""Constants and variables, with sigils and <= value> parts removed."""
	names = set()
	for filename in filenames:
		for line in _entries(filename):
			name = line.split('=', 1)[0].strip().lstrip(SIGILS)
			if name:
				names.add(name)
	return sorted(names)


def load_widgets(filename):
	return sorted({line.split(' ', 1)[0].strip() for line in _entries(filename)})


def load_shorthands(variables):
	"""<ui -> hide> is short for <CONTROL_PAR_HIDE>."""
	shorthands = set()
	for var in variables:
		if var.startswith('CONTROL_PAR_'):
			shorthands.add(var[12:])
			shorthands.add(var[12:].lower())
	return sorted(shorthands)


class CKSPLexer(RegexLexer):
	name = 'CKSP'
	aliases = ['cksp', 'ksp']
	filenames = ['*.cksp', '*.ksp', '*.txt']

	ident = r'[0-9#]*[a-zA-Z_#][0-9a-zA-Z_#]*'
	# member paths like <note.pitch> stay one name
	var_name = r'[0-9#]*[a-zA-Z_#][0-9a-zA-Z_#]*(?:\.[0-9#]*[a-zA-Z_#][0-9a-zA-Z_#]*)*'
	primitive_types = r'\b(int|real|string|bool|void|any|number)\b'
	# <List<int>>, <Map<K, V[]>>: only primitives or capitalised names, so <a < b> stays a comparison
	type_args = r'(?=(?:\s*(?:int|real|string|bool|any|number|[A-Z][0-9a-zA-Z_]*)(?:\[\])?\s*[,<>]\s*)+)'

	builtin_funcs = load_functions('engine_functions.txt')
	builtin_vars = load_names('engine_variables.txt', 'engine_constants.txt', 'engine_fx_enums.txt')
	builtin_widgets = load_widgets('engine_widgets.txt')
	shorthand_vars = load_shorthands(builtin_vars)

	tokens = {
		'root': [
			include('comments'),

			# on init, on ui_control(btn), on note override
			(r'^(\s*)(on)(\s+)(' + ident + r')(?:(\s+)(override)\b)?',
			 bygroups(Whitespace, Keyword, Whitespace, Keyword.Callback, Whitespace, Keyword.Declaration)),
			(r'\bend\s+on\b', Keyword),

			# definitions that name something
			(r'\b(function|taskfunc)(\s+)', bygroups(Keyword.Declaration, Whitespace), 'funcname'),
			(r'\b(struct|namespace|family|component)(\s+)', bygroups(Keyword.Declaration, Whitespace), 'typename'),
			(r'^(\s*)(?:(static)(\s+))?(const)(\s+)(' + ident + r')\b(?!\s*:)',
			 bygroups(Whitespace, Keyword.Declaration, Whitespace, Keyword.Declaration, Whitespace, Name.Class)),
			(r'\b(list)(\s+)(' + ident + r')',
			 bygroups(Keyword.Declaration, Whitespace, Name.Variable)),
			(r'\b(end\s+(?:function|taskfunc|struct|namespace|family|component|const|list|macro))\b',
			 Keyword.Declaration),

			# preprocessor
			(r'\b(macro|define)(\s+)', bygroups(Keyword.Declaration, Whitespace), 'macroname'),
			(r'\b(iterate_macro|literate_macro|iterate_post_macro|literate_post_macro)\b', Keyword.Preproc),
			(r'(#pragma)(\s+)(' + ident + r')', bygroups(Keyword.Preproc, Whitespace, Name.Preproc)),
			(r'\b(import)\b', Keyword.Preproc, 'import'),
			(r'\b(START_INC|END_INC|SET_CONDITION|RESET_CONDITION|USE_CODE_IF_NOT|USE_CODE_IF|END_USE_CODE)\b',
			 Keyword.Preproc),
			# <on> outside a callback header: <literate_macro(...) on a, b>
			(r'\bon\b', Keyword),

			include('expr'),
		],

		'expr': [
			include('comments'),
			include('strings'),

			(r'\b(if|else|end\s+if|for|end\s+for|while|end\s+while|select|case|end\s+select|'
			 r'to|downto|step|in|default|continue|break|return)\b', Keyword.Constant),
			(r'\b(declare|local|global|pers|instpers|read|const|polyphonic|ref|static|override|'
			 r'new|delete)\b', Keyword.Declaration),
			(r'\b(true|false|nil)\b', Name.Constant),
			(r'\b(self)\b(\.)?', bygroups(Name.Builtin.Pseudo, Punctuation)),
			(r'\b(call)(\s+)(' + var_name + r')', bygroups(Keyword.Declaration, Whitespace, Name.Function)),

			# casts and type annotations
			(r'\b(as)\b', Operator.Word, 'type'),
			(r'(:)(?!=)', Punctuation, 'type'),
			# parameterized types in expressions: new List<int>(), List<T>.storage(.value)
			(r'(' + ident + r')(<)' + type_args, bygroups(Name.Class, Punctuation), 'type_arguments'),

			# numbers
			(r'(?i)0b[01]+\b', Number.Bin),
			(r'\b[01]+b\b', Number.Bin),
			(r'\b0x[0-9a-fA-F]+\b', Number.Hex),
			(r'\b[0-9][0-9a-fA-F]*h\b', Number.Hex),
			(r'(?i)\b[0-9]+\.[0-9]+(e[+-]?[0-9]+)?\b', Number.Float),
			(r'(?i)\b[0-9]+e[+-]?[0-9]+\b', Number.Float),
			(r'\b[0-9]+\b', Number.Integer),

			# operators - longest first
			(r'\?\?', Operator),
			(r'\?\.', Operator),
			(r':=', Operator),
			(r'(->)(\s*)', bygroups(Operator, Whitespace), 'shorthands'),
			(r'\.(?:and|or|xor|not)\.', Operator.Word),
			(r'\b(and|or|xor|not|mod)\b', Operator.Word),
			(r'>>>|>>|<<|\*\*|<=|>=|!=|[-+*/=<>&]', Operator),
			(r'#(?![0-9a-zA-Z_#])', Operator),
			# type sigils: $int, ~real, @string, %int_array, ?real_array, !string_array
			(r'[$%~?@!](?=[0-9a-zA-Z_#])', Keyword.Type),
			(r'\?', Operator, 'ternary'),

			include('cksp_builtins'),
			include('builtins'),
			include('widgets'),

			# calls and names
			(r'(' + var_name + r')(\s*)(\()', bygroups(Name.Function, Whitespace, Punctuation)),
			(var_name, Name.Variable),
			# member access that does not start with a name: (id as Note).pitch, arr[0].pitch, .pitch
			(r'\.(?=[0-9#]*[a-zA-Z_#])', Punctuation),
			(r'\.\.\.', Punctuation),

			(r'[()\[\],;|]', Punctuation),
			(r'\s+', Whitespace),
		],

		'comments': [
			(r'//.*?$', Comment.Single),
			(r'/\*', Comment.Multiline, 'c_comment'),
			(r'\(\*', Comment.Multiline, 'paren_comment'),
			(r'\{', Comment.Multiline, 'brace_comment'),
		],
		# /* ... */ and (* ... *) do not nest, { ... } does
		'c_comment': [
			(r'\*/', Comment.Multiline, '#pop'),
			(r'[^*]+', Comment.Multiline),
			(r'\*', Comment.Multiline),
		],
		'paren_comment': [
			(r'\*\)', Comment.Multiline, '#pop'),
			(r'[^*]+', Comment.Multiline),
			(r'\*', Comment.Multiline),
		],
		'brace_comment': [
			(r'\{', Comment.Multiline, '#push'),
			(r'\}', Comment.Multiline, '#pop'),
			(r'[^{}]+', Comment.Multiline),
		],

		'strings': [
			(r'f"', String.Interpol, 'fstring_d'),
			(r"f'", String.Interpol, 'fstring_s'),
			(r'"(\\\\|\\"|[^"])*"', String.Double),
			(r"'(\\\\|\\'|[^'])*'", String.Single),
		],
		'fstring_d': [
			(r'"', String.Interpol, '#pop'),
			(r'\\.', String.Escape),
			(r'<', Punctuation, 'fexpr'),
			(r'[^"\\<]+', String.Interpol),
		],
		'fstring_s': [
			(r"'", String.Interpol, '#pop'),
			(r'\\.', String.Escape),
			(r'<', Punctuation, 'fexpr'),
			(r"[^'\\<]+", String.Interpol),
		],
		'fexpr': [
			(r'>', Punctuation, '#pop'),
			include('expr'),
		],

		# <a ? b : c> - the <:> belongs to the ternary, not to a type annotation
		'ternary': [
			(r'\n', Whitespace, '#pop'),
			(r':(?!=)', Operator, '#pop'),
			include('expr'),
		],

		'type': [
			(r'[ \t]+', Whitespace),
			(primitive_types, Keyword.Type, ('#pop', 'type_suffix')),
			(ident, Name.Class, ('#pop', 'type_suffix')),
			default('#pop'),
		],
		'type_suffix': [
			(r'<', Punctuation, 'type_arguments'),
			(r'\[\]', Keyword.Type),
			default('#pop'),
		],
		'type_arguments': [
			(r'\s+', Whitespace),
			(primitive_types, Keyword.Type),
			(ident, Name.Class),
			(r'\[\]', Keyword.Type),
			(r',', Punctuation),
			(r'<', Punctuation, '#push'),
			(r'>', Punctuation, '#pop'),
		],

		'funcname': [
			include('magicfuncs'),
			(var_name, Name.Function, ('#pop', 'type_suffix')),
			default('#pop'),
		],
		'typename': [
			(ident, Name.Class, ('#pop', 'type_suffix')),
			default('#pop'),
		],
		'macroname': [
			(var_name, Name.Macro, '#pop'),
			default('#pop'),
		],
		'import': [
			(r'\n', Whitespace, '#pop'),
			(r'(as)(\s+)(' + ident + r')', bygroups(Keyword.Preproc, Whitespace, Name.Namespace)),
			include('expr'),
		],

		'cksp_builtins': [
			(words(('use_count', 'num_elements', 'range', 'pairs', 'search', 'search_by', 'sort', 'storage'),
				   prefix=r'\b', suffix=r'\b'), Name.Builtin),
		],
		'builtins': [
			(words(builtin_funcs, prefix=r'\b', suffix=r'\b'), Name.Builtin),
			(words(builtin_vars, prefix=r'\b', suffix=r'\b'), Name.Builtin),
		],
		'shorthands': [
			(words(shorthand_vars, prefix=r'\b', suffix=r'\b'), Name.Builtin, '#pop'),
			default('#pop'),
		],
		'widgets': [
			(r'\b(' + '|'.join(builtin_widgets) + r')(\s+)(' + var_name + r')\b',
			 bygroups(Keyword.Builtin, Whitespace, Name.Variable)),
		],
		'magicfuncs': [
			(words(('__init__', '__repr__', '__del__', '__add__', '__sub__', '__mul__', '__div__', '__mod__',
					'__eq__', '__ne__', '__lt__', '__le__', '__gt__', '__ge__', '__invert__', '__and__',
					'__or__', '__xor__', '__get__', '__set__', '__getitem__', '__setitem__'),
				   suffix=r'\b'), Name.Function.Magic, ('#pop', 'type_suffix')),
		],
	}
