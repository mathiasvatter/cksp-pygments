from setuptools import setup

setup(
    name='pygments-cksp',
    version='0.1',
    packages=['pygments_lexers'],
    entry_points={
        'pygments.lexers': [
            'cksp = pygments_lexers.cksp_lexer:CKSPLexer',
        ],
    },
)