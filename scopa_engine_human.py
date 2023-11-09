from scopa_engine import ScopaEngineBase, Carta


class ScopaEngineHuman(ScopaEngineBase):

    messaggio_inizio = "Contro un uomo una macchina non vincerà mai!"

    def metodo_gioca_carta(self) -> Carta:
        """Sovrascrive il metodo di ScopaEngineBase
        definendo delle modalità di input fatte da un giocatore umano
        """
        carta_in_mano = self.carte_in_mano
        opzioni = [
            (f"{carta[0]}{carta[1]}".lower(), carta)
            for carta in carta_in_mano
        ]

        print("\nLe carte sul tavolo sono:")
        print(self.carte_sul_tavolo)

        print("Scegli la carta che vuoi giocare:")
        simboli_validi = []
        for simbolo, _ in opzioni:
            print(f"\t {simbolo}")
            simboli_validi.append(simbolo)

        while True:
            simbolo_scelto = input(" >> ").strip().lower()
            if simbolo_scelto in simboli_validi:
                indice_simbolo = simboli_validi.index(simbolo_scelto)
                return opzioni[indice_simbolo][1]
            print("\n*** scelta non valida, inserisci di nuovo ***\n")

    def metodo_scegli_presa(self, possibili_prese: list) -> int:
        """Sovrascrive il metodo di ScopaEngineBase
        definendo delle modalità di input fatte da un giocatore umano
        """
        print(f"Con la carta {self.ultima_carta_giocata} Puoi prendere:")

        for n, presa in enumerate(possibili_prese):
            print(f"\t{n} = {presa}")

        while True:
            input_presa = input("\nInserisci il numero della presa cha vuoi fare >> ").strip()
            try:
                input_presa = int(input_presa)
            except Exception:
                pass
            else:
                if 0 <= input_presa < len(possibili_prese):
                    return input_presa
            print("Scelta non valida")
