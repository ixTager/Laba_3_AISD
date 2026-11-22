#!/usr/bin/env python3
"""
Hash, compile and fuzz the bracket-parser / balanced-tree implementation.

What it does
------------
1. Takes C++ source files (default: the chosen implementation's sources).
2. Computes an MD5 hash of every C++ file of the project and one aggregate MD5.
3. Compiles those sources into an executable.
4. Implements the *same* observable contract in Python -- parse the bracket
   notation "(value [child] [child])" into a binary tree, insert its values into
   a balanced search tree (AVL or red-black) in preorder, and return the two tree
   heights and the four traversals (breadth-first, preorder, inorder, postorder)
   -- the reference oracle.
5. Generates random trees and runs the compiled executable as a subprocess,
   feeding it one tree per run through stdin, then compares the printed heights
   and four traversals with the oracle.
6. Executes 10 default boundary examples, 3 rejection tests and ~1000 generated
   trees, then writes a pass/fail report.

Usage
-----
    python3 test.py                          # hash + compile + fuzz AVL (default)
    python3 test.py --impl rb                # fuzz the red-black implementation
    python3 test.py avl/main.cpp avl/avl.cpp tree.cpp  # explicit file set
    python3 test.py --seed 7                 # reproducible corpus
    python3 test.py --runs 5000              # more fuzz runs
    python3 test.py --no-build               # test an already built executable
    python3 test.py --binary ./main          # same, explicit executable

Exit status: 0 = all checks passed, 1 = at least one error, 2 = setup problem.
Only the Python standard library is used.
"""

import argparse
import datetime
import hashlib
import os
import random
import shutil
import subprocess
import sys

IS_WINDOWS = os.name == "nt"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

CPP_EXTENSIONS = (".cpp", ".cc", ".cxx", ".c++", ".cp")
HEADER_EXTENSIONS = (".h", ".hpp", ".hh", ".hxx", ".h++", ".inl", ".ipp")
HASH_EXTENSIONS = CPP_EXTENSIONS + HEADER_EXTENSIONS


# ---------------------------------------------------------------------------
# File naming and hashing
# ---------------------------------------------------------------------------


def executable_name(base):
    return base + (".exe" if IS_WINDOWS else "")


IMPLEMENTATIONS = ("avl", "rb")


def default_sources_for_impl(impl):
    """Default translation units compiled for the chosen tree implementation."""
    if impl == "rb":
        return [
            os.path.join(SCRIPT_DIR, "rb", "main.cpp"),
            os.path.join(SCRIPT_DIR, "rb", "rb.cpp"),
            os.path.join(SCRIPT_DIR, "tree.cpp"),
        ]
    return [
        os.path.join(SCRIPT_DIR, "avl", "main.cpp"),
        os.path.join(SCRIPT_DIR, "avl", "avl.cpp"),
        os.path.join(SCRIPT_DIR, "tree.cpp"),
    ]


def default_output_path(source):
    return os.path.join(os.path.dirname(source), executable_name("main"))


def normalize_newlines(text):
    return text.replace("\r\n", "\n").replace("\r", "\n")


def format_command(parts):
    return " ".join(parts)


def relative_path(path, base_dir):
    try:
        return os.path.relpath(path, base_dir)
    except ValueError:
        return path


def collect_cpp_files(sources, extra_files):
    paths = list(sources)
    for path in list(paths):
        directory = os.path.dirname(path)
        if not os.path.isdir(directory):
            continue
        for name in os.listdir(directory):
            candidate = os.path.join(directory, name)
            if os.path.isfile(candidate) and name.lower().endswith(HASH_EXTENSIONS):
                if candidate not in paths:
                    paths.append(candidate)
    for path in extra_files:
        if path not in paths:
            paths.append(path)
    return paths


def md5_of_file(path, chunk_size=65536):
    digest = hashlib.md5()
    size = 0
    with open(path, "rb") as handle:
        while True:
            chunk = handle.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
    return digest.hexdigest(), size


def hash_files(paths, base_dir):
    entries = []
    for path in sorted(set(paths)):
        file_md5, size = md5_of_file(path)
        entries.append((relative_path(path, base_dir), file_md5, size))
    return entries


def aggregate_md5(entries):
    digest = hashlib.md5()
    for relative, file_md5, _size in sorted(entries):
        digest.update(("%s:%s\n" % (relative, file_md5)).encode("utf-8"))
    return digest.hexdigest()


