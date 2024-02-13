#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022-2024 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

__version_info__: tuple[int, int, int] = (1, 20, 1)
__version__ = ".".join(map(str, __version_info__))
__author__ = "Decompollaborate"

# from . import common as common

from .common import Utils

from .common.SortedDict import SortedDict as SortedDict
from .common.GlobalConfig import GlobalConfig as GlobalConfig
from .common.GlobalConfig import InputEndian as InputEndian
from .common.GlobalConfig import Compiler as Compiler
from .common.GlobalConfig import Abi as Abi
from .common.GlobalConfig import ArchLevel as ArchLevel
from .common.GlobalConfig import InputFileType as InputFileType
from .common.FileSectionType import FileSectionType as FileSectionType
from .common.FileSectionType import FileSections_ListBasic as FileSections_ListBasic
from .common.FileSectionType import FileSections_ListAll as FileSections_ListAll
from .common.ContextSymbols import SymbolSpecialType as SymbolSpecialType
from .common.ContextSymbols import ContextSymbol as ContextSymbol
from .common.ContextSymbols import gKnownTypes as gKnownTypes
from .common.SymbolsSegment import SymbolsSegment as SymbolsSegment
from .common.Context import Context as Context
from .common.FileSplitFormat import FileSplitFormat as FileSplitFormat
from .common.FileSplitFormat import FileSplitEntry as FileSplitEntry
from .common.ElementBase import ElementBase as ElementBase
from .common.GpAccesses import GlobalOffsetTable as GlobalOffsetTable
from .common.OrderedEnum import OrderedEnum as OrderedEnum
from .common.Relocation import RelocType as RelocType
from .common.Relocation import RelocationInfo as RelocationInfo
from .common.Relocation import RelocationStaticReference as RelocationStaticReference

# from . import elf32 as elf32

from .elf32.Elf32Constants import Elf32ObjectFileType as Elf32ObjectFileType
from .elf32.Elf32Constants import Elf32HeaderFlag as Elf32HeaderFlag
from .elf32.Elf32Constants import Elf32SectionHeaderType as Elf32SectionHeaderType
from .elf32.Elf32Constants import Elf32SectionHeaderFlag as Elf32SectionHeaderFlag
from .elf32.Elf32Constants import Elf32SymbolTableType as Elf32SymbolTableType
from .elf32.Elf32Constants import Elf32SymbolTableBinding as Elf32SymbolTableBinding
from .elf32.Elf32Constants import Elf32SymbolVisibility as Elf32SymbolVisibility
from .elf32.Elf32Constants import Elf32SectionHeaderNumber as Elf32SectionHeaderNumber
from .elf32.Elf32Constants import Elf32DynamicTable as Elf32DynamicTable
from .elf32.Elf32Dyns import Elf32Dyns as Elf32Dyns
from .elf32.Elf32Dyns import Elf32DynEntry as Elf32DynEntry
from .elf32.Elf32GlobalOffsetTable import Elf32GlobalOffsetTable as Elf32GlobalOffsetTable
from .elf32.Elf32Header import Elf32Header as Elf32Header
from .elf32.Elf32RegInfo import Elf32RegInfo as Elf32RegInfo
from .elf32.Elf32SectionHeaders import Elf32SectionHeaders as Elf32SectionHeaders
from .elf32.Elf32SectionHeaders import Elf32SectionHeaderEntry as Elf32SectionHeaderEntry
from .elf32.Elf32StringTable import Elf32StringTable as Elf32StringTable
from .elf32.Elf32Syms import Elf32Syms as Elf32Syms
from .elf32.Elf32Syms import Elf32SymEntry as Elf32SymEntry
from .elf32.Elf32Rels import Elf32Rels as Elf32Rels
from .elf32.Elf32Rels import Elf32RelEntry as Elf32RelEntry

from .elf32.Elf32File import Elf32File as Elf32File

# from . import mips as mips
from .mips import sections as sections
from .mips import symbols as symbols

from .mips.FuncRodataEntry import FunctionRodataEntry as FunctionRodataEntry

from .mips import FilesHandlers as FilesHandlers

from .mips.InstructionConfig import InstructionConfig as InstructionConfig
from .mips.MipsFileBase import FileBase as FileBase
from .mips.MipsFileBase import createEmptyFile as createEmptyFile
from .mips.MipsFileSplits import FileSplits as FileSplits

# Front-end scripts
from . import frontendCommon as frontendCommon
from . import disasmdis as disasmdis
from . import rspDisasm as rspDisasm
from . import elfObjDisasm as elfObjDisasm
from . import singleFileDisasm as singleFileDisasm
