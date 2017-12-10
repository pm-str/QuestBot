from fabric.api import local


def celery():
    """Start celery beat"""
    local('celery -A apps worker -l info')


def runserver():
    """Run django server"""
    local('./manage.py runserver')


def localtunnel():
    """Start ``localtunnel`` server

    It's done in test purposes and might be disconnected at will
    Https connection is required in order to handle webhooks properly

    """
    local('lt -h https://questbot.ml -p 8000 -s tunnel')


def isort_fix(print_msg=True):
    """Start isort to fix importing format"""
    print('Running imports fix\n')
    return local('isort -rc -y --skip .venv')


def pep8():
    """Check PEP8 errors"""

    isort_fix()
    print('Running pep8 checker\n')
    return local('flake8 --config=.flake8')
