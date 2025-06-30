#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Ensure the settings module is set to your project’s settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onego.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # The usual Django error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? "
            "Did you forget to activate your virtual environment?"
        ) from exc

    # If you want to support a `--settings` or other custom flags,
    # they can be handled here before passing into execute_from_command_line

    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
