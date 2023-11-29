# accepted on codewars.com


class MemoryManager:
    def __init__(self, memory):
        """
        @constructor Creates a new memory manager for the provided array.
        @param {memory} An array to use as the backing memory.
        """
        self.memory = memory
        self.allocated_blocks = {}
        self.allocated_blocks_cells = set()

    def allocate(self, size: int) -> int:
        """
        Allocates a block of memory of requested size.
        @param {number} size - The size of the block to allocate.
        @returns {number} A pointer which is the index of the first location in the allocated block.
        @raises If it is not possible to allocate a block of the requested size.
        """
        start_ind = None
        i = 0
        while i < len(self.memory):
            temp_ind = i
            while i < len(self.memory) and i not in self.allocated_blocks_cells and i - temp_ind < size:
                i += 1
            if i - temp_ind == size:
                start_ind = temp_ind
                break
            i += 1
        if start_ind is None:
            raise ValueError(f'Cannot allocate the memory of a size: {size}!')
        # updating the structures:
        self.allocated_blocks[start_ind] = size
        self.allocated_blocks_cells |= {i for i in range(start_ind, start_ind + size)}
        # returning the starting position of the memory block allocated:
        return start_ind

    def release(self, pointer: int):
        """
        Releases a previously allocated block of memory.
        @param {number} pointer - The pointer to the block to release.
        @raises If the pointer does not point to an allocated block.
        """
        # checks for the exception:
        if pointer not in self.allocated_blocks.keys():
            raise ValueError(f'The pointer does not point to an allocated block!')
        # releasing the memory clock:
        self.allocated_blocks_cells -= {i for i in range(pointer, pointer + self.allocated_blocks[pointer])}
        del self.allocated_blocks[pointer]

    def read(self, pointer: int):
        """
        Reads the value at the location identified by pointer
        @param {number} pointer - The location to read.
        @returns {number} The value at that location.
        @raises If pointer is in unallocated memory.
        """
        # checks for the exception:
        if pointer not in self.allocated_blocks_cells:
            raise ValueError(f'The pointer is in unallocated memory!')
        # reading:
        return self.memory[pointer]

    def write(self, pointer: int, value: int):
        """
        Writes a value to the location identified by pointer
        @param {number} pointer - The location to write to.
        @param {number} value - The value to write.
        @raises If pointer is in unallocated memory.
        """
        # checks for the exception:
        if pointer not in self.allocated_blocks_cells:
            raise ValueError(f'The pointer is in unallocated memory!')
        # writing:
        self.memory[pointer] = value





