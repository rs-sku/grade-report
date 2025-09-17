import os
from _collections_abc import Iterable
from argparse import Action


class ValidatePathExists(Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if isinstance(values, Iterable):
            for value in values:
                if not os.path.exists(value):
                    parser.error(f"Path '{value}' does not exist")
        else:
            if not os.path.exists(values):
                parser.error(f"Path '{value}' does not exist")
        setattr(namespace, self.dest, values)
