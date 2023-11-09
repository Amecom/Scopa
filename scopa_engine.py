import random
from typing import Optional
import libscopa

Carta = libscopa.Carta


class ScopaEngineBase:

    # assegnato qui perchè non cambio tra le istanze
    messaggio_inizio = "Sono pronto a vincere!"

    # assegnato qui perchè personalizzabile dall'istanze
    # a seconda del risultato della partita
    messaggio_fine_vittoria = "Vittoria stracciante!"
    messaggio_fine_sconfitta = "Sconfitta immeritata!"
    messaggio_fine_pareggio = "Pareggio fortunato (per te)"

    is_log_enabled = True

    def __init__(self, nome) -> None:

        # nome del giocatore
        self.nome = nome

        # le carte che posso giocare
        self.carte_in_mano = []

        # le carte che sosso prendere
        self.carte_sul_tavolo = []

        # lista delle carte prese
        self.carte_prese = []

        # Contatore della mano in corso della partita da 1 a 6
        # usato per eccezione ultima scopa
        self.numero_mano = 0

        # conta le scope che ho fatto
        self.numero_scope = 0

        # booleano che indica se sono il primo giocatore
        # utilizzato per la regola per eccezione scopa ultima mano
        self.sto_giocondo_per_primo = None

        # mi serve per gestire le prese e rimuovere la carta dal tavolo
        self.ultima_carta_giocata = None

        # informazioni sull'avversario
        self.avversario_carte_prese = []
        self.avversario_numero_scope = 0

    # METODI INTERFACCIA COMUNE

    def inizia_partita(self) -> str:
        """Reimposta i valori delle variabili interne.
        """
        self.carte_in_mano.clear()
        self.carte_sul_tavolo.clear()
        self.carte_prese.clear()
        self.numero_mano = 0
        self.numero_scope = 0
        self.sto_giocondo_per_primo = None
        self.ultima_carta_giocata = None
        self.avversario_carte_prese.clear()
        self.avversario_numero_scope = 0
        return self.messaggio_inizio

    def fine_partita(self) -> str:
        """Metodo chiamato a fine partita che calcola il punteggio
        ottenuto da me e dall'avversario.

        Restituisce un messaggio.
        """
        punti_miei, punti_avversario = libscopa.analisi_punteggio(
            self.carte_prese,
            self.avversario_carte_prese
        )
        punti_miei += self.numero_scope
        punti_avversario += self.avversario_numero_scope

        print(f"\nMie carte prese: {self.carte_prese}")
        print(f"Mio punteggio: {punti_miei} - ({self.numero_scope} scope)")
        print(f"\nAvversario carte: {self.avversario_carte_prese} - ({self.avversario_numero_scope} scope)")
        print(f"Avversario punteggio: {punti_avversario}")
        print(f"\nCarte ancora sul tavolo: {len(self.carte_sul_tavolo)}")
        print(f"TOTALE CARTE: {len(self.carte_prese + self.avversario_carte_prese)}")

        if punti_miei == punti_avversario:
            messaggio = self.messaggio_fine_pareggio

        elif punti_miei > punti_avversario:
            messaggio = self.messaggio_fine_vittoria

        else:
            messaggio = self.messaggio_fine_sconfitta

        return messaggio

    def prendi_carta(self, carta: Carta) -> None:
        """Riceve una carta dal mazziere e la memorizza per uso interno.
        """
        if len(self.carte_in_mano) == 3:
            raise Exception("Ho già tre carte in mano!")
        self.carte_in_mano.append(carta)
        # ogni tre carte ricevute inizia una nuova mano
        if len(self.carte_in_mano) == 3:
            self.numero_mano += 1

    def gioca_carta(self) -> Carta:
        """Restituisce una carta tra quelle che si hanno in mano.
        """
        # verifica di eccezione del gioco
        numero_carte_in_mano = len(self.carte_in_mano)
        if numero_carte_in_mano == 0:
            raise Exception("Non ho carte in mano!")

        # controlo fatto solo la prima volta per determinare
        # se sono il primo di mano, si basa sul fatto che le carte sul tavolo
        # sono 4 solo all'inizio (per il secono saraano di più o di meno in caso di presa)
        if self.sto_giocondo_per_primo is None:
            self.sto_giocondo_per_primo = len(self.carte_sul_tavolo) == libscopa.CARTE_SUL_TAVOLO_SMAZZATA

        carta_da_giocare = self.metodo_gioca_carta()

        indice_carta = self.carte_in_mano.index(carta_da_giocare)
        self.carte_in_mano.pop(indice_carta)

        self._log(f"Gioco la carta {carta_da_giocare}")

        # mi serve per sapere quale carte rimuovere in caso di presa
        self.ultima_carta_giocata = carta_da_giocare

        # dato che non so ancora se ci sono prese considero la carta sul tavolo
        # poi la rimuovo in caso di presa in 'scegli presa'
        self._aggiungi_carta_sul_tavolo(carta_da_giocare)

        return carta_da_giocare

    def scegli_presa(self, possibili_prese: tuple) -> int:
        """Scegli presa viene chiamato solo quando c'è la possibilità di almeno una presa,
        anche se ce ne è una sola.
        
        ESEMPIO della lista 'possibili_prese'
        Gioco un (7, 'B'), 
        a terra ci sono [(5, 'C'), (2, 'B'), (4, 'D') , (3, 'C')]
        Possibili_prese:
        [
            [(5, 'C'), (2, 'B')],
            [(4, 'D'), (3, 'C')]
        ]

        Risposta sarà 0 oppure 1 (indice della presa scelta)
        """

        if len(possibili_prese) == 1:
            indice_presa_scelta = 0
        else:
            indice_presa_scelta = self.metodo_scegli_presa(possibili_prese)

        # rimuovo dal tavolo le carte prese
        carte_prese = list(possibili_prese[indice_presa_scelta])

        # rimuovo dal tavolo l'ultima carta giocata
        carte_prese.append(self.ultima_carta_giocata)

        self._log(f"Eseguo presa {carte_prese}")

        for carta in carte_prese:
            self._rimuovi_carta_sul_tavolo(carta)
            self.carte_prese.append(carta)

        if not self.carte_sul_tavolo:
            # regola eccezione per impedire la scopa di ultima mano
            annulla_scopa = all([
                not self.sto_giocondo_per_primo,
                self.numero_mano == libscopa.NUMERO_ULTIMA_MANO,
                not self.carte_in_mano
            ])

            if not annulla_scopa:
                self.numero_scope += 1

        # restituisco l'indice scelto
        self._log(f"Invio scelta di presa numero {indice_presa_scelta}")
        return indice_presa_scelta

    def prendi_carte_rimanenti(self, carte: list[Carta]) -> None:
        """Carte assegnate in caso di ultima presa nell'ultima mano.
        """
        for carta in carte:
            self.carte_sul_tavolo.remove(carta)
            self.carte_prese.append(carta)

    def info_smazzata(self, carte: list[Carta]) -> None:
        """Serve per conoscere la carte messe sul tavolo a inizio partita.

        Questa info viene data una volta sola, sarà compito del engine
        aggiornare le carte sul tavolo a seconda delle prese.
        """
        # decido di fare un ciclo perchè dovrò
        # eseguire più operazioni selle carte
        for carta in carte:
            self._aggiungi_carta_sul_tavolo(carta)

    def info_carte_rimanenti_ad_avversario(self, carte: list[Carta]) -> None:
        for carta in carte:
            self.carte_sul_tavolo.remove(carta)
            self.avversario_carte_prese.append(carta)

    def info_mossa_avversario(self, carta_giocata: Carta, carte_prese: Optional[list[Carta]]) -> None:
        self._log(f"Segno che l'avversiario con {carta_giocata} prende {carte_prese}")
        if carte_prese:
            for carta in carte_prese:
                # rimuovo le carte prese dal tavolo
                self._rimuovi_carta_sul_tavolo(carta)
                # assegno la carta tre le prese dell'avversario
                self.avversario_carte_prese.append(carta)

            # devo aggiungere anche la carta giocate
            # tra le prese dell'avversario
            self.avversario_carte_prese.append(carta_giocata)

            # aasegno la scopa all'avversario
            if not self.carte_sul_tavolo:
                # regola eccezione per impedire la scopa di ultima mano
                annulla_scopa = all([
                    self.sto_giocondo_per_primo,
                    self.numero_mano == libscopa.NUMERO_ULTIMA_MANO,
                    not self.carte_in_mano
                ])

                if not annulla_scopa:
                    self.avversario_numero_scope += 1

        else:
            # non avendo preso la carta giocata finisce sul tavolo
            self._aggiungi_carta_sul_tavolo(carta_giocata)

    # METODI SOVRASCRIVIBILI DI BASE

    def metodo_gioca_carta(self) -> Carta:
        """Metodo semplificato per selezionare la carta da giocare
        che può essere sovrascritto.
        Tenere la logica più semplice possibile,
        restituirà una carta tra le carte_in_mano
        """

        """
        combo = libscopa.crea_combinazioni_carte(carte_sul_tavolo)
        punteggi = []
        for n, carta in enumerate(carte_in_mano):
            punteggi[n] = max([
                len(presa)
                for presa in trova_possibili_prese(carta, cartetavlolo)
            ])

        """
        # randrange non include il valore di 'numero_carte_in_mano'
        indice_carta = random.randrange(0, len(self.carte_in_mano))
        return self.carte_in_mano[indice_carta]

    # noinspection PyMethodMayBeStatic
    def metodo_scegli_presa(self, possibili_prese: tuple) -> int:
        return random.randrange(0, len(possibili_prese))

    # METODI A USO INTERNO

    def _log(self, messaggio):
        if self.is_log_enabled:
            print(f" * {self.nome}: {messaggio}")

    def _aggiungi_carta_sul_tavolo(self, carta):
        self._log(f"Aggiungo sul tavolo {carta} in {self.carte_sul_tavolo}")
        self.carte_sul_tavolo.append(carta)
        self._log(f"Sul tavolo ora ci sono {self.carte_sul_tavolo}")

    def _rimuovi_carta_sul_tavolo(self, carta):
        self._log(f"Rimuovo dal tavolo {carta} in {self.carte_sul_tavolo}")
        self.carte_sul_tavolo.remove(carta)
        self._log(f"Sul tavolo ora ci sono {self.carte_sul_tavolo}")
