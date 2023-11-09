# importo tutte le funzioni
from typing import Any
import libscopa

# importo solo la classe
from scopa_engine import ScopaEngineBase
from scopa_engine_human import ScopaEngineHuman
ENABLE_DEBUG = True

# Creo due istanze di ScopaEngineBase (i giocatrori)
GIOCATORE_UNO = ScopaEngineBase("Computer")
GIOCATORE_DUE = ScopaEngineHuman("Human")

GIOCATORI = [
    GIOCATORE_UNO,
    GIOCATORE_DUE
]

# Creo il mazzo di carte da scopa
MAZZO = libscopa.crea_mazzo_scopa()


def debug(message: Any):
    if ENABLE_DEBUG:
        print("\n * DEBUG:", message)


def giocatore_dice(giocatore, message):
    for n, istanza in enumerate(GIOCATORI):
        if istanza is giocatore:
            print(f"Giocatore {n+1}: {message}")
            break


def avversario_del_giocatore(giocatore):
    return GIOCATORE_DUE if giocatore is GIOCATORE_UNO else GIOCATORE_UNO


def gioca():
    """Avvia una partita tra i due giocatori.
    """

    # todo fix per continuare a giocare, ma poi ricreare il mazz
    global MAZZO
    MAZZO = libscopa.crea_mazzo_scopa()

    print(" MAZZO >> ", MAZZO)

    ultima_presa_di = None

    libscopa.mescola_mazzo(MAZZO)

    debug(MAZZO)

    carte_sul_tavolo = []

    info_giocatori = {
        giocatore: {
            'nome': f"Player {giocatore+1}",
            'engine': GIOCATORI[giocatore],
            'carte_prese': [],
            'numero_scope': 0
        } for giocatore in [
            libscopa.GIOCATORE_1,
            libscopa.GIOCATORE_2
        ]
    }

    for k, v in info_giocatori.items():
        debug(f"{k}={v}")

    # metto le carte sul tavolo
    for _ in range(4):
        carta = libscopa.prendi_carta_dal_mazzo(MAZZO)
        carte_sul_tavolo.append(carta)

    debug(f"\nSmazzata {carte_sul_tavolo}")

    # Inizializzo i giocatori
    for giocatore in GIOCATORI:
        debug(f"\n Avvio {giocatore.nome}")
        # dico al giocatore che la partita è iniziata
        messaggio = giocatore.inizia_partita()
        giocatore_dice(giocatore, messaggio)

        # dico al giocatore quali sono le carte sul tavolo
        giocatore.info_smazzata(carte_sul_tavolo)

    numero_mano = 0
    while len(MAZZO) > 0:
        numero_mano += 1

        debug(f"\nNumero_mano {numero_mano}")

        # do tre carte ai giocatori
        for giocatore in GIOCATORI:
            debug(f"\nDistribuisco carte a giocatore {giocatore.nome}")
            for _ in range(3):
                carta = libscopa.prendi_carta_dal_mazzo(MAZZO)
                giocatore.prendi_carta(carta)

        # faccio giocare le carte che hanno in mano
        for _ in range(3):
            for giocatore in GIOCATORI:

                carta_giocata = giocatore.gioca_carta()

                opzioni_di_presa = libscopa.trova_possibili_prese(
                    carta_giocata,
                    carte_sul_tavolo
                )
                debug(f"Possibili prese {opzioni_di_presa}")
                if opzioni_di_presa:

                    indice_presa = giocatore.scegli_presa(opzioni_di_presa)
                    carte_prese_dal_giocatore = opzioni_di_presa[indice_presa]

                    for carta_presa in carte_prese_dal_giocatore:
                        carte_sul_tavolo.remove(carta_presa)

                    # todo assengare le prese ai giocatori
                    # todo assegnare eventuale scopa
                    ultima_presa_di = giocatore

                else:
                    carte_prese_dal_giocatore = None
                    carte_sul_tavolo.append(carta_giocata)

                avversario = avversario_del_giocatore(giocatore)

                avversario.info_mossa_avversario(
                    carta_giocata,
                    carte_prese_dal_giocatore
                )

        debug(f"Carte sul tavolo: {carte_sul_tavolo}")

    if carte_sul_tavolo:
        # assegno le carte rimanenti al giocatore che ha fatto l'ultima presa
        ultima_presa_di.prendi_carte_rimanenti(carte_sul_tavolo)
        # inform l'avversario della presa
        avversario_del_giocatore(ultima_presa_di).info_carte_rimanenti_ad_avversario(carte_sul_tavolo)

    # diciamo ai giocatori che la partita è finita
    for giocatore in GIOCATORI:
        giocatore.fine_partita()

    debug("Partita finita")

    # ricreo il mazzo iniziale
    libscopa.rimetti_carte_nel_mazzo(MAZZO, carte_sul_tavolo)


# avvia partita
if __name__ == '__main__':
    # for x in range(1):
    gioca()
