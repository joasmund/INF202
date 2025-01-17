from collections import defaultdict

LEN = 100_000_000

def example_gen(len):
    return (x*x for x in range(len))

ex = example_gen(LEN)

for i in range(LEN):
    print(next(ex))
