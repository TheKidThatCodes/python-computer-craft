from cc import LuaException, import_file, turtle, peripheral

_lib = import_file('_lib.py', __file__)
assert_raises, step = _lib.assert_raises, _lib.step


tbl = _lib.get_object_table('turtle')
assert tbl['table'] == {'native': True}
del tbl['table']
tbl['function'].setdefault('craft', True)
assert _lib.get_class_table(turtle) == tbl

flimit = turtle.getFuelLimit()
assert isinstance(flimit, int)
assert flimit > 0

flevel = turtle.getFuelLevel()
assert isinstance(flevel, int)
assert 0 <= flevel <= flimit

assert turtle.select(2) is None
assert turtle.getSelectedSlot() == 2
with assert_raises(LuaException):
    turtle.select(0)
assert turtle.select(1) is None
assert turtle.getSelectedSlot() == 1

step('Put 3 coals into slot 1')

assert turtle.getItemCount() == 3
assert turtle.getItemCount(1) == 3

assert turtle.getItemDetail() == {
    b'count': 3,  # TODO: binary output
    b'name': b'minecraft:coal',
}
assert turtle.getItemDetail(1) == {
    b'count': 3,
    b'name': b'minecraft:coal',
}

assert turtle.getItemSpace() == 61
assert turtle.getItemSpace(1) == 61

assert turtle.refuel(1) is None

assert turtle.getFuelLevel() > flevel
flevel = turtle.getFuelLevel()
assert turtle.getItemCount() == 2

assert turtle.refuel() is None

assert turtle.getFuelLevel() > flevel
assert turtle.getItemCount() == 0

with assert_raises(LuaException):
    turtle.refuel(1)
with assert_raises(LuaException):
    turtle.refuel()

step('Remove blocks in front/below/above turtle')

assert turtle.detect() is False
assert turtle.detectUp() is False
assert turtle.detectDown() is False

assert turtle.inspect() is None
assert turtle.inspectUp() is None
assert turtle.inspectDown() is None

step('Put cobblestone blocks in front/below/above turtle')

assert turtle.detect() is True
assert turtle.detectUp() is True
assert turtle.detectDown() is True

for c in [
    turtle.inspect(),
    turtle.inspectUp(),
    turtle.inspectDown()
]:
    assert isinstance(c, dict)
    assert c[b'name'] == b'minecraft:cobblestone'

assert turtle.select(1) is None
assert turtle.getItemCount() == 0
assert turtle.equipLeft() is None

assert turtle.select(2) is None
assert turtle.getItemCount() == 0
assert turtle.equipRight() is None

if (
    turtle.getItemCount(1) != 0
    or turtle.getItemCount(2) != 0
):
    step('Remove all items from slots 1 and 2')

assert turtle.select(1) is None
if turtle.getItemDetail(1) != {
    b'count': 1,
    b'name': b'minecraft:diamond_pickaxe',
}:
    step('Put fresh diamond pickaxe at slot 1')

assert turtle.equipLeft() is None

assert turtle.dig() is True
assert turtle.dig() is False
assert turtle.digUp() is True
assert turtle.digUp() is False
assert turtle.digDown() is True
assert turtle.digDown() is False

assert turtle.getItemCount() == 3

assert turtle.forward() is True
assert turtle.back() is True
assert turtle.up() is True
assert turtle.down() is True
assert turtle.turnLeft() is None
assert turtle.turnRight() is None

assert turtle.place() is True
assert turtle.place() is False
assert turtle.placeUp() is True
assert turtle.placeUp() is False
assert turtle.placeDown() is True
with assert_raises(LuaException, 'No items to place'):
    turtle.placeDown()

step('Put 3 cobblestone blocks to slot 1')

assert turtle.getItemCount(1) == 3
assert turtle.getItemCount(2) == 0

assert turtle.compare() is True
assert turtle.compareUp() is True
assert turtle.compareDown() is True

assert turtle.select(2) is None

assert turtle.compare() is False
assert turtle.compareUp() is False
assert turtle.compareDown() is False

assert turtle.select(1) is None

assert turtle.transferTo(2, 1) is True
assert turtle.getItemCount(1) == 2
assert turtle.getItemCount(2) == 1
assert turtle.compareTo(2) is True

assert turtle.transferTo(2) is True
assert turtle.getItemCount(1) == 0
assert turtle.getItemCount(2) == 3
assert turtle.compareTo(2) is False

assert turtle.select(2) is None
assert turtle.transferTo(1) is True
assert turtle.select(1) is None
assert turtle.dig() is True
assert turtle.digUp() is True
assert turtle.digDown() is True
assert turtle.getItemCount() == 6

assert turtle.drop(1) is True
assert turtle.dropUp(1) is True
assert turtle.dropDown(1) is True
assert turtle.getItemCount() == 3
assert turtle.drop() is True
assert turtle.getItemCount() == 0
assert turtle.drop() is False

step(
    'Collect dropped cobblestone\n'
    'Drop stack of sticks right in front of the turtle\n'
    'Its better to build 1-block room then throw sticks there',
)

assert turtle.suck(1) is True
assert turtle.getItemCount() == 1
assert turtle.suck() is True
assert turtle.getItemCount() == 64
assert turtle.suck() is False
assert turtle.drop() is True
assert turtle.getItemCount() == 0

step(
    'Collect dropped sticks\n'
    'Drop stack of sticks right below the turtle\n'
    'Its better to build 1-block room then throw sticks there',
)

assert turtle.suckDown(1) is True
assert turtle.getItemCount() == 1
assert turtle.suckDown() is True
assert turtle.getItemCount() == 64
assert turtle.suckDown() is False
assert turtle.dropDown() is True
assert turtle.getItemCount() == 0

step(
    'Collect dropped sticks\n'
    'Drop stack of sticks right above the turtle\n'
    'Its better to build 1-block room then throw sticks there',
)

assert turtle.suckUp(1) is True
assert turtle.getItemCount() == 1
assert turtle.suckUp() is True
assert turtle.getItemCount() == 64
assert turtle.suckUp() is False
assert turtle.dropUp() is True
assert turtle.getItemCount() == 0


def craft1():
    return turtle.craft()


def craft2():
    c = peripheral.wrap('right')
    return c.craft()


step('Put crafting table into slot 1')
assert turtle.select(1) is None
assert turtle.equipRight() is None

for craft_fn in craft1, craft2:
    step(
        'Clean inventory of turtle\n'
        'Put 8 cobblestones into slot 1',
    )

    assert turtle.select(1) is None
    assert craft_fn() is False
    for idx in [2, 3, 5, 7, 9, 10, 11]:
        assert turtle.transferTo(idx, 1)
    assert craft_fn() is True
    assert craft_fn() is False
    assert turtle.getItemDetail() == {
        b'count': 1,
        b'name': b'minecraft:furnace',
    }

print('Test finished successfully')
