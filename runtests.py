import os
import sys
from django.conf import settings

DIRNAME = os.path.dirname(__file__)
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
    )
)


from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)

failures = test_runner.run_tests(['excel_sync'], verbosity=1)
if failures:
    sys.exit(failures)
