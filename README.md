# Gioco della scopa

**Questo progetto è stato sviluppato durante un corso per FullStack developers che ho tenuto nel 2022 per introdurre le classi ed ereditarietà. Dato lo scopo puramente didattico si è scelto di utilizzare una nomenclatura delle variabili e dei metodi in lingua italiana.**


Scopo del progetto:
 
 - creare una classe giocatore base di un giocatore di scopa (scopa_engine.py) e definire i metodi di gioco.
 - creare un orchestrator per permettere a 2 giocatori di sfidarsi (gioca_partita.py).
 - sviluppare classi di giocatori con strategie migliori rispetto la classe base.


# Orchestrator

L'orchestrator (gioca_partita.py) si occupa di:

- Creare, mescolare e distribuire le carte sul tavolo e ai giocatori.
- Chiedere a turno a un giocatore quale carta vuole giocare ed eventualmente quale presa effettuare nel caso siano possibili prese diverse.
- Informare un giocatore sulla giocata dell'avversario.

In questa implementazione l'orchestrator non tiene conto del punteggio che invece viene calcolato direttamente dai giocatori a fine della partita.

# Classe giocatore base

La classe giocatore base (scopa_engine.py) definisce i metodi di comunicazione tra orchestrator e giocatore mentre la strategia di gioco è casuale.

## Metodi principali per la comunicazione con l'orchestrator (da non sovrascivere):

- inizia_partita() -> None: permette di inizializzare le variabili di gioco
- fine_partita() -> str: calcola il punteggio sia del giocatore che dell'avversario per stabilire chi ha vinto e restituisce un messaggio sulla base del risultato.
- prendi_carta(carta) -> None: permette al giocatore di ricevere una carta dal mazziere / orchestrator.
- gioca_carta() -> carta: chiede al giocatore di giocare un carta tra quelle in suo possesso.
- scegli_presa(possibili_prese) -> int: permettere al giocatore, quando con una carta giocata sono possibili più prese, di indicare quale presa si preferisce fare.
- prendi_carte_rimanenti(carte) -> None: permette al giocatore di raccogliere le carte rimaste sul tavolo a fine partita.
- info_carte_rimanenti_ad_avversario(carte) -> None: informa il giocatore sulle carte rimaste sul tavolo prese dall'avversario.
- info_mossa_avversario(carta_giocata, carte_prese): informa il giocatore sulla carta giocata dall'avversario e sulle carte prese dal tavolo.

## Metodi con logiche di scelta (sovrascrivili):

- metodo_gioca_carta() -> carta: definisce la logica di scelta della carta da giocare (in questo caso casuale).
- metodo_scegli_presa(possibili_prese) -> int: definisce la logica di scelta sulle carte da prendere dal tavolo in caso siano possibili piu' opzioni di presa (in questo caso casuale).



# Classi giocatori avanzate

Definita la classe giocatore base è possibile creare altri modelli di giocatore ridefinendo semplicemente i metodi:

- metodo_gioca_carta()
- metodo_scegli_presa(possibili_prese)

Ogni classe giocatore può anche personalizzare i vari messaggi di gioco come:

- messaggio_inizio
- messaggio_fine_vittoria
- messaggio_fine_sconfitta
- messaggio_fine_pareggio


# NOTA

Data la complessità del progetto per il livello dei partecipanti al corso
non sono state create classi di giocatori 'intelligenti' che potessero sfidarsi tra loro
tuttavia è stata creata una classe (scopa_engine_human.py) per permettere a un umano di giocare 
 semplicemente sostituendo la scelta casuale della classe base con richieste di input utente.


