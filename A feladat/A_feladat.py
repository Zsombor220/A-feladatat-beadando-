from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional


# ----- Absztrakt alaposztaly -----
class Auto(ABC):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int):
        self.rendszam = rendszam
        self.tipus = tipus
        self.berleti_dij = berleti_dij

    @abstractmethod
    def info(self):
        pass


# ----- Szemelyauto -----
class Szemelyauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, utasok_szama: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.utasok_szama = utasok_szama

    def info(self):
        return (f"Szemelyauto | Rendszam: {self.rendszam} | Tipus: {self.tipus} | "
                f"Dij: {self.berleti_dij} Ft | Utasok szama: {self.utasok_szama}")


# ----- Teherauto -----
class Teherauto(Auto):
    def __init__(self, rendszam: str, tipus: str, berleti_dij: int, teherbiras: int):
        super().__init__(rendszam, tipus, berleti_dij)
        self.teherbiras = teherbiras

    def info(self):
        return (f"Teherauto | Rendszam: {self.rendszam} | Tipus: {self.tipus} | "
                f"Dij: {self.berleti_dij} Ft | Teherbiras: {self.teherbiras} kg")


# ----- Berles -----
class Berles:
    def __init__(self, auto: Auto, datum: date):
        self.auto = auto
        self.datum = datum

    def info(self):
        return f"{self.auto.rendszam} - {self.datum} - {self.auto.berleti_dij} Ft"


# ----- Autokolcsonzo -----
class Autokolcsonzo:
    def __init__(self, nev: str):
        self.nev = nev
        self.autok: List[Auto] = []
        self.berlesek: List[Berles] = []

    def hozzaad_auto(self, auto: Auto):
        self.autok.append(auto)

    def berel_auto(self, rendszam: str, datum: date) -> Optional[int]:
        auto = next((a for a in self.autok if a.rendszam == rendszam), None)
        if not auto:
            print("Hiba: Nincs ilyen auto.")
            return None
        if any(b.auto.rendszam == rendszam and b.datum == datum for b in self.berlesek):
            print("Hiba: Az auto mar foglalt ezen a napon.")
            return None
        self.berlesek.append(Berles(auto, datum))
        return auto.berleti_dij

    def lemond_berles(self, rendszam: str, datum: date) -> bool:
        for b in self.berlesek:
            if b.auto.rendszam == rendszam and b.datum == datum:
                self.berlesek.remove(b)
                return True
        return False

    def listaz_berlesek(self):
        if not self.berlesek:
            print("Nincs aktiv berles.")
        else:
            for b in self.berlesek:
                print(b.info())


# ----- Kezdeti adatok betoltese -----
def kezdo_adatok() -> Autokolcsonzo:
    kolcsonzo = Autokolcsonzo("CityRent")
    a1 = Szemelyauto("ABC123", "Toyota Corolla", 10000, 5)
    a2 = Szemelyauto("DEF456", "Honda Civic", 12000, 5)
    a3 = Teherauto("GHI789", "Ford Transit", 15000, 2000)
    kolcsonzo.hozzaad_auto(a1)
    kolcsonzo.hozzaad_auto(a2)
    kolcsonzo.hozzaad_auto(a3)

    kolcsonzo.berlesek.extend([
        Berles(a1, date(2025, 5, 30)),
        Berles(a2, date(2025, 6, 1)),
        Berles(a3, date(2025, 5, 28)),
        Berles(a1, date(2025, 6, 2)),
    ])

    return kolcsonzo


# ----- Felhasznaloi interface -----
def menu(kolcsonzo: Autokolcsonzo):
    while True:
        print("\n--- AUTOKOLCSONZO RENDSZER ---")
        print("1. Auto berlese")
        print("2. Berles lemondasa")
        print("3. Berlesek listazasa")
        print("4. Kilepes")

        valasz = input("Valasztas: ").strip()

        if valasz == "1":
            rendszam = input("Rendszam: ").strip().upper()
            datum_input = input("Datum (eeee-hh-nn): ")
            try:
                ev, ho, nap = map(int, datum_input.split("-"))
                datum = date(ev, ho, nap)
                ar = kolcsonzo.berel_auto(rendszam, datum)
                if ar is not None:
                    print(f"Berles sikeres. Ar: {ar} Ft")
            except ValueError:
                print("Hibas datumformatum.")

        elif valasz == "2":
            rendszam = input("Rendszam: ").strip().upper()
            datum_input = input("Datum (eeee-hh-nn): ")
            try:
                ev, ho, nap = map(int, datum_input.split("-"))
                datum = date(ev, ho, nap)
                if kolcsonzo.lemond_berles(rendszam, datum):
                    print("Berles sikeresen lemondva.")
                else:
                    print("Nincs ilyen berles.")
            except ValueError:
                print("Hibas datumformatum.")

        elif valasz == "3":
            kolcsonzo.listaz_berlesek()

        elif valasz == "4":
            print("Kilepes...")
            break

        else:
            print("Ervenytelen valasztas.")


# ----- Foprogram -----
if __name__ == "__main__":
    kolcsonzo = kezdo_adatok()
    menu(kolcsonzo)
