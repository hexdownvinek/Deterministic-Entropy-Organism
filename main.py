# HexDownVinek :: deterministic entropy organism

import time
import random
import hashlib
import sys

WIDTH = 60
HEIGHT = 20
TICKS = 300
SEED_PHRASE = "hexdownvinek::gmt+11::vine"
VINE = ["░", "▒", "▓", "⠿", "#", "*"]
HEX = "0123456789abcdef"

seed = hashlib.sha256(SEED_PHRASE.encode()).hexdigest()
random.seed(int(seed[:16], 16))
grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
x, y = WIDTH // 2, HEIGHT // 2
chain_hash = seed
trace_log = []

def clear():
    sys.stdout.write("\033[2J\033[H")
    sys.stdout.flush()

def step():
    global x, y, chain_hash

    dx, dy = random.choice([
        (-1,0),(1,0),(0,-1),(0,1),
        (-1,-1),(1,1),(-1,1),(1,-1)
    ])

    x = (x + dx) % WIDTH
    y = (y + dy) % HEIGHT

    char = random.choice(VINE)
    grid[y][x] = char
    event = f"{x},{y},{char},{chain_hash}"
    chain_hash = hashlib.sha256(event.encode()).hexdigest()
    trace_log.append(chain_hash)

def render(tick):
    clear()
    print("HexDownVinek :: Entropy Engine")
    print(f"tick {tick}/{TICKS} | hash {chain_hash[:16]}… | ?????\n")

    for row in grid:
        print("".join(row))

try:
    for t in range(TICKS):
        step()
        render(t)
        time.sleep(0.04)

except KeyboardInterrupt:
    print("\n[!] vine severed by operator")

with open("vine.trace", "w", encoding="utf-8") as f:
    for h in trace_log:
        f.write(h + "\n")

with open("vine.snapshot.txt", "w", encoding="utf-8") as f:
    for row in grid:
        f.write("".join(row) + "\n")

print("\n[+] entropy chain written to vine.trace")
print("[+] final organism snapshot written to vine.snapshot.txt")
print("[+] deterministic seed:", seed[:32])
