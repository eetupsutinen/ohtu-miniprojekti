import os
from pathlib import Path
from viite_parseri import ViiteParseri

class ViiteEditori:
    def __init__(self, io):
        self.io = io
        self.aktiivinen_tiedosto = None

    def run(self):
        '''Käynnistää sovelluksen ja kysyy komennon.'''
        tiedostonimi = None
        self.helppi()
        while True:
            # Luetaan käyttäjältä syötettä, kunnes annetaan exit-komento
            syote_raaka = self.io.lue("Syötä komento. (Listaa komennot syöttämällä help.) > ")
            # strip poistaa whitespacen, joten ylimääräiset välilyönnit eivät haittaa
            syote = syote_raaka.strip()
            if syote == "help":
                self.helppi()

            elif syote == "exit":
                break

            elif syote == "avaa":
                tiedostonimi = self.io.lue("Anna avattava tiedosto muodossa sijainti/nimi: ")
                self.avaa_tiedosto(tiedostonimi)

            elif syote == "luo":
                tiedostonimi = self.io.lue("Anna luotava tiedoston polku/nimi (suhteessa työhakemistoon): ")
                self.luo_ja_avaa_tiedosto(tiedostonimi)

            elif syote == "tulosta":
                self.tulosta_tiedosto()

            elif syote == "syota":
                self.syota_bib_viite()

            elif syote == "muokkaa":
                viitteen_avain = self.io.lue("Anna muokattan viitteen avain: ")
                parametrin_tyyppi = self.io.lue("Anna parametrin tyyppi: ")
                muokattu_parametri = self.io.lue("Anna muokattu parametri: ")
                self.muokkaa_tiedosto(viitteen_avain, parametrin_tyyppi, muokattu_parametri)
            else:
                if syote == "":
                    continue
                self.io.kirjoita("Tuntematon komento \""+syote+"\"")


    def helppi(self):
        self.io.kirjoita("\nKomennot:\n\
help\t\ttulostaa tämän viestin\n\
exit\t\tpoistuu ohjelmasta\n\
avaa\t\tavaa bib-tiedoston\n\
luo\t\tluo bib-tiedoston\n\
tulosta\t\ttulostaa aktiivisen bib-tiedoston sisällön\n\
syota\t\ttallentaa bib-dataa aktiiviseen bib-tiedostoon\n\
muokkaa\t\tmuokkaa valitun viitteen haluttua parametria\n\
")
        return 0
    def avaa_tiedosto(self, tiedostonimi):
        '''Avaa tiedoston sovelluksen käsiteltäväksi.'''
        tiedosto = None
        if not tiedostonimi.strip().endswith(".bib"):
            tiedostonimi = tiedostonimi + ".bib"
        if Path(tiedostonimi).is_absolute():
            polku = tiedostonimi
        else:
            tyohakemisto_str = os.path.abspath(os.getcwd())
            tyohakemisto_polku = Path(tyohakemisto_str)
            tiedostonimi_polku = Path(tiedostonimi)
            polku = tyohakemisto_polku / tiedostonimi_polku
        try:
            # Avaa tiedoston read/write tilassa tai I/O error, jos tiedostoa ei löydy
            with open(polku, "r+") as tiedosto:
                self.aktiivinen_tiedosto = polku
                self.io.kirjoita("Avattiin tiedosto: "+str(polku))
        except IOError:
            self.io.kirjoita("Tapahtui virhe: Tiedostoa "+str(polku)+" ei löynyt.")
        finally:
            # Suljetaan tiedosto lopulta (vaikka tapahtuisi virhe)
            if tiedosto is not None:
                tiedosto.close()

    def luo_ja_avaa_tiedosto(self, tiedostonimi):
        '''Luo uuden .bib-tiedoston ja avaa sen sovelluksen käsiteltäväksi.'''
        tiedosto = None
        if not tiedostonimi.strip().endswith(".bib"):
            tiedostonimi = tiedostonimi + ".bib"
        if Path(tiedostonimi).is_absolute():
            polku = tiedostonimi
        else:
            tyohakemisto_str = os.path.abspath(os.getcwd())
            tyohakemisto_polku = Path(tyohakemisto_str)
            tiedostonimi_polku = Path(tiedostonimi)
            polku = tyohakemisto_polku / tiedostonimi_polku
        try:
            # Luo ja avaa uuden tiedoston read/write tilassa, antaa errorin, jos tiedosto on jo olemassa
            with open(polku, "x+") as tiedosto:
                self.aktiivinen_tiedosto = polku
                self.io.kirjoita("Luodaan tiedosto sijaintiin: "+str(polku))
        except IOError:
            self.io.kirjoita("Tapahtui virhe: Tiedosto "+str(polku)+" on jo olemassa.")
        finally:
            if tiedosto is not None:
                tiedosto.close()

    def tulosta_tiedosto(self):
        '''Tulostaa avatun tidoston sisällön.(aktiivinen_tiedosto)'''
        if self.aktiivinen_tiedosto is None:
            self.io.kirjoita("Ei avattua tiedostoa. Avaa tiedosto ensin komennolla 'avaa'.")
            return -1

        try:
            with open(self.aktiivinen_tiedosto, "r") as tiedosto:
                sisalto = tiedosto.read()
                self.io.kirjoita(f"Tiedoston {self.aktiivinen_tiedosto.name} sisältö:\n{sisalto}")
                return 0
        except IOError:
            self.io.kirjoita(f"Tapahtui virhe: Tiedostoa {self.aktiivinen_tiedosto} ei voitu lukea.")
            return -1

    def syota_bib_viite(self):
        '''Ottaa käyttäjältä vastaan valmiita viitteitä bib-syntaksissa ja tallentaa aktiiviseen tiedostoon'''
        if self.aktiivinen_tiedosto is None:
            self.io.kirjoita("Ei avattua tiedostoa. Avaa tiedosto ensin komennolla 'avaa'.")
            return -1
        self.io.kirjoita("Syötä lisättävä bib-data. Lopeta syöttö kirjaamalla tyhjälle riville 'valmis'.")
        rivit = []
        while True:
            rivi = self.io.lue("> ").rstrip()
            if rivi == "valmis":
                break
            rivit.append(rivi)

        uusi_data = "\n".join(rivit)

        with open(self.aktiivinen_tiedosto, "r") as tiedosto:
            sisalto = tiedosto.read()

        if not sisalto.endswith("\n"):
            uusi_data = "\n" + uusi_data

        with open(self.aktiivinen_tiedosto, "a") as tiedosto:
            tiedosto.write(uusi_data + "\n\n")

        self.io.kirjoita("Viite lisätty tiedoston loppuun.")
        return 0

    def muokkaa_tiedosto(self, viitteen_avain, parametrin_tyyppi, muokattu_parametri ):
        '''Muokkaa valitun viitteen haluttua parametriä'''
        if self.aktiivinen_tiedosto is None:
            self.io.kirjoita("Ei avattua tiedostoa. Avaa tiedosto ensin komennolla 'avaa'.")
            return -1

        try:
            with open(self.aktiivinen_tiedosto, "r") as tiedosto:
                viite_alku = tiedosto.read()

                tiedoston_viitteet = viite_alku.split('@')[1:]  # Jokainen viite alkaa '@'
                viitteet = ["@" + viite.strip() for viite in tiedoston_viitteet]

            muokattava_viite = None
            for viite in viitteet:
                if viitteen_avain in viite:
                    muokattava_viite = viite
                    break

            if not muokattava_viite:
                self.io.kirjoita(f"Viitettä avaimella '{viitteen_avain}' ei löytynyt.")
                return -1

            parseri = ViiteParseri(muokattava_viite)
            tulos = parseri.muokkaa(parametrin_tyyppi, muokattu_parametri)

            viitteet = [viite if viite != muokattava_viite else str(parseri) for viite in viitteet]

            with open(self.aktiivinen_tiedosto, "w") as tiedosto:
                tiedosto.write("\n\n".join(viitteet))

            if tulos >= 0:
                self.io.kirjoita("Muokkaus onnistui")
            else:
                self.io.kirjoita("Muokkaus epäonnistui tarkista parametrin tyyppi")
            return 0

        except FileNotFoundError:
            print("Tiedostoa ei löytynyt.")
            return -1
