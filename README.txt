This file is going to contain all the conventions I MUST use for coding over the duration of my project in accordance with the good coding practices mentioned in the PEP-8.

Imports
- all imports must be made at the start of the file 

e.g.
ALLOW: 
import x 
import y 

from x import a,b

NOT:
import x, y

- they should be in the order:
	1. Standard libraries
	2. Related 3rd party libraries 
	3. Local application libraries

- absolute imports are recommended, although relative are acceptable
	e.g.
		import dir.file
		from dir import file
		from dir.file import x

		from . import file
		from .file import x

- If the filename and class have the same name, 
	e.g. 
		from myclass import MyClass



String Quotes
- everything should be in double quotes!

 

Whitespaces 
- for parameters, everything should be right inside the brackets
	e.g.
		YES: spam(x, y)
		NO: spam ( x, y ) <-- no space between function calls 

- there should be a single space between : for conditionals:
	e.g.
		YES: if x == 4: print(x, y); x, y = y, x
		NO: if x == 4 : print( x , y) ; x , y = y , x



Comments 
- should be complete sentences

- Block comment - apply to the code that is BELOW them. Each line starts with a # and a single space. Paragraphs in block comments are separated by a line containing a single #

- Inline comment - should be used sparingly. Separated by at least 2 spaces from the code. 

- Documentation strings - https://www.python.org/dev/peps/pep-0257/. All functions and classes should have a docstring. Should all start and end with """ (triple double quotes). 

def complex(real=0.0, imag=0.0):
    """Form a complex number.

    Keyword arguments:
    real -- the real part (default 0.0)
    imag -- the imaginary part (default 0.0)
    """
    if imag == 0.0 and real == 0.0:
        return complex_zero
    ...



Naming Conventions

- all folder names in small

- All Module names should be in small and should be a single word e.g. module 
- Class names should be in camel case e.g. ClassName
- Method names should be in smalls with underscore e.g. this_is_a_method_name()
- If parameters exceeds more than 4, we move on to the next line.

- All variable names should start with a small letters e.g. name = 'hi'
- multi word variables should have an underscore separator in them e.g. first_name = 'Rajat'
- All iterables should be in smalls and should be a single word e.g. for name in x:

- All constants should be in complete capitals e.g. CONSTANT = 3.14

OTHER NAMING CONVENTIONS:

- .sql files in camelcase with capitalise first letter e.g. ThisIsAnSQLFile.sql

- database file in all caps e.g. CRICKETSCORE.db

- python file in all smalls just like module name e.g. pythonfile.py