# ---------------------------------------------------------------------------
# Compiler discovery and build
# ---------------------------------------------------------------------------

GCC_COMPILERS = ("g++", "clang++", "c++")
MSVC_COMPILERS = ("cl", "clang-cl")


def find_compiler(requested=None):
    if requested:
        if requested in MSVC_COMPILERS or os.path.basename(requested) in MSVC_COMPILERS:
            return requested, "msvc"
        return requested, "gcc"
    for name in GCC_COMPILERS:
        path = shutil.which(name)
        if path:
            return path, "gcc"
    for name in MSVC_COMPILERS:
        path = shutil.which(name)
        if path:
            return path, "msvc"
    return None, None


def build_executable(compiler, flags, sources, output, kind="gcc", timeout=180):
    if kind == "msvc":
        command = [compiler, "/nologo", "/std:c++14", "/Zi"] + flags + list(sources) + ["/Fe:" + output]
    else:
        command = [compiler] + flags + list(sources) + ["-o", output]
    try:
        proc = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return command, None, "", "compilation timed out"
    except OSError as exc:
        return command, None, "", str(exc)
    return command, proc.returncode, proc.stdout, proc.stderr


# ---------------------------------------------------------------------------
# Reference oracle
# ---------------------------------------------------------------------------
# The readable reference implementation (bracket parser + AVL tree + traversals)
# and the generator that produced the obfuscated function below live in tree.py.
# Regenerate with:    python3 tree.py --write
# Prove it matches:   python3 tree.py --verify

