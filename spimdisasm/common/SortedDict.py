#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

from abc import abstractmethod
import bisect
from collections.abc import Mapping, MutableMapping
from typing import Any, Generator, TypeVar, Protocol


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self, other: Any, /) -> bool: ...

KeyType = TypeVar('KeyType', bound=Comparable)
ValueType = TypeVar("ValueType")


class SortedDict(MutableMapping[KeyType, ValueType]):
    def __init__(self, other: Mapping[KeyType, ValueType]|None=None):
        self.map: dict[KeyType, ValueType] = dict()
        self.sortedKeys: list[KeyType] = list()

        if other is not None:
            for key, value in other.items():
                self.map[key] = value
                bisect.insort(self.sortedKeys, key)


    def add(self, key: KeyType, value: ValueType) -> None:
        if key not in self.map:
            # Avoid adding the key twice if it is already on the map
            bisect.insort(self.sortedKeys, key)
        self.map[key] = value

    def remove(self, key: KeyType) -> None:
        del self.map[key]
        self.sortedKeys.remove(key)


    def getKeyRight(self, key: KeyType, inclusive: bool=True) -> tuple[KeyType, ValueType]|None:
        if inclusive:
            index = bisect.bisect_right(self.sortedKeys, key)
        else:
            index = bisect.bisect_left(self.sortedKeys, key)
        if index == 0:
            return None
        key = self.sortedKeys[index - 1]
        return key, self.map[key]

    def getKeyLeft(self, key: KeyType, inclusive: bool=True) -> tuple[KeyType, ValueType]|None:
        if inclusive:
            index = bisect.bisect_left(self.sortedKeys, key)
        else:
            index = bisect.bisect_right(self.sortedKeys, key)
        if index == len(self.sortedKeys):
            return None
        key = self.sortedKeys[index]
        return key, self.map[key]


    def getRange(self, startKey: KeyType, endKey: KeyType, startInclusive: bool=True, endInclusive: bool=False) -> Generator[tuple[KeyType, ValueType], None, None]:
        if startInclusive:
            keyIndexStart = bisect.bisect_left(self.sortedKeys, startKey)
        else:
            keyIndexStart = bisect.bisect_right(self.sortedKeys, startKey)

        if endInclusive:
            keyIndexEnd = bisect.bisect_right(self.sortedKeys, endKey)
        else:
            keyIndexEnd = bisect.bisect_left(self.sortedKeys, endKey)

        for index in range(keyIndexStart, keyIndexEnd):
            key = self.sortedKeys[index]
            yield (key, self.map[key])


    def __getitem__(self, key: KeyType) -> ValueType:
        return self.map[key]

    def __setitem__(self, key: KeyType, value: ValueType) -> None:
        self.add(key, value)

    def __delitem__(self, key: KeyType) -> None:
        self.remove(key)

    def __iter__(self) -> Generator[KeyType, None, None]:
        for key in self.sortedKeys:
            yield key

    def __len__(self) -> int:
        return len(self.map)


    def __str__(self) -> str:
        ret = "SortedDict({"
        comma = False
        for key, value in self.items():
            if comma:
                ret += ", "
            ret += f"{repr(key)}: {repr(value)}"
            comma = True
        ret += "})"
        return ret

    def __repr__(self) -> str:
        return self.__str__()
