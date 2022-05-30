"""Tasks for the project"""


def task_docs():
    """Build docs for project"""
    return {
        'actions': ['sphinx-build -M html ./docs/ ./docs/_build']
    }


def task_run_tests():
    """Run tests for the project"""
    yield {'actions': 'cd ./anchor_binding'}
    yield {'actions': 'python3 ./test_anchor.py'}
    yield {'actions': 'cd ..'}


def task_run_checks():
    """Run flake, pydocstring, tests"""
    yield {'actions': ['flake8 .'], 'task_dep': ['run_tests']}
    yield {'actions': ['pydocstyle .']}

def task_make_pot():
    """Make pot file"""
    return {
        'actions': ['pybabel extract -o bot.pot bot'],
        'targets': ['bot.pot']
    }

def task_make_po():
    """Update translation."""
    return {
        'actions': ['pybabel update -D bot -d po -i bot.po'],
        'task_dep': ['make_pot'],
        'targets': ['po/ru/LC_MESSAGES/bot.po']
    }

def task_compile_ru():
    """Build russian localization"""
    return {
        'actions': ['pybabel compile -D bot -d po -l ru']
    }
