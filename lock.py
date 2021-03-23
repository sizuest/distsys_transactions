import time
from enum import Enum


class LockType(Enum):
    NONE = 0
    READ = 1
    WRITE = 2


class Lock:
    holders = []
    type = LockType.NONE

    def acquire(self, id: int, type: Enum):
        while self.has_conflict(id, type):
            try:
                time.sleep()
            except:
                raise Exception()

        # Hand over
        if len(self.holders) == 0:
            self.holders.append(id)
            self.type = type
        # Share
        elif id not in self.holders:
            self.holders.append(id)
        # Promote
        elif (id in self.holders) and (self.type is not type):
            self.type = type

    def release(self, id: int):
        self.holders.remove(id)

        if len(self.holders):
            self.type = LockType.NONE

    def has_conflict(self, id, type):
        # No active locks
        if self.type is LockType.NONE:
            return False
        # Only read
        elif (self.type is LockType.READ) and (type is LockType.READ):
            return False
        # Promote
        elif (self.type is LockType.READ) and (self.holders.len == 1) and (id in self.holders):
            return False
        # Otherwise
        else:
            return True
