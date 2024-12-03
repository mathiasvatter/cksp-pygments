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
    install_requires=[
        'Pygments>=2.0',
    ],
    author="Mathias Vatter",
    description="A Pygments Lexer for CKSP",
    url="https://github.com/mathiasvatter/cksp-pygments",
    classifiers=[
        "Programming Language :: CKSP",
        "Operating System :: OS Independent",
    ],
)