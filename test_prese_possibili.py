import libscopa
import itertools 


def get_all_combinations(elements):
    combos = []
    for i in range(len(elements)):
        for j in itertools.combinations(elements, i):
            combos.append(j)
    return combos


mazzo = libscopa.crea_mazzo_scopa()
libscopa.mescola_mazzo(mazzo)
carte_sul_tavolo = []
for _ in range(13):
    carta = libscopa.prendi_carta_dal_mazzo(mazzo)
    carte_sul_tavolo.append(carta)

carte_combinate = get_all_combinations(carte_sul_tavolo)

for numero, seme in mazzo:
    # voglio sapere con carte 
    # quali prese posso fare sulle carte sul tavolo
    print(f"\n Con la carta numero {numero} e sul tavolo {carte_sul_tavolo} posso prendere:")
    opzioni = []
    for carte in carte_combinate:
        if sum([n for n, _ in carte]) == numero:
            opzioni.append(carte)

    # opzioni = [carte for carte in carte_combinate if sum(n for n, _ in carte) == numero ]

    for opzione in opzioni:
        print(" * ", opzione)



# def f(v, i, S, memo):
#   if i >= len(v):
#       return 1 if S == 0 else 0
#   if (i, S) not in memo:  # <-- Check if value has not been calculated.
#     count = f(v, i + 1, S, memo)
#     count += f(v, i + 1, S - v[i], memo)
#     memo[(i, S)] = count  # <-- Memoize calculated result.
#   return memo[(i, S)]     # <-- Return memoized value.
#
# v = [1, 2, 3, 10]
# somma = 15
# memo = dict()
# print(f(v, 0, somma, memo))
#
# for m in memo.items():
#     print(m)
# raise
