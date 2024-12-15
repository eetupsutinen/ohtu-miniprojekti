*** Settings ***
Library   ../ViiteLibrary.py
Library  OperatingSystem
Library  String
Test Timeout  5s

*** Variables ***
${TIEDOSTONIMI}   test.bib

${OHJETEKSTI}     \nKomennot:\n\help\t\ttulostaa tämän viestin\n\exit\t\tpoistuu ohjelmasta\n\avaa\t\tavaa bib-tiedoston\n\luo\t\tluo bib-tiedoston\ntulosta\t\ttulostaa aktiivisen bib-tiedoston sisällön\n\syota\t\ttallentaa bib-dataa aktiiviseen bib-tiedostoon\n\muokkaa\t\tmuokkaa valitun viitteen parametreja\n\muokkaaparam\tmuokkaa valitun viitteen haluttua parametria\n\lisaatagi\tlisää halutun tagin\n\poistatagi\tpoistaa halutun tagin\n\


*** Test Cases ***
Help Tulostuu Ohjelman Alkuun
    Nayta Alkutekstit
    Output Should Contain   ${OHJETEKSTI}

Testaa Help Komento
    Syota Komento  help
    Output Should Contain  ${OHJETEKSTI}
