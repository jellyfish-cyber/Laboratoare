# -*- coding: utf-8 -*-
"""Un test care prinde regresia: diferenta de multimi da doar ce e nou."""
from arsenal.privesc.enum import suid_noi


def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b"}
    assert suid_noi(acum, baza) == {"c"}
    assert suid_noi(baza, acum) == set()
    assert suid_noi(set(), baza) == set()


if __name__ == "__main__":
    test_doar_ce_e_nou()
    print("Testul a trecut.")
