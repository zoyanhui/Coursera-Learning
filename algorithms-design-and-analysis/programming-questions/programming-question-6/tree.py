from collections import deque


class SearchTree():
    def __init__(self):
        self._root = None
        self._array = []
        self._size = 0
        self._size_left = 0
        self._size_right = 0

    def insert(self, value):
        self._bubble_down_(value)
        self._balance_()

    def root(self):
        if self._root:
            return self._root.value
        return None

    def _bubble_down_(self, value):
        cur = self._root
        pre = None
        is_left = True
        if self._root:
            if value < self._root.value:
                self._size_left += 1
            else:
                self._size_right += 1
        while cur:
            pre = cur
            if value < cur.value:
                cur = cur.left
                is_left = True
            else:
                cur = cur.right
                is_left = False
        if not pre:
            self._root = BinaryTreeNode(value)
        else:
            if is_left:
                pre.left = BinaryTreeNode(value)
            else:
                pre.right = BinaryTreeNode(value)
        self._size += 1


    def _balance_(self):
        while self._size_left > self._size_right:
            self._rotate_right_()
        while self._size_right > self._size_left + 1:
            self._rotate_left_()

    def _rotate_right_(self):
        old_root = self._root
        new_root = self._find_max_(old_root.left)
        if not new_root:
            return
        self._root = new_root
        if new_root != old_root.left:
            new_root.left = old_root.left
        old_root.left = None
        new_root.right = old_root
        self._size_left -= 1
        self._size_right += 1

    def _rotate_left_(self):
        old_root = self._root
        new_root = self._find_min_(old_root.right)
        if not new_root:
            return
        self._root = new_root
        if new_root != old_root.right:
            new_root.right = old_root.right
        old_root.right = None
        new_root.left = old_root
        self._size_left += 1
        self._size_right -= 1

    def _find_max_(self, node):
        cur = node
        if cur == None:
            return None
        pre = None
        while cur.right != None:
            pre = cur
            cur = cur.right
        if pre != None:
            pre.right = cur.left
        return cur

    def _find_min_(self, node):
        cur = node
        if cur == None:
            return None
        pre = None
        while cur.left != None:
            pre = cur
            cur = cur.left
        if pre != None:
            pre.left = cur.right
        return cur

    def __str__(self):
        queue = deque()
        s = ''
        if self._root:
            queue.append(self._root)
        cur = None
        if queue:
            cur = queue.popleft()
        while cur:
            s += str(cur.value) + ","
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)
            if queue:
                cur = queue.popleft()
            else:
                cur = None
        return s


class BinaryTreeNode():
    def __init__(self, val):
        self.left = None
        self.right = None
        self.value = val

    def __str__(self):
        return str(self.value)
		
		