#!/usr/bin/python3

import os, sys;

template = \
"""
# Chip configuration for no library small size GCC RISC-V Configuration
#
# Copyright (C) 2019 Embecosm Limited and the University of Bristol
#
# Contributor {} <{}>
#
# This file is part of Embench and was formerly part of the Bristol/Embecosm
# Embedded Benchmark Suite.
#
# SPDX-License-Identifier: GPL-3.0-or-later

export CHIP_CFLAGS="-Os -march={} -mabi={} -msave-restore -fdata-sections -ffunction-sections"
export CHIP_LDFLAGS="-Os -march={} -mabi={} -msave-restore -Wl,-gc-sections"

USE_DUMMY_CRT0=no
USE_DUMMY_LIBC=no
USE_DUMMY_LIBGCC=no
USE_DUMMY_LIBM=no
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

chipsdir = sys.argv[1];

for variant in variants:
    contrib_name = sys.argv[2];
    contrib_email = sys.argv[3];

    vdir = "size-test-gcc-bitmanip-libc-" + variant["name"];

    os.mkdir(chipsdir + "/" + vdir);

    # print("DEBUG: Write to file \"" + vdir + "/chip.cfg\":");
    # print(template.format(contrib_name, contrib_email,
    #                       variant["march"], variant["mabi"],
    #                       variant["march"], variant["mabi"]));

    chip_cfg = open(chipsdir + "/" + vdir + "/chip.cfg", "w+");
    chip_cfg.write(template.format(contrib_name, contrib_email,
                                   variant["march"], variant["mabi"],
                                   variant["march"], variant["mabi"]));

