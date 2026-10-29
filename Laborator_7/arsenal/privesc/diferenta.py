# -*- coding: utf-8 -*-
"""Laboratorul 7, partea B: ce e nou fata de un sistem curat."""
import os
from arsenal.privesc.enum import cai, suid_noi, risc_pe_nume, periculoase_noi

AICI = os.path.join(os.path.dirname(os.path.abspath(__file__)), "start")


def main():
    baza = cai(os.path.join(AICI, "baza_suid.txt"))
    acum = cai(os.path.join(AICI, "suid.txt"))
    print("baza:", len(baza), " acum:", len(acum))
    noi = suid_noi(acum, baza)
    print(len(noi), "SUID noi fata de sistemul curat")
    for c in sorted(noi):
        print(" ", c)
    risc = risc_pe_nume(noi)
    periculoase = periculoase_noi(noi)
    print("periculoase NOI:", periculoase)
    return risc


if __name__ == "__main__":
    main()
