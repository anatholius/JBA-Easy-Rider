types = {'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
hand = []
while len(hand) < 6:
    entry = input()
    hand.append(types[entry] if entry in types.keys() else int(entry))

print(sum(hand) / len(hand))