# --- BEGIN GENERATED (tree.py) ---
def expected_for(_da, _c9):
    _7e="\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39"
    _oz="\x28"
    _xk="\x29"
    _o9="\x20"
    _9o="\x6d\x69\x73\x6d\x61\x74\x63\x68\x65\x64\x20\x70\x61\x72\x65\x6e\x74\x68\x65\x73\x65\x73"
    _e8="\x6e\x6f\x74\x20\x61\x20\x62\x69\x6e\x61\x72\x79\x20\x74\x72\x65\x65"
    _u1="\x75\x6e\x6b\x6e\x6f\x77\x6e\x20\x74\x6f\x6b\x65\x6e\x3a\x20"
    _h8="\x6f\x6b"
    _if="\x65\x72\x72\x6f\x72"
    _vr="\x72\x62"
    _2e=Exception
    def _sg(_fz):
        _39=[]
        _ve=0
        while _ve<len(_fz):
            _sc=_fz[_ve]
            if _sc==_o9:
                _ve+=1
            elif _sc==_oz:
                _39.append(_oz)
                _ve+=1
            elif _sc==_xk:
                _39.append(_xk)
                _ve+=1
            elif _sc in _7e:
                _as=_ve
                while _as<len(_fz) and _fz[_as] in _7e:
                    _as+=1
                _39.append(_fz[_ve:_as])
                _ve=_as
            else:
                raise _2e(_u1+_sc)
        return _39
    def _iz(_u7,_j0):
        if _j0>=len(_u7) or _u7[_j0]!=_oz:
            raise _2e(_9o)
        _j0+=1
        if _j0>=len(_u7):
            raise _2e(_9o)
        if not all(_3e in _7e for _3e in _u7[_j0]):
            raise _2e(_u1+_u7[_j0])
        _s6=int(_u7[_j0])
        _j0+=1
        _cz=[_s6,None,None]
        _7q=0
        while _j0<len(_u7) and _u7[_j0]==_oz:
            if _7q>=2:
                raise _2e(_e8)
            _fo,_j0=_iz(_u7,_j0)
            if _7q==0:
                _cz[1]=_fo
            else:
                _cz[2]=_fo
            _7q+=1
        if _j0>=len(_u7) or _u7[_j0]!=_xk:
            raise _2e(_9o)
        _j0+=1
        return _cz,_j0
    def _um(_dg):
        if _dg is None:
            return []
        return [_dg[0]]+_um(_dg[1])+_um(_dg[2])
    def _x1(_7c):
        if _7c is None:
            return 0
        _4l=_x1(_7c[1])
        _v0=_x1(_7c[2])
        return 1+(_4l if _4l>_v0 else _v0)
    def _k4(_4m):
        _fy=[]
        if not _4m:
            return _fy
        _f6=[_4m]
        _fb=0
        while _fb<len(_f6):
            _uk=_f6[_fb]
            _fb+=1
            _fy.append(_uk[0])
            if _uk[1]:
                _f6.append(_uk[1])
            if _uk[2]:
                _f6.append(_uk[2])
        return _fy
    def _oj(_q4):
        _3q=[]
        if not _q4:
            return _3q
        _bj=[_q4]
        while _bj:
            _o1=_bj.pop()
            _3q.append(_o1[0])
            if _o1[2]:
                _bj.append(_o1[2])
            if _o1[1]:
                _bj.append(_o1[1])
        return _3q
    def _b3(_ao):
        _hd=[]
        _kb=[]
        _im=_ao
        while _im or _kb:
            while _im:
                _kb.append(_im)
                _im=_im[1]
            _im=_kb.pop()
            _hd.append(_im[0])
            _im=_im[2]
        return _hd
    def _0l(_5a):
        _m9=[]
        if not _5a:
            return _m9
        _tl=[_5a]
        while _tl:
            _o7=_tl.pop()
            _m9.append(_o7[0])
            if _o7[1]:
                _tl.append(_o7[1])
            if _o7[2]:
                _tl.append(_o7[2])
        _m9.reverse()
        return _m9
    def _1q(_x2):
        return _x2[3] if _x2 is not None else 0
    def _j9(_va):
        _va[3]=1+(_1q(_va[1]) if _1q(_va[1])>_1q(_va[2]) else _1q(_va[2]))
    def _gm(_bn):
        return _1q(_bn[1])-_1q(_bn[2])
    def _18(_2k):
        _u0=_2k[1]
        _32=_u0[2]
        _u0[2]=_2k
        _2k[1]=_32
        _j9(_2k)
        _j9(_u0)
        return _u0
    def _uz(_cv):
        _ig=_cv[2]
        _1k=_ig[1]
        _ig[1]=_cv
        _cv[2]=_1k
        _j9(_cv)
        _j9(_ig)
        return _ig
    def _o3(_bh,_6z):
        if _bh is None:
            return [_6z,None,None,1]
        if _6z<_bh[0]:
            _bh[1]=_o3(_bh[1],_6z)
        elif _6z>_bh[0]:
            _bh[2]=_o3(_bh[2],_6z)
        else:
            return _bh
        _j9(_bh)
        _mg=_gm(_bh)
        if _mg>1 and _6z<_bh[1][0]:
            return _18(_bh)
        if _mg<-1 and _6z>_bh[2][0]:
            return _uz(_bh)
        if _mg>1 and _6z>_bh[1][0]:
            _bh[1]=_uz(_bh[1])
            return _18(_bh)
        if _mg<-1 and _6z<_bh[2][0]:
            _bh[2]=_18(_bh[2])
            return _uz(_bh)
        return _bh
    def _fp(_ak):
        return _ak is not None and _ak[4]
    def _ei(_3w,_5c):
        _6x=_5c[2]
        _5c[2]=_6x[1]
        if _6x[1] is not None:
            _6x[1][3]=_5c
        _6x[3]=_5c[3]
        if _5c[3] is None:
            _3w=_6x
        elif _5c is _5c[3][1]:
            _5c[3][1]=_6x
        else:
            _5c[3][2]=_6x
        _6x[1]=_5c
        _5c[3]=_6x
        return _3w
    def _na(_x0,_9b):
        _r6=_9b[1]
        _9b[1]=_r6[2]
        if _r6[2] is not None:
            _r6[2][3]=_9b
        _r6[3]=_9b[3]
        if _9b[3] is None:
            _x0=_r6
        elif _9b is _9b[3][2]:
            _9b[3][2]=_r6
        else:
            _9b[3][1]=_r6
        _r6[2]=_9b
        _9b[3]=_r6
        return _x0
    def _2d(_v8,_kv):
        _i9=[_kv,None,None,None,True]
        _7h=None
        _pb=_v8
        while _pb is not None:
            _7h=_pb
            if _kv<_pb[0]:
                _pb=_pb[1]
            elif _kv>_pb[0]:
                _pb=_pb[2]
            else:
                return _v8
        _i9[3]=_7h
        if _7h is None:
            _i9[4]=False
            return _i9
        if _kv<_7h[0]:
            _7h[1]=_i9
        else:
            _7h[2]=_i9
        while _i9 is not _v8 and _fp(_i9[3]):
            _xk=_i9[3]
            _s1=_xk[3]
            if _xk is _s1[1]:
                _no=_s1[2]
                if _fp(_no):
                    _xk[4]=False
                    _no[4]=False
                    _s1[4]=True
                    _i9=_s1
                else:
                    if _i9 is _xk[2]:
                        _i9=_xk
                        _v8=_ei(_v8,_i9)
                    _xk=_i9[3]
                    _s1=_xk[3]
                    _xk[4]=False
                    _s1[4]=True
                    _v8=_na(_v8,_s1)
            else:
                _no=_s1[1]
                if _fp(_no):
                    _xk[4]=False
                    _no[4]=False
                    _s1[4]=True
                    _i9=_s1
                else:
                    if _i9 is _xk[1]:
                        _i9=_xk
                        _v8=_na(_v8,_i9)
                    _xk=_i9[3]
                    _s1=_xk[3]
                    _xk[4]=False
                    _s1[4]=True
                    _v8=_ei(_v8,_s1)
        _v8[4]=False
        return _v8
    def _tv(_wh):
        if _wh is None:
            return 0
        _qr=_tv(_wh[1])
        _hk=_tv(_wh[2])
        return 1+(_qr if _qr>_hk else _hk)
    try:
        _eh=_sg(_da)
        _h2,_9j=_iz(_eh,0)
        if _9j<len(_eh):
            raise _2e(_u1+_eh[_9j])
        _w8=_x1(_h2)
        _06=_um(_h2)
        _6q=None
        if _c9==_vr:
            for _e4 in _06:
                _6q=_2d(_6q,_e4)
            _6r=_tv(_6q)
        else:
            for _e4 in _06:
                _6q=_o3(_6q,_e4)
            _6r=_1q(_6q)
        return (_h8,[str(_w8),str(_6r),[str(_u2) for _u2 in _k4(_6q)],[str(_u2) for _u2 in _oj(_6q)],[str(_u2) for _u2 in _b3(_6q)],[str(_u2) for _u2 in _0l(_6q)]])
    except _2e as _z5:
        return (_if,str(_z5))

