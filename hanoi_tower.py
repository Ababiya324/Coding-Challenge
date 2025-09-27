def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from {source} to {target}")
        return
    # Move n-1 disks from source to auxiliary using target as helper
    hanoi(n - 1, source, auxiliary, target)
    
    # Move the nth disk from source to target
    print(f"Move disk {n} from {source} to {target}")
    
    # Move n-1 disks from auxiliary to target using source as helper
    hanoi(n - 1, auxiliary, target, source)
