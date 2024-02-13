#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022-2024 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations
from typing import Final

from .OrderedEnum import OrderedEnum


class FileSectionType(OrderedEnum):
    Dummy: Final[int]   = -4
    End: Final[int]     = -3
    Unknown: Final[int] = -2
    Invalid: Final[int] = -1

    Text: Final[int]    = 1
    Data: Final[int]    = 2
    Rodata: Final[int]  = 3
    Bss: Final[int]     = 4
    Reloc: Final[int]   = 5

    @staticmethod
    def fromId(sectionId: int) -> FileSectionType:
        try:
            return FileSectionType(sectionId)
        except:
            return FileSectionType.Invalid

    @staticmethod
    def fromStr(x: str) -> FileSectionType:
        return gNameToSectionType.get(x, FileSectionType.Invalid)

    @staticmethod
    def fromSmallStr(x: str) -> FileSectionType:
        return gSmallNameToSectionType.get(x, FileSectionType.Invalid)

    def toStr(self) -> str:
        if self == FileSectionType.Text:
            return ".text"
        if self == FileSectionType.Data:
            return ".data"
        if self == FileSectionType.Rodata:
            return ".rodata"
        if self == FileSectionType.Bss:
            return ".bss"
        if self == FileSectionType.Reloc:
            return ".reloc"
        return ""

    def toCapitalizedStr(self) -> str:
        if self == FileSectionType.Text:
            return "Text"
        if self == FileSectionType.Data:
            return "Data"
        if self == FileSectionType.Rodata:
            return "RoData"
        if self == FileSectionType.Bss:
            return "Bss"
        if self == FileSectionType.Reloc:
            return "Reloc"
        return ""

    def toSectionName(self) -> str:
        if self == FileSectionType.Text:
            return ".text"
        if self == FileSectionType.Data:
            return ".data"
        if self == FileSectionType.Rodata:
            return ".rodata"
        if self == FileSectionType.Bss:
            return ".bss"
        if self == FileSectionType.Reloc:
            return ".ovl"
        return ""

gNameToSectionType = {
    ".text":    FileSectionType.Text,
    ".data":    FileSectionType.Data,
    ".rodata":  FileSectionType.Rodata,
    ".rdata":   FileSectionType.Rodata,
    ".bss":     FileSectionType.Bss,
    ".ovl":     FileSectionType.Reloc,
    ".reloc":   FileSectionType.Reloc,
    ".end":     FileSectionType.End,
    ".dummy":   FileSectionType.Dummy,
}
gSmallNameToSectionType = {
    ".sdata":    FileSectionType.Data,
    ".srodata":  FileSectionType.Rodata,
    ".srdata":   FileSectionType.Rodata,
    ".sbss":     FileSectionType.Bss,
}


FileSections_ListBasic = [FileSectionType.Text, FileSectionType.Data, FileSectionType.Rodata, FileSectionType.Bss]
FileSections_ListAll = [FileSectionType.Text, FileSectionType.Data, FileSectionType.Rodata, FileSectionType.Bss, FileSectionType.Reloc]
