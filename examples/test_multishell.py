import random

from cc import import_file, multishell

_lib = import_file('_lib.py', __file__)


assert _lib.get_class_table(multishell) == _lib.get_object_table('multishell')

_lib.step('Close all additional shells')

assert multishell.getCount() == 1
assert multishell.getCurrent() == 1
assert multishell.getFocus() == 1
assert isinstance(multishell.getTitle(1), str)

title = f'new title {random.randint(1, 1000000)}'
assert multishell.setTitle(1, title) is None
assert multishell.getTitle(1) == title

assert multishell.setFocus(1) is True
assert multishell.setFocus(0) is False
assert multishell.setFocus(2) is False

assert multishell.getTitle(2) is None

assert multishell.launch({}, 'rom/programs/fun/hello.lua') == 2
assert isinstance(multishell.getTitle(2), str)

print('Test finished successfully')
