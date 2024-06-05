from memory.Memory import Memory

memory = Memory()
memory.access(3)
memory.access(5)

print(memory.memory[3].get_right_blast_radius_impacts())