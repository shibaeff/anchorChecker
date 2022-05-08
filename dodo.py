def task_hello():
    """hello cmd """
    msg = 3 * "hi! "
    return {
        'actions': ['echo %s ' % msg],
        }

def task_docs():
    """build docs for project"""
    return {
        'actions': ['sphinx-build -M html ./docs/ ./docs/_build']
    }