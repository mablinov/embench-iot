#!/usr/bin/python3

import os, sys, subprocess, csv;

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
    {"name": "none", "march": "rv32imc", "mabi": "ilp32"},

    {"name": "libc-base", "march": "rv32imcb", "mabi": "ilp32"},
    {"name": "libc-zbb", "march": "rv32imc_zbb", "mabi": "ilp32"},
    {"name": "libc-zbc", "march": "rv32imc_zbc", "mabi": "ilp32"},
    {"name": "libc-zbe", "march": "rv32imc_zbe", "mabi": "ilp32"},
    {"name": "libc-zbf", "march": "rv32imc_zbf", "mabi": "ilp32"},
    {"name": "libc-zbm", "march": "rv32imc_zbm", "mabi": "ilp32"},
    {"name": "libc-zbp", "march": "rv32imc_zbp", "mabi": "ilp32"},
    {"name": "libc-zbr", "march": "rv32imc_zbr", "mabi": "ilp32"},
    {"name": "libc-zbs", "march": "rv32imc_zbs", "mabi": "ilp32"},
    {"name": "libc-zbt", "march": "rv32imc_zbt", "mabi": "ilp32"},
    {"name": "libc-none", "march": "rv32imc", "mabi": "ilp32"}
];

embench_iot = "/home/maxim/dev/riscv-bmi/repo/embench-iot";

def run_all_benchmarks():
    for variant in variants:
        vdir = "size-test-gcc-bitmanip-" + variant["name"];

        try:
            os.mkdir(vdir);
        except FileExistsError:
            print("Directory \"" + vdir + "\" already exists, skipping...");
            continue;

        cmd = [embench_iot + "/./configure",
               "--host=riscv32-unknown-elf",
               "--with-board=picorv32verilator",
               "--with-chip=" + vdir];

        subprocess.run(cmd, cwd = vdir);

        make = ["make",
                "-j8",
                "RUNTESTFLAGS=size.exp"];

        subprocess.run(make, cwd = vdir);

def collect_result(variant, benchmark):
    # Probably not very """pythonic"""...

    vdir = "size-test-gcc-bitmanip-" + variant;

    sizeprog = "riscv32-unknown-elf-size";
    awkscript = "BEGIN { lineno = 0 } { if(lineno++ == 1) { print $1 } }";

    cmd = [sizeprog,
           "-G",
           os.path.join(vdir, "src", benchmark, benchmark)];

    ret = subprocess.run(cmd, stdout=subprocess.PIPE);

    # ret.stdout contains the output of running `size`.
    # we need the .text value, so uuh... lets just feed it into awk, I guess.

    cmd = ["awk",
           awkscript];

    ret = subprocess.run(cmd, input=ret.stdout, stdout=subprocess.PIPE);
    return int(ret.stdout);

benchmarks = [
    "aha-mont64",
    "crc32",
    "cubic",
    "edn",
    "huffbench",
    "matmult-int",
    "minver",
    "nbody",
    "nettle-aes",
    "nettle-sha256",
    "nsichneu",
    "picojpeg",
    "qrduino",
    "sglib-combined",
    "slre",
    "st",
    "statemate",
    "ud",
    "wikisort"
];

def main():
    if len(sys.argv) < 2:
        csvname = "results.csv";
    else:
        csvname = sys.argv[1];

    run_all_benchmarks();

    # Results matrix.
    # * Each row is a toolchain variant (*-none, *-base, *-zbb, etc.)
    # * Each column is the .text for the entire set of benchmarks
    #   for the given toolchain variant.

    # Initialise it with a header.
    results = [[""] + benchmarks];

    for variant in variants:
        row = [variant["name"]];
        
        for benchmark in benchmarks:
            row.append(collect_result(variant["name"], benchmark));
        results.append(row);

    # Let's not overwrite the previous result.
    with open(csvname, "w") as csvfile:
        writer = csv.writer(csvfile);

        for row in results:
            print("Writing " ", ".join([str(n) for n in row]));
            writer.writerow(row);

main();
