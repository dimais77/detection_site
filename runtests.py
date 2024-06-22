import os
import sys
import django
from django.conf import settings

def run_tests():
    # Добавьте корневой каталог проекта в sys.path
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

    os.environ['DJANGO_SETTINGS_MODULE'] = 'detection_site.settings'
    django.setup()

    from django.test.utils import get_runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['object_detection.tests'])
    sys.exit(bool(failures))

if __name__ == "__main__":
    run_tests()
