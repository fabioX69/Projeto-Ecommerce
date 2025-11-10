# app/algorithms/bst.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Optional, List

@dataclass
class _BSTNode:
    key: Any
    value: Any
    left: Optional["_BSTNode"] = None
    right: Optional["_BSTNode"] = None

def bst_insert(root: Optional[_BSTNode], key: Any, value: Any) -> _BSTNode:
    if root is None:
        return _BSTNode(key, value)
    if key < root.key:
        root.left = bst_insert(root.left, key, value)
    elif key > root.key:
        root.right = bst_insert(root.right, key, value)
    else:
        # chave igual: atualiza valor
        root.value = value
    return root

def bst_inorder(root: Optional[_BSTNode]) -> List[Any]:
    out: List[Any] = []
    def _walk(n: Optional[_BSTNode]):
        if not n:
            return
        _walk(n.left)
        out.append(n.value)
        _walk(n.right)
    _walk(root)
    return out

def bst_search(root: Optional[_BSTNode], key: Any) -> Optional[Any]:
    cur = root
    while cur:
        if key == cur.key:
            return cur.value
        cur = cur.left if key < cur.key else cur.right
    return None
