import sys

pCount = int(sys.argv[1])
pLevel = float(sys.argv[2])
mCount = int(sys.argv[3])
mLevel = float(sys.argv[4])

total = pCount + pLevel + mCount + mLevel

print('Hello from Python! %(total)s' % { 'total': total })