#!/usr/bin/python3

import os, sys, subprocess, multiprocessing;
from multiprocessing import Pool;

benchmarks = {
    "aha-mont64": None,
    "crc32": None,
    "cubic": None,
    "edn": None,
    "huffbench": None,
    "matmult-int": None,
    "minver": None,
    "nbody": None,
    "nettle-aes": None,
    "nettle-sha256": None,
    "nsichneu": None,
    "picojpeg": None,
    "qrduino": None,
    "sglib-combined": None,
    "slre": None,
    "st": None,
    "statemate": None,
    "ud": None,
    "wikisort": None
};

def run_execute_benchmark(path, benchmark):
    # Set the timeout to 100, since the execute benchmarks tend to take a while.
    # (Incidentally, that's also the reason why I'm writing this script...)
    env = os.environ;
    env["BEEBS_TIMEOUT"] = "200";

    cmd = ["make",
           "check",
           "SIZE_EXP=riscv32-unknown-elf-size",
           "RUNTESTFLAGS=execute.exp=" + benchmark];

    print("[INFO]: Running " + benchmark); 
    run = subprocess.run(cmd, cwd = path, env = env,
                         stdout = subprocess.PIPE, stderr = subprocess.PIPE);

    print("[INFO]: Completed " + benchmark); 

#    benchmarks[benchmark] = run.stdout.decode("utf-8").strip();
    
    awk = "/" + benchmark + " +[0-9]+/ { print $2 }";

    print("still here 1");

    cmd = ["awk", awk];

#    print("[INFO]: output produced:");
#    print(run.stdout.decode("utf-8"));

    run = subprocess.run(cmd, stdout = subprocess.PIPE, input = run.stdout);
    result = run.stdout.decode("utf-8").strip();
    print("[INFO] Result for " + benchmark + ": " + result);
    return result;

if "EMBENCH_FILTER" in os.environ:
    filters = os.environ["EMBENCH_FILTER"].split(",");
    argslist = [(".", k) for k, v in benchmarks.items() if k in filters];
else:
    argslist = [(".", k) for k, v in benchmarks.items()];

threads = min(8, len(argslist));

with Pool(threads) as p:
    ret = p.starmap(run_execute_benchmark, argslist);

    for a, r in zip(argslist, ret):
        benchmarks[a[1]] = r;
        
for k, v in benchmarks.items():
    print(k + "," + str(v));
