#!/usr/bin/env python3

# SPDX-FileCopyrightText: © 2022 Decompollaborate
# SPDX-License-Identifier: MIT

from __future__ import annotations

from ... import common

from ..MipsFileBase import FileBase

class SectionBase(FileBase):
    def checkWordIsASymbolReference(self, word: int) -> bool:
        if not self.context.totalVramRange.isInRange(word):
            return False
        if self.context.isAddressBanned(word):
            return False

        contextSym = self.getSymbol(word, tryPlusOffset=True, checkUpperLimit=False)
        if contextSym is not None:
            symType = contextSym.getTypeSpecial()
            if symType in {common.SymbolSpecialType.function, common.SymbolSpecialType.branchlabel, common.SymbolSpecialType.jumptablelabel}:
                # Avoid generating extra symbols in the middle of functions
                return False

            if word < contextSym.vram + contextSym.getSize():
                # Avoid generating symbols in the middle of other symbols with known sizes
                return False

        self.addPointerInDataReference(word)
        return True

    def processStaticRelocs(self) -> None:
        for i in range(self.sizew):
            word = self.words[i]
            vrom = self.getVromOffset(i*4)
            relocInfo = self.context.globalRelocationOverrides.get(vrom)
            if relocInfo is None or relocInfo.staticReference is None:
                continue

            relocVram = relocInfo.staticReference.sectionVram + word
            sectionType = relocInfo.staticReference.sectionType
            if self.sectionType == common.FileSectionType.Rodata and sectionType == common.FileSectionType.Text:
                contextSym = self.addJumpTableLabel(relocVram, isAutogenerated=True)
            else:
                contextSym = self.addSymbol(relocVram, sectionType=sectionType, isAutogenerated=True)
            contextSym._isStatic = True

    def _stringGuesser(self, contextSym: common.ContextSymbol, localOffset: int) -> bool:
        if contextSym.isMaybeString or contextSym.isString():
            return True

        if self.sectionType == common.FileSectionType.Rodata:
            stringGuesserLevel = common.GlobalConfig.RODATA_STRING_GUESSER_LEVEL
        else:
            stringGuesserLevel = common.GlobalConfig.DATA_STRING_GUESSER_LEVEL

        if stringGuesserLevel < 1:
            return False

        if contextSym.referenceCounter > 1:
            if stringGuesserLevel < 2:
                return False

        # This would mean the string is an empty string, which is not very likely
        if self.words[localOffset//4] == 0:
            if stringGuesserLevel < 3:
                return False

        if contextSym.hasOnlyAutodetectedType():
            if stringGuesserLevel < 4:
                return False

        currentVram = self.getVramOffset(localOffset)
        currentVrom = self.getVromOffset(localOffset)
        _, rawStringSize = common.Utils.decodeBytesToStrings(self.bytes, localOffset, self.stringEncoding)
        if rawStringSize < 0:
            # String can't be decoded
            return False

        # Check if there is already another symbol after the current one and before the end of the string,
        # in which case we say this symbol should not be a string
        otherSym = self.getSymbol(currentVram + rawStringSize, vromAddress=currentVrom + rawStringSize, checkUpperLimit=False, checkGlobalSegment=False)
        if otherSym != contextSym:
            return False

        return True

    def _pascalStringGuesser(self, contextSym: common.ContextSymbol, localOffset: int) -> bool:
        if contextSym.isMaybePascalString or contextSym.isPascalString():
            return True

        if self.sectionType == common.FileSectionType.Rodata:
            stringGuesserLevel = common.GlobalConfig.PASCAL_RODATA_STRING_GUESSER_LEVEL
        else:
            stringGuesserLevel = common.GlobalConfig.PASCAL_DATA_STRING_GUESSER_LEVEL

        if stringGuesserLevel < 1:
            return False

        if contextSym.referenceCounter > 1:
            if stringGuesserLevel < 2:
                return False

        # This would mean the string is an empty string, which is not very likely
        if self.words[localOffset//4] == 0:
            if stringGuesserLevel < 3:
                return False

        if contextSym.hasOnlyAutodetectedType():
            if stringGuesserLevel < 4:
                return False

        currentVram = self.getVramOffset(localOffset)
        currentVrom = self.getVromOffset(localOffset)
        _, rawStringSize = common.Utils.decodeBytesToPascalStrings(self.bytes, localOffset, self.stringEncoding, terminator=0x20)
        if rawStringSize < 0:
            # String can't be decoded
            return False

        # Check if there is already another symbol after the current one and before the end of the string,
        # in which case we say this symbol should not be a string
        otherSym = self.getSymbol(currentVram + rawStringSize - 1, vromAddress=currentVrom + rawStringSize, checkUpperLimit=False, checkGlobalSegment=False)
        if otherSym != contextSym:
            return False

        return True


    def blankOutDifferences(self, other: FileBase) -> bool:
        if not common.GlobalConfig.REMOVE_POINTERS:
            return False

        was_updated = False
        if len(common.GlobalConfig.IGNORE_WORD_LIST) > 0:
            min_len = min(self.sizew, other.sizew)
            for i in range(min_len):
                for upperByte in common.GlobalConfig.IGNORE_WORD_LIST:
                    word = upperByte << 24
                    if ((self.words[i] >> 24) & 0xFF) == upperByte and ((other.words[i] >> 24) & 0xFF) == upperByte:
                        self.words[i] = word
                        other.words[i] = word
                        was_updated = True

        return was_updated
