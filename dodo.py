"""Tasks for the project"""


def task_hello():
    """Hello cmd"""
    msg = 3 * "hi! "
    return {
        'actions': ['echo %s ' % msg],
    }


def task_docs():
    """Build docs for project"""
    return {
        'actions': ['sphinx-build -M html ./docs/ ./docs/_build']
    }


def task_run_tests():
    """Run tests for the project"""
    return {
        'actions': ['cd ./anchor_binding && python3 ./test_anchor.py && cd ..']
    }


def task_run_checks():
    """Run flake, pydocstring, tests"""
    return {
        'actions': ['flake8 .', 'pydocstyle .', 'doit run_tests']
    }


def task_compile_ru():
    """Build russian localization"""
    return {
        'actions': ['pybabel compile -D bot -d po -l ru']
    }
