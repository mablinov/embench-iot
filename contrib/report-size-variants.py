#!/usr/bin/python3

import os, sys;

template = \
"""
export CHIP_CFLAGS="-Os -march={} -mabi={} -msave-restore -fdata-sections -ffunction-sections"
export CHIP_LDFLAGS="-Os -march={} -mabi={} -msave-restore -Wl,-gc-sections -nostartfiles -nostdlib"
""";

variants = [
    {"name": "base", "march": "rv32imcb", "mabi": "ilp32"},
    {"name": "zbb", "march": "rv32imc_zbb", "mabi": "ilp32"},
    {"name": "zbc", "march": "rv32imc_zbc", "mabi": "ilp32"},
    {"name": "zbe", "march": "rv32imc_zbe", "mabi": "ilp32"},
    {"name": "zbf", "march": "rv32imc_zbf", "mabi": "ilp32"},
    {"name": "zbm", "march": "rv32imc_zbm", "mabi": "ilp32"},
    {"name": "zbp", "march": "rv32imc_zbp", "mabi": "ilp32"},
    {"name": "zbr", "march": "rv32imc_zbr", "mabi": "ilp32"},
    {"name": "zbs", "march": "rv32imc_zbs", "mabi": "ilp32"},
    {"name": "zbt", "march": "rv32imc_zbt", "mabi": "ilp32"},
    {"name": "none", "march": "rv32imc", "mabi": "ilp32"}
];

for variant in variants:
    vdir = "size-test-gcc-bitmanip-" + variant["name"];

    print(vdir + ":");
    print(template.format(variant["march"], variant["mabi"],
                          variant["march"], variant["mabi"]));
