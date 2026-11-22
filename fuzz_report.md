# Bracket tree / AVL fuzzing report

- Generated: 2026-11-22 23:11:32
- Platform: `win32` (executable suffix `.exe`)
- **MD5 of all C++ files: `99d123049001a03bf5f7164bd70ae6ee`** (9 files)
- Executable: `main.exe`
- Executable MD5: `6ce0cf676fdd0625f16d660bf85bde5a` (186776 bytes)
- Compiled with: `C:\msys64\ucrt64\bin\g++.EXE -std=c++11 -g C:\Users\levic\OneDrive\Desktop\Github\Laba_3_AISD\main.cpp -o C:\Users\levic\OneDrive\Desktop\Github\Laba_3_AISD\main.exe`
- Reference: Python oracle implementing the same contract (bracket notation -> AVL four traversals)
- Random seed: `20261021` (re-run with `--seed 20261021` to reproduce)
- Fuzz runs requested: 1000 (max tree depth 5)
- Generated trees: average node count 3.22, max node count 27
- Per-run timeout: 5s
- Duration: 9.72s

## Verdict

**PASS**

| Metric | Value |
| --- | --- |
| Total executions | 1013 |
| 10 default bound examples | 10 |
| Rejection (error handling) tests | 3 |
| Random fuzz runs | 1000 |
| Average node count | 3.22 |
| Max node count | 27 |
| Errors found | **0** |
| Pass rate | 100.00% |

## C++ files hashed (MD5)

Aggregate MD5 of all C++ files: **`99d123049001a03bf5f7164bd70ae6ee`**

| File | Size (bytes) | MD5 |
| --- | --- | --- |
| `AVLNode.h` | 211 | `a0b636e7bcca4508513da9663509704a` |
| `AVLTree.h` | 7791 | `bc7853df47df00023f0e18dce3f4eb9d` |
| `BinaryTree.h` | 1612 | `9800f839e63d2d12f0e4f52be918ec03` |
| `DoublyLinkedList.h` | 2022 | `37fdee2da2647cda297372a089edf14c` |
| `DynamicArray.h` | 1804 | `4600de67b44d2fe664bb1bfc253d6c62` |
| `Stack.h` | 574 | `43a2f7860e5a08ed7843426c9ac69e49` |
| `TreeNode.h` | 164 | `fe393a8ea2b7c3b274f691df9656711d` |
| `TreeParser.h` | 2546 | `c6669f967f749b1dd499741b37a6fe7d` |
| `main.cpp` | 1354 | `a1fb1d7ea1cab66719fc3e5c6046a9fa` |

| Artifact | Size (bytes) | MD5 |
| --- | --- | --- |
| `main.exe` (executable) | 186776 | `6ce0cf676fdd0625f16d660bf85bde5a` |

## Default bound test examples

| # | Input | binary height | AVL height | breadth-first | preorder | inorder | postorder | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `(5)` | `1` | `1` | `5` | `5` | `5` | `5` | PASS |
| 2 | `(8 (9 (5)) (1))` | `3` | `3` | `8, 5, 9, 1` | `8, 5, 1, 9` | `1, 5, 8, 9` | `1, 5, 9, 8` | PASS |
| 3 | `(1 (2))` | `2` | `2` | `1, 2` | `1, 2` | `1, 2` | `2, 1` | PASS |
| 4 | `(1 (2) (3))` | `2` | `2` | `2, 1, 3` | `2, 1, 3` | `1, 2, 3` | `1, 3, 2` | PASS |
| 5 | `(3 (2 (1)) (4 (5)))` | `3` | `3` | `2, 1, 4, 3, 5` | `2, 1, 4, 3, 5` | `1, 2, 3, 4, 5` | `1, 3, 5, 4, 2` | PASS |
| 6 | `(1 (2 (3) (4)) (5 (6) (7)))` | `3` | `3` | `4, 2, 6, 1, 3, 5, 7` | `4, 2, 1, 3, 6, 5, 7` | `1, 2, 3, 4, 5, 6, 7` | `1, 3, 2, 5, 7, 6, 4` | PASS |
| 7 | `(10 (20) (30 (40 (50))))` | `4` | `3` | `20, 10, 40, 30, 50` | `20, 10, 40, 30, 50` | `10, 20, 30, 40, 50` | `10, 30, 50, 40, 20` | PASS |
| 8 | `(1 (2 (3 (4 (5 (6 (7)))))))` | `7` | `3` | `4, 2, 6, 1, 3, 5, 7` | `4, 2, 1, 3, 6, 5, 7` | `1, 2, 3, 4, 5, 6, 7` | `1, 3, 2, 5, 7, 6, 4` | PASS |
| 9 | `(50 (40 (30 (20 (10)))))` | `5` | `3` | `40, 20, 50, 10, 30` | `40, 20, 10, 30, 50` | `10, 20, 30, 40, 50` | `10, 30, 20, 50, 40` | PASS |
| 10 | `(7 (3 (1) (5)) (11 (9) (13)))` | `3` | `3` | `7, 3, 11, 1, 5, 9, 13` | `7, 3, 1, 5, 11, 9, 13` | `1, 3, 5, 7, 9, 11, 13` | `1, 5, 3, 9, 13, 11, 7` | PASS |

## Error handling tests

| Input | Expected | Result |
| --- | --- | --- |
| `(a)` | reject: unknown token: a | PASS (exit non-zero) |
| `(1` | reject: mismatched parentheses | PASS (exit non-zero) |
| `(1 (2) (3) (4))` | reject: not a binary tree | PASS (exit non-zero) |

## Error breakdown

No errors: every execution matched the reference implementation.

## Notes

- The MD5 hashes cover every C++ file of the project: the listed sources and all `.cpp`/`.hpp`/`.h` files next to them.
  The aggregate hash is computed from the sorted `<path>:<md5>` lines, so it changes whenever any file changes, is added, removed or renamed,
  and it does not depend on the order the files were listed in or on the absolute path of the project.
- The executable MD5 identifies the exact binary that was tested; it may differ between identical builds on some linkers. The aggregate C++ MD5
  is the stable identity of the sources.
- The oracle re-implements the bracket parser and the AVL / red-black insertion and rotations (there is no standard-library equivalent), so it
  lives in `tree.py` and is embedded into `test.py` only in obfuscated form.
- The contract: parse bracket notation into a plain binary tree, insert its values into the chosen balanced tree (AVL or red-black) in preorder
  (duplicates once), then print the plain tree height, the balanced tree height, and the four traversals -- breadth-first, preorder, inorder,
  postorder -- each on its own line, values joined with `", "`.
- Every fuzz input is a valid binary tree; malformed input is *not* generated. The error paths are exercised only by the fixed rejection tests.
- A passing run means the compiled target agrees with the reference on every bound and fuzz case, with no crash, timeout or stray stderr output.