# --- END GENERATED (tree.py) ---


# ---------------------------------------------------------------------------
# Target program interaction
# ---------------------------------------------------------------------------

TARGET_HEADER = "\n\n"
TRAVERSAL_NAMES = ("breadth-first", "preorder", "inorder", "postorder")


def parse_target_output(stdout):
    """
    Extract the two heights and the four traversal token lists from stdout.

    main.cpp prints: <echo> + blank line + six lines:
      1. plain binary tree height
      2. balanced tree (AVL or red-black) height
      3-6. breadth-first, preorder, inorder, postorder (each a ", "-joined list).
    Returns [binary_height, tree_height, bfs, pre, in, post], or None.
    """
    stdout = normalize_newlines(stdout)
    marker = stdout.find(TARGET_HEADER)
    if marker == -1:
        return None
    tail = stdout[marker + len(TARGET_HEADER):].strip()
    if tail == "":
        return None
    lines = tail.split("\n")
    if len(lines) != 6:
        return None
    result = [lines[0].strip(), lines[1].strip()]
    for i in range(2, 6):
        line = lines[i].strip()
        if line == "":
            result.append([])
        else:
            result.append([token.strip() for token in line.split(",") if token.strip() != ""])
    return result


def run_target(binary, expression, timeout):
    """Run the target once, feeding the input string on stdin."""
    try:
        proc = subprocess.run(
            [binary],
            input=expression + "\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "returncode": None, "stdout": "", "stderr": ""}
    except OSError as exc:
        raise RuntimeError("cannot execute %s: %s" % (binary, exc))

    return {
        "status": "ran",
        "returncode": proc.returncode,
        "stdout": normalize_newlines(proc.stdout),
        "stderr": normalize_newlines(proc.stderr),
    }


def check_case(binary, expression, timeout, impl):
    """
    Compare the target against the oracle for one input.

    Returns (category, expected, actual); category is None when the case passed.
    """
    kind, expected = expected_for(expression, impl)
    result = run_target(binary, expression, timeout)

    if result["status"] == "timeout":
        return ("timeout", expected, "no answer within %gs" % timeout)

    returncode = result["returncode"]
    stdout = result["stdout"]
    stderr = result["stderr"].strip()

    if returncode < 0:
        return ("crash", expected, "killed by signal %d" % -returncode)

    if kind == "error":
        # The oracle rejects this input: the target has to reject it too.
        if returncode == 0:
            return (
                "not_rejected",
                expected,
                "exit=0, stdout=%r (expected rejection: %s)" % (stdout.strip(), expected),
            )
        if stderr == "":
            return ("silent_rejection", expected, "exit=%d but stderr is empty" % returncode)
        return (None, expected, "exit=%d, stderr=%r" % (returncode, stderr))

    # Oracle accepts the input: the target must print the four traversals.
    if returncode != 0:
        return (
            "nonzero_exit",
            expected,
            "exit=%d, stderr=%r" % (returncode, stderr or stdout.strip()),
        )

    actual = parse_target_output(stdout)
    if actual is None:
        return ("bad_format", expected, "unparsable stdout=%r" % stdout)

    if actual != expected:
        return ("mismatch", expected, actual)

    if stderr != "":
        return ("unexpected_stderr", expected, "stderr=%r" % stderr)

    return (None, expected, actual)


# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------

DEFAULT_BOUND_TESTS = [
    "(5)",
    "(8 (9 (5)) (1))",
    "(1 (2))",
    "(1 (2) (3))",
    "(3 (2 (1)) (4 (5)))",
    "(1 (2 (3) (4)) (5 (6) (7)))",
    "(10 (20) (30 (40 (50))))",
    "(1 (2 (3 (4 (5 (6 (7)))))))",
    "(50 (40 (30 (20 (10)))))",
    "(7 (3 (1) (5)) (11 (9) (13)))",
]

REJECTION_TESTS = [
    "(a)",
    "(1",
    "(1 (2) (3) (4))",
]

MAX_VALUE = 999999


def random_tree(rng, depth):
    value = rng.randint(0, MAX_VALUE)
    if depth <= 0 or rng.random() < 0.35:
        return "( %d )" % value
    left = random_tree(rng, depth - 1)
    if rng.random() < 0.5:
        return "( %d %s )" % (value, left)
    right = random_tree(rng, depth - 1)
    return "( %d %s %s )" % (value, left, right)


def random_input(rng, max_depth=5):
    """Generate one valid bracket-notation tree and the number of nodes in it."""
    expression = random_tree(rng, rng.randint(0, max_depth))
    return expression, expression.count("(")


CATEGORY_LABELS = {
    "mismatch": "wrong traversal output",
    "not_rejected": "invalid input accepted (exit 0)",
    "silent_rejection": "rejected without a stderr message",
    "nonzero_exit": "valid input rejected (non-zero exit)",
    "bad_format": "stdout does not follow the echo + blank + 4 lines contract",
    "unexpected_stderr": "valid input produced stray stderr output",
    "timeout": "target did not finish in time",
    "crash": "target crashed (signal)",
}


def traversal_text(values):
    return ", ".join(values) if values else "(empty)"


def write_report(path, lines):
    with open(path, "w") as handle:
        handle.write("\n".join(lines) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Hash and compile C++ sources, then fuzz the executable against a Python oracle."
    )
    parser.add_argument("sources", nargs="*", metavar="FILE", help="C++ files to hash and compile (default: the chosen implementation's sources).")
    parser.add_argument("--impl", choices=IMPLEMENTATIONS, default="avl",
                        help="tree implementation to verify: 'avl' (default) or 'rb'.")
    parser.add_argument("--compiler", default=None, help="C++ compiler: a path or name (g++, clang++, c++, cl, clang-cl).")
    parser.add_argument("--cxxflags", default="-std=c++11 -g", help="compiler flags, GCC-style (default: '-std=c++11 -g').")
    parser.add_argument("--std", default=None, help="C++ standard, e.g. c++11, c++17.")
    parser.add_argument("--output", default=None, help="executable to produce (default: main[.exe] next to the first source).")
    parser.add_argument("--no-build", action="store_true", help="do not compile; test the existing executable.")
    parser.add_argument("--binary", default=None, help="existing executable to test (implies --no-build).")
    parser.add_argument("--runs", type=int, default=1000, help="number of fuzz runs (default: 1000).")
    parser.add_argument("--seed", type=int, default=20261021, help="random seed (default: 20261021).")
    parser.add_argument("--max-depth", type=int, default=5, help="max generated tree depth.")
    parser.add_argument("--timeout", type=float, default=5.0, help="per-run timeout in seconds.")
    parser.add_argument("--max-examples", type=int, default=10, help="failure examples kept in the report.")
    parser.add_argument("--report", default="fuzz_report.md", help="report file to write.")
    args = parser.parse_args(argv)

    # --- resolve the C++ inputs -------------------------------------------
    sources = [os.path.abspath(path) for path in args.sources]
    if not sources:
        default_sources = default_sources_for_impl(args.impl)
        sources = [path for path in default_sources if os.path.isfile(path)]
        if not sources and not args.no_build and not args.binary:
            sys.stderr.write("error: no C++ source file given and no sources found for implementation %r\nusage: python3 test.py --impl %s\n" % (args.impl, args.impl))
            return 2

    for path in sources:
        if not os.path.isfile(path):
            sys.stderr.write("error: source file not found: %s\n" % path)
            return 2

    compile_sources = [path for path in sources if not path.lower().endswith(HEADER_EXTENSIONS)]
    if not compile_sources and not (args.no_build or args.binary):
        sys.stderr.write("error: no compilable C++ source given (only headers were listed)\n")
        return 2

    # --- hash every C++ file of the project --------------------------------
    hash_inputs = collect_cpp_files(sources, [])
    hash_entries = hash_files(hash_inputs, SCRIPT_DIR)
    sources_md5 = aggregate_md5(hash_entries)

    # --- obtain the executable under test ----------------------------------
    build_command = None
    target = None

    if args.binary:
        if not os.path.isfile(args.binary):
            sys.stderr.write("error: executable not found: %s\n" % args.binary)
            return 2
        target = os.path.abspath(args.binary)
    elif args.no_build:
        candidate = args.output or default_output_path(compile_sources[0] if compile_sources else sources[0])
        if not os.path.isfile(candidate):
            sys.stderr.write("error: --no-build was given but no executable exists at %s\n" % os.path.abspath(candidate))
            return 2
        target = os.path.abspath(candidate)
    else:
        compiler, kind = find_compiler(args.compiler)
        if compiler is None:
            sys.stderr.write("error: no C++ compiler found (looked for g++, clang++, c++, cl, clang-cl on PATH)\n")
            return 2

        flags = args.cxxflags.split()
        if args.std:
            wanted = args.std.strip()
            replaced = False
            for position, flag in enumerate(flags):
                if flag.lower().startswith(("-std=", "--std=", "/std:")):
                    flags[position] = "-std=" + wanted
                    replaced = True
            if not replaced:
                flags.append("-std=" + wanted)

        output = os.path.abspath(args.output) if args.output else default_output_path(compile_sources[0])
        build_command, returncode, compiler_out, compiler_err = build_executable(compiler, flags, compile_sources, output, kind=kind)

        if returncode is None:
            sys.stderr.write("error: could not run %s: %s\n" % (compiler, compiler_err))
            return 2
        if returncode != 0:
            sys.stderr.write("error: compilation failed (exit %d)\n  %s\n" % (returncode, format_command(build_command)))
            if compiler_out.strip():
                sys.stderr.write(compiler_out)
            sys.stderr.write(compiler_err)
            return 2
        target = output

    if not IS_WINDOWS and not os.access(target, os.X_OK):
        sys.stderr.write("error: target is not executable: %s\nfix it with: chmod +x %s\n" % (target, target))
        return 2

    target_md5, target_size = md5_of_file(target)

    rng = random.Random(args.seed)
    started = datetime.datetime.now()

    failures = []
    counts = {}
    corpus_stats = {"bound": 0, "rejection": 0, "fuzz": 0}
    node_sum = 0
    node_max = 0

    def record(corpus, expression, category, expected, actual):
        if category is None:
            return
        failures.append((corpus, expression, category, expected, actual))
        counts[category] = counts.get(category, 0) + 1

    # --- default boundary tests -------------------------------------------
    bound_results = []
    for expression in DEFAULT_BOUND_TESTS:
        category, expected, actual = check_case(target, expression, args.timeout, args.impl)
        corpus_stats["bound"] += 1
        bound_results.append((expression, category, expected, actual))
        record("bound", expression, category, expected, actual)

    # --- rejection tests ---------------------------------------------------
    rejection_results = []
    for expression in REJECTION_TESTS:
        category, expected, actual = check_case(target, expression, args.timeout, args.impl)
        corpus_stats["rejection"] += 1
        rejection_results.append((expression, category, expected, actual))
        record("rejection", expression, category, expected, actual)

    # --- fuzzing -----------------------------------------------------------
    for _ in range(args.runs):
        expression, nodes = random_input(rng, max_depth=args.max_depth)
        node_sum += nodes
        node_max = max(node_max, nodes)
        category, expected, actual = check_case(target, expression, args.timeout, args.impl)
        corpus_stats["fuzz"] += 1
        record("fuzz", expression, category, expected, actual)

    node_avg = (node_sum / args.runs) if args.runs else 0.0

    finished = datetime.datetime.now()
    elapsed = (finished - started).total_seconds()

    total_runs = corpus_stats["bound"] + corpus_stats["rejection"] + corpus_stats["fuzz"]
    total_errors = len(failures)
    passed = total_errors == 0

    # --- console output ----------------------------------------------------
    print("Bracket tree / %s fuzzer" % args.impl.upper())
    print("  C++ files     : %d hashed" % len(hash_entries))
    for relative, file_md5, size in hash_entries:
        print("      %-42s %s  (%d B)" % (relative, file_md5, size))
    print("  MD5 (all C++) : %s" % sources_md5)
    if build_command:
        print("  build         : %s" % format_command(build_command))
    else:
        print("  build         : skipped (using existing executable)")
    print("  target        : %s" % target)
    print("  target MD5    : %s  (%d B)" % (target_md5, target_size))
    print("  seed          : %d   (reproducible corpus)" % args.seed)
    print("  bound tests   : %d" % corpus_stats["bound"])
    print("  rejection test: %d" % corpus_stats["rejection"])
    print("  fuzz runs     : %d" % corpus_stats["fuzz"])
    print("  tree nodes    : avg %.2f, max %d" % (node_avg, node_max))
    print("  total runs    : %d" % total_runs)
    print("  errors        : %d" % total_errors)
    print("  elapsed       : %.2fs" % elapsed)
    print("")
    print("Bound test examples:")
    for expression, category, expected, actual in bound_results:
        if category is None:
            print("  [PASS] %-40s -> h=%s/%s %s" % (expression, actual[0], actual[1], traversal_text(actual[2])))
        else:
            print("  [FAIL] %-40s -> %s (%s)" % (expression, category, actual))
    print("")
    if counts:
        print("Error breakdown:")
        for category in sorted(counts):
            print("  %-18s %d  (%s)" % (category, counts[category], CATEGORY_LABELS.get(category, "")))
        print("")
        print("First failures:")
        for corpus, expression, category, expected, actual in failures[: args.max_examples]:
            print("  [%s] %s" % (corpus, expression))
            print("      expected: %s" % (expected,))
            print("      actual  : %s" % (actual,))
        print("")
    print("RESULT: %s" % ("PASS - target matches the reference implementation" if passed else "FAIL - %d error(s) found" % total_errors))

    # --- report file -------------------------------------------------------
    report = []
    report.append("# Bracket tree / %s fuzzing report" % args.impl.upper())
    report.append("")
    report.append("- Generated: %s" % finished.strftime("%Y-%m-%d %H:%M:%S"))
    report.append("- Platform: `%s` (executable suffix `%s`)" % (sys.platform, ".exe" if IS_WINDOWS else "(none)"))
    report.append("- **MD5 of all C++ files: `%s`** (%d files)" % (sources_md5, len(hash_entries)))
    report.append("- Executable: `%s`" % relative_path(target, SCRIPT_DIR))
    report.append("- Executable MD5: `%s` (%d bytes)" % (target_md5, target_size))
    if build_command:
        report.append("- Compiled with: `%s`" % format_command(build_command))
    else:
        report.append("- Compilation skipped (`--no-build`), an existing executable was tested")
    report.append("- Reference: Python oracle implementing the same contract (bracket notation -> %s four traversals)" % args.impl.upper())
    report.append("- Random seed: `%d` (re-run with `--seed %d` to reproduce)" % (args.seed, args.seed))
    report.append("- Fuzz runs requested: %d (max tree depth %d)" % (args.runs, args.max_depth))
    report.append("- Generated trees: average node count %.2f, max node count %d" % (node_avg, node_max))
    report.append("- Per-run timeout: %gs" % args.timeout)
    report.append("- Duration: %.2fs" % elapsed)
    report.append("")
    report.append("## Verdict")
    report.append("")
    report.append("**%s**" % ("PASS" if passed else "FAIL"))
    report.append("")
    report.append("| Metric | Value |")
    report.append("| --- | --- |")
    report.append("| Total executions | %d |" % total_runs)
    report.append("| 10 default bound examples | %d |" % corpus_stats["bound"])
    report.append("| Rejection (error handling) tests | %d |" % corpus_stats["rejection"])
    report.append("| Random fuzz runs | %d |" % corpus_stats["fuzz"])
    report.append("| Average node count | %.2f |" % node_avg)
    report.append("| Max node count | %d |" % node_max)
    report.append("| Errors found | **%d** |" % total_errors)
    report.append("| Pass rate | %.2f%% |" % (100.0 * (total_runs - total_errors) / total_runs if total_runs else 0.0))
    report.append("")
    report.append("## C++ files hashed (MD5)")
    report.append("")
    report.append("Aggregate MD5 of all C++ files: **`%s`**" % sources_md5)
    report.append("")
    report.append("| File | Size (bytes) | MD5 |")
    report.append("| --- | --- | --- |")
    for relative, file_md5, size in hash_entries:
        report.append("| `%s` | %d | `%s` |" % (relative, size, file_md5))
    report.append("")
    report.append("| Artifact | Size (bytes) | MD5 |")
    report.append("| --- | --- | --- |")
    report.append("| `%s` (executable) | %d | `%s` |" % (relative_path(target, SCRIPT_DIR), target_size, target_md5))
    report.append("")
    report.append("## Default bound test examples")
    report.append("")
    report.append("| # | Input | binary height | %s height | breadth-first | preorder | inorder | postorder | Result |" % args.impl.upper())
    report.append("| --- | --- | --- | --- | --- | --- | --- | --- | --- |")
    for position, (expression, category, expected, actual) in enumerate(bound_results, 1):
        if category is None:
            result_text = "PASS"
            cells = actual
        else:
            result_text = "FAIL (%s)" % category
            cells = [str(actual)] * 6
        report.append("| %d | `%s` | `%s` | `%s` | `%s` | `%s` | `%s` | `%s` | %s |"
                      % (position, expression, cells[0], cells[1], traversal_text(cells[2]),
                         traversal_text(cells[3]), traversal_text(cells[4]), traversal_text(cells[5]), result_text))
    report.append("")
    report.append("## Error handling tests")
    report.append("")
    report.append("| Input | Expected | Result |")
    report.append("| --- | --- | --- |")
    for expression, category, expected, actual in rejection_results:
        expected_text = "reject: %s" % expected
        result_text = "PASS (exit non-zero)" if category is None else "FAIL (%s)" % category
        report.append("| `%s` | %s | %s |" % (expression, expected_text, result_text))
    report.append("")
    report.append("## Error breakdown")
    report.append("")
    if counts:
        report.append("| Category | Count | Meaning |")
        report.append("| --- | --- | --- |")
        for category in sorted(counts):
            report.append("| `%s` | %d | %s |" % (category, counts[category], CATEGORY_LABELS.get(category, "")))
    else:
        report.append("No errors: every execution matched the reference implementation.")
    report.append("")
    if failures:
        report.append("## Failure examples (first %d)" % min(args.max_examples, len(failures)))
        report.append("")
        for corpus, expression, category, expected, actual in failures[: args.max_examples]:
            report.append("- **%s** [%s] `%s`" % (category, corpus, expression))
            report.append("  - expected: `%s`" % (expected,))
            report.append("  - actual: `%s`" % (actual,))
        report.append("")
    report.append("## Notes")
    report.append("")
    report.append("- The MD5 hashes cover every C++ file of the project: the listed sources and all `.cpp`/`.hpp`/`.h` files next to them.")
    report.append("  The aggregate hash is computed from the sorted `<path>:<md5>` lines, so it changes whenever any file changes, is added, removed or renamed,")
    report.append("  and it does not depend on the order the files were listed in or on the absolute path of the project.")
    report.append("- The executable MD5 identifies the exact binary that was tested; it may differ between identical builds on some linkers. The aggregate C++ MD5")
    report.append("  is the stable identity of the sources.")
    report.append("- The oracle re-implements the bracket parser and the AVL / red-black insertion and rotations (there is no standard-library equivalent), so it")
    report.append("  lives in `tree.py` and is embedded into `test.py` only in obfuscated form.")
    report.append("- The contract: parse bracket notation into a plain binary tree, insert its values into the chosen balanced tree (AVL or red-black) in preorder")
    report.append("  (duplicates once), then print the plain tree height, the balanced tree height, and the four traversals -- breadth-first, preorder, inorder,")
    report.append("  postorder -- each on its own line, values joined with `\", \"`.")
    report.append("- Every fuzz input is a valid binary tree; malformed input is *not* generated. The error paths are exercised only by the fixed rejection tests.")
    report.append("- A passing run means the compiled target agrees with the reference on every bound and fuzz case, with no crash, timeout or stray stderr output.")

    report_path = os.path.abspath(args.report)
    write_report(report_path, report)
    print("Report written to %s" % report_path)

    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
