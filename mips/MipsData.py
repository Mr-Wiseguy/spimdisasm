#!/usr/bin/python3

from __future__ import annotations

from .Utils import *
from .GlobalConfig import GlobalConfig
from .MipsFile import File


class Data(File):
    def removePointers(self):
        if not GlobalConfig.REMOVE_POINTERS:
            return
        super().removePointers()

        was_updated = False
        for i in range(self.sizew):
            top_byte = (self.words[i] >> 24) & 0xFF
            if top_byte == 0x80:
                self.words[i] = top_byte << 24
                was_updated = True
            if (top_byte & 0xF0) == 0x00 and (top_byte & 0x0F) != 0x00:
                self.words[i] = top_byte << 24
                was_updated = True

        if was_updated:
            self.updateBytes() 

    def saveToFile(self, filepath: str):
        super().saveToFile(filepath + ".data")

        if self.size == 0:
            return

        with open(filepath + ".data.asm", "w") as f:
            f.write(".section .data\n\n")
            offset = 0
            i = 0
            while i < self.sizew:
                w = self.words[i]
                offsetHex = toHex(offset, 5)[2:]
                vramHex = ""
                if self.vRamStart != -1:
                    currentVram = self.getVramOffset(offset)
                    vramHex = toHex(currentVram, 8)[2:]
                    if currentVram == self.initVarsAddress:
                        f.write(f"glabel {self.filename}_InitVars\n")
                        actorId = toHex((w >> 16) & 0xFFFF, 4)
                        category = toHex((w >> 8) & 0xFF, 2)
                        flags = toHex((self.words[i+1]), 8)
                        objectId = toHex((self.words[i+2] >> 16) & 0xFFFF, 4)
                        instanceSize = toHex(self.words[i+3], 8)
                        f.write(f"/* %05X %08X {actorId[2:].zfill(8)} */  .half  {actorId}\n" % (offset + 0x0, currentVram + 0x0))
                        f.write(f"/* %05X %08X {category[2:].zfill(8)} */  .byte  {category}\n" % (offset + 0x2, currentVram + 0x2))
                        f.write(f"/* %05X %08X {flags[2:].zfill(8)} */  .word  {flags}\n" % (offset + 0x4, currentVram + 0x4))
                        f.write(f"/* %05X %08X {objectId[2:].zfill(8)} */  .half  {objectId}\n" % (offset + 0x8, currentVram + 0x8))
                        f.write(f"/* %05X %08X {instanceSize[2:].zfill(8)} */  .word  {instanceSize}\n" % (offset + 0xC, currentVram + 0xC))
                        init = f"{self.filename}_Init"
                        if self.words[i+4] == 0:
                            init = toHex(0, 8)
                        destroy = f"{self.filename}_Destroy"
                        if self.words[i+5] == 0:
                            destroy = toHex(0, 8)
                        update = f"{self.filename}_Update"
                        if self.words[i+6] == 0:
                            update = toHex(0, 8)
                        draw = f"{self.filename}_Draw"
                        if self.words[i+7] == 0:
                            draw = toHex(0, 8)
                        f.write(f"/* %05X %08X {toHex(self.words[i+4], 8)[2:]} */  .word  {init}\n" % (offset + 0x10, currentVram + 0x10))
                        f.write(f"/* %05X %08X {toHex(self.words[i+5], 8)[2:]} */  .word  {destroy}\n" % (offset + 0x14, currentVram + 0x14))
                        f.write(f"/* %05X %08X {toHex(self.words[i+6], 8)[2:]} */  .word  {update}\n" % (offset + 0x18, currentVram + 0x18))
                        f.write(f"/* %05X %08X {toHex(self.words[i+7], 8)[2:]} */  .word  {draw}\n" % (offset + 0x1C, currentVram + 0x1C))
                        f.write("\n")

                        i += 8
                        offset += 0x20
                        continue

                dataHex = toHex(w, 8)[2:]
                line = toHex(w, 8)

                f.write(f"/* {offsetHex} {vramHex} {dataHex} */  .word  {line}\n")
                i += 1
                offset += 4
