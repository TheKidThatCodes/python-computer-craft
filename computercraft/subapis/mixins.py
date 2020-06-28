from typing import Tuple

from ..rproc import boolean, nil, integer, tuple3_number, tuple2_integer


class TermMixin:
    async def write(self, text: str):
        return nil(await self._send('write', text))

    async def blit(self, text: str, textColors: str, backgroundColors: str):
        return nil(await self._send('blit', text, textColors, backgroundColors))

    async def clear(self):
        return nil(await self._send('clear'))

    async def clearLine(self):
        return nil(await self._send('clearLine'))

    async def getCursorPos(self) -> Tuple[int, int]:
        return tuple2_integer(await self._send('getCursorPos'))

    async def setCursorPos(self, x: int, y: int):
        return nil(await self._send('setCursorPos', x, y))

    async def getCursorBlink(self) -> bool:
        return boolean(await self._send('getCursorBlink'))

    async def setCursorBlink(self, value: bool):
        return nil(await self._send('setCursorBlink', value))

    async def isColor(self) -> bool:
        return boolean(await self._send('isColor'))

    async def getSize(self) -> Tuple[int, int]:
        return tuple2_integer(await self._send('getSize'))

    async def scroll(self, lines: int):
        return nil(await self._send('scroll', lines))

    async def setTextColor(self, color: int):
        return nil(await self._send('setTextColor', color))

    async def getTextColor(self) -> int:
        return integer(await self._send('getTextColor'))

    async def setBackgroundColor(self, color: int):
        return nil(await self._send('setBackgroundColor', color))

    async def getBackgroundColor(self) -> int:
        return integer(await self._send('getBackgroundColor'))

    async def getPaletteColor(self, index: int) -> Tuple[float, float, float]:
        return tuple3_number(await self._send('getPaletteColor', index))

    async def setPaletteColor(self, index: int, r: float, g: float, b: float):
        return nil(await self._send('setPaletteColor', index, r, g, b))

    async def nativePaletteColor(self, index: int) -> Tuple[float, float, float]:
        return tuple3_number(await self._send('nativePaletteColor', index))
