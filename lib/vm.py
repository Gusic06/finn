from random import randint

MAX_MEMORY: int = 1048576 # megabyte of memory

class VM:

    def __init__(self) -> None:
        self.memory: int = MAX_MEMORY
        self.addresses: list[hex] = [ hex(i) for i in range(1, 2**20 + 1) ]
        self.memory_array: dict[hex, int|None] = { hex(i) : None for i in range (1, 2**20 + 1) } # 2**20 + 1
        self.variable_pointers: dict[str, int] = {}

    def assign_variable_to_address(self, variable_name: str, address: hex) -> None:
        self.variable_pointers[variable_name] = address

    def allocate_memory_and_store(self, amount_of_memory: int, value: any) -> None:
        self.memory -= amount_of_memory
        if self.memory < 0:
            print(f"you fucked up buddy")
            exit(1)
        else:
            memory_address: hex = hex(randint(0, 2**20))
            if memory_address not in self.addresses:
                while memory_address not in self.addresses:
                    memory_address = hex(randint(0, 2**20))
            self.addresses.remove(memory_address)
            self.memory_array[memory_address] = [amount_of_memory, value]
            return memory_address

    def assign_memory(self, amount_of_memory: int) -> hex:
        """
        deprecated trash, do not use
        """
        self.memory -= amount_of_memory
        if self.memory < 0:
            print(f"MemoryError: Tried to allocate {amount_of_memory} bytes with {self.memory + amount_of_memory} bytes available ({self.memory} byte diff)")
            exit(1)
        else:
            memory_address: hex = hex(randint(0, 2**20))
            if memory_address not in self.addresses:
                while memory_address not in self.addresses:
                    memory_address = hex(randint(0, 2**20))
            self.addresses.remove(memory_address)
            self.memory_array[memory_address] = [amount_of_memory, None]
            return memory_address

    def free_memory(self, memory_address: hex) -> None:
        if self.memory_array[memory_address] == None:
            return
        self.memory += self.memory_array[memory_address][0]
        self.copy = list(self.variable_pointers.items())
        for address in self.copy:
            if address[1] == memory_address: del self.variable_pointers[address[0]]
        self.addresses.append(memory_address)
        self.memory_array[memory_address] = None

    def print_total_used_memory(self) -> None:
        memory_used: int = MAX_MEMORY - self.memory
        if memory_used == 0:
            print("Total Memory Used: 0 bytes")
        else:
            print(f"Total Memory Used: {memory_used} bytes\n    at addresses:")
            for address in self.memory_array.items():
                if self.memory_array[address[0]] != None:
                    padding: int = 12 - (len(str(address[1][0])) + len(address[0]))
                    if address[0] in self.variable_pointers.values():
                        for variable in self.variable_pointers.items():
                            if variable[1] == address[0]:
                                print(f"        {address[0]} -> {address[1][0]} bytes {' ' * padding}| ({variable[0]})")
                    else:
                        print(f"        {address[0]} -> {address[1][0]} bytes {' ' * padding}|")
        print("\n")
