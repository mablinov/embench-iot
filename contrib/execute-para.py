#!/usr/bin/python3

import os, sys, subprocess, multiprocessing;
from multiprocessing import Pool;

benchmarks = {
    "aha-mont64": {},
    "crc32": {},
    "cubic": {},
    "edn": {},
    "huffbench": {},
    "matmult-int": {},
    "minver": {},
    "nbody": {},
    "nettle-aes": {},
    "nettle-sha256": {},
    "nsichneu": {},
    "picojpeg": {},
    "qrduino": {},
    "sglib-combined": {},
    "slre": {},
    "st": {},
    "statemate": {},
    "ud": {},
    "wikisort": {}
};

def run_execute_benchmark(path, benchmark):
    # Set the timeout to 100, since the execute benchmarks tend to take a while.
    # (Incidentally, that's also the reason why I'm writing this script...)
    env = os.environ;
    env["BEEBS_TIMEOUT"] = "100";

    cmd = ["make",
           "check",
           "SIZE_EXP=riscv32-unknown-elf-size",
           "RUNTESTFLAGS=execute.exp=" + benchmark];

    print("[INFO]: Running " + benchmark); 
    run = subprocess.run(cmd, cwd = path, env = env,
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE);

    print("[INFO]: Completed " + benchmark); 

    benchmarks[benchmark] = run.stdout.decode("utf-8").strip();
    print("[INFO]: Results for " + benchmark + ":");
    print(benchmarks[benchmark]);
    
    return;

with Pool(8) as p:
    p.starmap(run_execute_benchmark, [(".", k) for k, v in benchmarks.items()]);

for k, v in benchmarks.items():
    print("Results for \"" + k + "\":");
    print(v);
