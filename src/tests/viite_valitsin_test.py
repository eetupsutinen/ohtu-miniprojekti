import unittest
from viite_valitsin import ViiteValitsin

class TestViiteValitsin(unittest.TestCase):

    maxDiff = None

    esimerkkiviitteet = ["""@article{kadiyala2018applications,
title={Applications of python to evaluate the performance of decision tree-based boosting algorithms},
author={Kadiyala, Akhil and Kumar, Ashok},
journal={Environmental Progress & Sustainable Energy},
volume={37},
number={2},
pages={618--623},
year={2018},
publisher={Wiley Online Library}
}""",
"""@article{saabith2019python,
  title   = {Python current trend applications-an overview},
  author  = {Saabith, AS and Fareez, MMM and Vinothraj, T},
  journal = {International Journal of Advance Engineering and Research Development},
  volume  = {6},
  number  = {10},
  year    = {2019}
}@comment{python,katselmus,englannin kielinen}""",
"""@article{larsen2017atomic,
  title={The atomic simulation environment—a Python library for working with atoms},
  author={Larsen, Ask Hjorth and Mortensen, Jens J{\o}rgen and Blomqvist, Jakob and Castelli, Ivano E and Christensen, Rune and Du{\l}ak, Marcin and Friis, Jesper and Groves, Michael N and Hammer, Bj{\o}rk and Hargus, Cory and others},
  journal={Journal of Physics: Condensed Matter},
  volume={29},
  number={27},
  pages={273002},
  year={2017},
  publisher={IOP Publishing}
}@comment{larsen,   fysiikka  , 2017,englannin kielinen}"""]

    def test_tagien_haku(self):
        self.assertEqual(
            ViiteValitsin.hae_tagit(self.esimerkkiviitteet[0]),
            []
        )

        self.assertEqual(
            ViiteValitsin.hae_tagit(self.esimerkkiviitteet[1]),
            ["python","katselmus","englannin kielinen"]
        )

        self.assertEqual(
            ViiteValitsin.hae_tagit(self.esimerkkiviitteet[2]),
            ["larsen","fysiikka","2017","englannin kielinen"]
        )

    def test_tagine_olemassaolo_tiedustelu(self):
        self.assertEqual(
            ViiteValitsin.tagi_tiedustelu(self.esimerkkiviitteet[0],"testitagi"),
            False
        )

        self.assertEqual(
            ViiteValitsin.tagi_tiedustelu(self.esimerkkiviitteet[1],"python"),
            True
        )
        self.assertEqual(
            ViiteValitsin.tagi_tiedustelu(self.esimerkkiviitteet[1],"java"),
            False
        )

        self.assertEqual(
            ViiteValitsin.tagi_tiedustelu(self.esimerkkiviitteet[2],"fysiikka"),
            True
        )
        self.assertEqual(
            ViiteValitsin.tagi_tiedustelu(self.esimerkkiviitteet[2],"python"),
            False
        )

    def test_viite_listan_seulonta_1(self):
        self.assertEqual(
            ViiteValitsin.tagi_seulo_viitteet(self.esimerkkiviitteet,"java"),
            []
        )

    def test_viite_listan_seulonta_2(self): # TODO: Tämä testi on virheellinen. Metodi on keskeneräinen.
        self.assertEqual(
            ViiteValitsin.tagi_seulo_viitteet(self.esimerkkiviitteet,"python"),
            self.esimerkkiviitteet
        )
