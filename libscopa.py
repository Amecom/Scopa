import random
import itertools

# Definisco una carta come:
# intero (numero della carta), str: seme della carta 
Carta = tuple[int, str]

SEME_DENARI = "D"
SEME_BASTONI = "B"
SEME_COPPE = "C"
SEME_SPADE = "S"

SEMI = (SEME_DENARI, SEME_BASTONI, SEME_COPPE, SEME_SPADE)
NUMERO_CARTE_PER_SEME = 10
NUMERO_GIOCATORI = 2

# numero fisso con due giocatori
NUMERO_ULTIMA_MANO = 6
CARTE_SUL_TAVOLO_SMAZZATA = 4

GIOCATORE_1 = 0
GIOCATORE_2 = 1

TABELLA_PRIMIERA = (
    (7, 21),
    (6, 18),
    (1, 16),
    (5, 15),
    (4, 14),
    (3, 13),
    (2, 12),
    (8, 10),
    (9, 10),
    (10, 10)
)


def crea_mazzo(semi: tuple, ncarte: int) -> list[Carta]:
    """Restituisce un mazzo dati semi e numero di carte.

    ... Descrizione dettagliata ...
    """
    mazzo = []
    for seme in semi:
        for x in range(1, ncarte + 1):
            mazzo.append((x, seme))
    return mazzo


def crea_mazzo_scopa() -> list[Carta]:
    return crea_mazzo(SEMI, NUMERO_CARTE_PER_SEME)


def mescola_mazzo(mazzo: list[Carta]) -> None:
    """Mescola il mazzo in entrata modificando l'ordine.

    Non crea un nuovo mazzo ma mofica l'ordine degli elementi del mazzo stesso.
    """
    mazzo.sort(key=lambda e: random.random())


def distribuisci_carte_a_caso(mazzo: list[Carta], n_giocatori: int) -> list:
    """Distribuisce le carte a n giocatori per simulare un conteggio punti
    senza giocare una partita.
    """
    giocatori = [[] for _ in range(n_giocatori)]
    for _ in range(len(mazzo)):
        giocatore = random.choice(giocatori)
        giocatore.append(mazzo.pop())
    return giocatori


def prendi_carta_dal_mazzo(mazzo: list[Carta]) -> Carta:
    """Seleziona la carta in cima al mazzo.

    Utile per distribuire le carte ai giocatori o sul tavolo.
    """
    if len(mazzo) == 0:
        raise Exception("Non ci sono più carte nel mazzo!")
    return mazzo.pop(0)


def rimetti_carte_nel_mazzo(mazzo: list[Carta], carte: list[Carta]) -> None:
    """Modifica sul posto il mazzo inserendo le carte passate.

    Utile a riconstruire un mazzo dopo una partita.
    """
    mazzo.extend(carte)


# ************************* ANALISI DEI PUNTI *************************

def solo_carte_di_un_seme(carte: list[Carta], seme: str) -> list[int]:
    """Restituisce un sottoinsieme delle carte per seme.

    Il sottoinsieme è una lista con i soli numeri delle carte (senza il seme)
    """
    return [carta_numero for carta_numero, carta_seme in carte if carta_seme == seme]


def insieme_carte(carte: list[Carta]) -> list[Carta]:
    """Restituisce l'insieme di tutte le carte.`
    
    Utile nell'assegnare il punto per chi ha più carte.
    """
    return carte


def insieme_denari(carte: list[Carta]) -> list[int]:
    return solo_carte_di_un_seme(carte, SEME_DENARI)


def insieme_settebello(carte: list[Carta]) -> list[int]:
    return [7] if 7 in insieme_denari(carte) else []


def insieme_primiera(carte: list[Carta]) -> list:
    punti_totali = []
    for seme in SEMI:
        carte_del_seme = solo_carte_di_un_seme(carte, seme)
        for numero_carta, punti_carta in TABELLA_PRIMIERA:
            if numero_carta in carte_del_seme:
                for _ in range(punti_carta):
                    # appendo la carte che mi ha assegnato il punto
                    # tante volte quanti sono i punti che mi ha assegnato
                    punti_totali.append((numero_carta, seme))
                break
        else:
            # regola per cui se non ho una carte di un seme, non posso vincere la primiera
            punti_totali.clear()
            break

    return punti_totali


def analisi_punteggio(carte_giocatore_uno: list[Carta], carte_giocatore_due: list[Carta]) -> list[int]:
    """
        'numero_carte': ...,
        'numero_denari': ...,
        'ha_settebello': ...,
        'punti_primiera': ...,
    """
    punti = [0, 0]

    funzioni_di_punteggio = [
        insieme_carte,
        insieme_denari,
        insieme_settebello,
        insieme_primiera
    ]

    for funzione in funzioni_di_punteggio:
        nome_funzione = funzione.__name__
        carte_g1 = len(funzione(carte_giocatore_uno))
        carte_g2 = len(funzione(carte_giocatore_due))

        if carte_g1 != carte_g2:
            vincitore = GIOCATORE_1 if carte_g1 > carte_g2 else GIOCATORE_2
            print(f"{nome_funzione}: Giocatore {vincitore+1} (G1:{carte_g1} G2:{carte_g2})")
            punti[vincitore] += 1
        else:
            print(f"{nome_funzione}: Pareggio")

    return punti


def crea_combinazioni_carte(carte):
    """Restituisce tutte le possibili associazioni
    tra le carte passate.
    """
    carte_combinate = []
    for i in range(1, len(carte) + 1):
        for j in itertools.combinations(carte, i):
            carte_combinate.append(j)
    return carte_combinate


def trova_possibili_prese(carta_in_mano, carte_sul_tavolo):
    """Restituisce le possibili prese
    che carta può fare all'interno di carte
    """
    print(" ~~ carte_sul_tavolo", carte_sul_tavolo)
    numero_carta_in_mano = carta_in_mano[0]
    # riduco le carte da combinare rimuovendo quell che non potrebbero
    # mai essere prese perchè di valore superiore a quelle cha ho in mano
    carte_possibili = [
        carta
        for carta in carte_sul_tavolo
        if carta[0] <= numero_carta_in_mano
    ]
    print(" ~~ carte_possibili", carte_possibili)

    carte_combinate = crea_combinazioni_carte(carte_possibili)
    print(" ~~ carte_combinate", carte_combinate)
    # opzioni = [carte for carte in carte_combinate if sum(n for n, _ in carte) == numero ]
    opzioni = []
    for carte in carte_combinate:
        # sommo tutti numeri delle carte della combinazione
        # se il valore `uguale a 'numero' allora è una presa valida
        if sum([n for n, _ in carte]) == numero_carta_in_mano:
            opzioni.append(carte)

    # REGOLA dice che se tra le carte è presente una carta
    # uguale allora è l'unica presa valida (non carte combinate)
    print(" ~~ opzioni MATEMATICHE: ", opzioni)
    if opzioni:
        opzioni_singole = [
            opzione
            for opzione in opzioni
            if len(opzione) == 1
        ]
        if opzioni_singole:
            print(" ~~ uso opzioni singole")
            opzioni = opzioni_singole
    print(" ~~ trova_possibili_prese", carta_in_mano, carte_sul_tavolo)
    print(" ~~ opzioni FINALI: ", opzioni)
    return opzioni


def main():
    print("Ciao sono la libscopa")
    x = crea_combinazioni_carte([(3, 'C'), (4, 'C'), (9, 'X')])
    print(x)


if __name__ == "__main__":
    main()
