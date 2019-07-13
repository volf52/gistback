import sys

import click

from utils import Gistback

gist_dec = click.make_pass_decorator(Gistback)
