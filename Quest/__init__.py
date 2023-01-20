__author__ = 'github.com/wardsimon'
__version__ = '0.0.1'


def is_notebook() -> bool:
    try:
        from IPython import get_ipython
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter

IS_NOTEBOOK = False

if is_notebook():
    try:
        from ipyturtle3 import ipyturtle3 as turtle
        IS_NOTEBOOK = True
    except ImportError:
        import turtle
else:
    import turtle