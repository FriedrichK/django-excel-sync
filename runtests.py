import os
import sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
ABSDIRNAME = os.path.abspath(DIRNAME)
settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(DIRNAME, 'database.db')
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'excel_sync',
        #'excel_sync.tests',
    ),
    TESTS=os.path.join(ABSDIRNAME, 'excel_sync', 'tests'),
    TEST_DATA=os.path.join(ABSDIRNAME, 'excel_sync', 'tests', 'data'),
)


from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['excel_sync'], verbosity=1)
if failures:
    sys.exit(failures)
