#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
#
# Reproducible patcher for the vangogh libdpps.so DPPS_THREAD crash.
#
# Original blob:
#   sha256 a12cba0dcd99b7e583a83f56888431c81e4212aaab36fa7f15cdcde2806ea647
# Patched blob:
#   sha256 f65529a89cf1b987048843b9c4785bd7f954f688fb7518fc242d00423feb1174
#
# The crash is at DppsFactoryImpSDM::GetLtmXmlParser+1076 (0x9e570):
#   ldr x8, [x23, #0x28]   ; x23 is TLS, corrupted to 0 by a callee
# The stack canary check reads through the corrupted TLS register and faults
# at address 0x28. Replace it with a load of the saved canary from the stack:
#   ldur x8, [x29, #-8]
# The compare against [x29, #-8] then passes; the epilogue restores x23 from
# the stack and the function returns normally. This does not alter the
# LTM parser result or any other DPPS feature.
#
# Usage: ./patch-libdpps.py /path/to/libdpps.so

import hashlib
import sys

ORIGINAL_SHA256 = "a12cba0dcd99b7e583a83f56888431c81e4212aaab36fa7f15cdcde2806ea647"
PATCHED_SHA256 = "f65529a89cf1b987048843b9c4785bd7f954f688fb7518fc242d00423feb1174"
OFFSET = 0x9E570
OLD = bytes.fromhex("e81640f9")  # ldr x8, [x23, #0x28]
NEW = bytes.fromhex("a8835ff8")  # ldur x8, [x29, #-8]


def main() -> int:
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} /path/to/libdpps.so", file=sys.stderr)
        return 2
    path = sys.argv[1]
    with open(path, "rb") as f:
        data = bytearray(f.read())

    digest = hashlib.sha256(data).hexdigest()
    if digest == PATCHED_SHA256:
        print(f"{path}: already patched")
        return 0
    if digest != ORIGINAL_SHA256:
        print(f"{path}: unexpected sha256 {digest}", file=sys.stderr)
        return 1
    if data[OFFSET:OFFSET + 4] != OLD:
        print(f"{path}: unexpected bytes at 0x{OFFSET:x}", file=sys.stderr)
        return 1

    data[OFFSET:OFFSET + 4] = NEW
    with open(path, "wb") as f:
        f.write(data)

    digest = hashlib.sha256(data).hexdigest()
    if digest != PATCHED_SHA256:
        print(f"{path}: patched sha256 mismatch: {digest}", file=sys.stderr)
        return 1
    print(f"{path}: patched successfully ({digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
