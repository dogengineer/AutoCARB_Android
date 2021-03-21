import unittest
from AutoCARB import *

class TestAutoCARB(unittest.TestCase):

############# TEST aria ###############################################################################################

    def test_cp_air(self):
        self.assertTrue(1005 <= cp_air_interp(20) <= 1030)

    def test_pressioneAria3(self):
        self.assertEqual(pressioneAria3(88000,88000), 0)
        self.assertEqual(pressioneAria3(88000,84000), 4000)
        self.assertTrue(86000 <= pressioneAria3(101325,13325) <= 90000)

    def test_RapportoCaloreAria(self):        
        self.assertTrue(1.3 <= RapportoCaloreAria(20) <= 1.4)

    def test_densitAir1(self):
        self.assertAlmostEqual(densitAir1(20,101325), 1.2041, places=4) 

    def test_UmiditAssoluta(self):
        self.assertAlmostEqual(UmiditAssoluta(20, 101325, 40), 0.0058, places=4)

    def test_areaSezione2(self):
        self.assertAlmostEqual(areaSezione2(0.019, 0.019), 2.8353e-4, places=8)       

    def test_areaSezione3(self):
        self.assertAlmostEqual(areaSezione3(0.02), 3.1416e-4, places=8)

    def test_TemperaturaTeoricaAria3(self):
        self.assertAlmostEqual(TemperaturaTeoricaAria3(20, 101325, 13325), 281.6618, places=4)

    def test_velocitaSez3(self):
        self.assertAlmostEqual(velocitaSez3(20, 101325, 13325), 152.5734, places=0)

    def test_velocitaTeoricaSez2(self):
        self.assertAlmostEqual(velocitaTeoricaSez2(20, 101325, 13325, 0.02, 0.019, 0.019), 169.0564, places=0)

    def test_PressioneAriaTeorica2(self):
        self.assertAlmostEqual(PressioneAriaTeorica2(20, 101325, 13325, 0.02, 0.019, 0.019), 85139, places=-3)

    def test_TemperaturaTeoricaAria2(self):
        self.assertAlmostEqual(TemperaturaTeoricaAria2(20, 101325, 13325, 0.02, 0.019, 0.019), 279, places=0)

    def test_NumeroMach(self):
        self.assertAlmostEqual(NumeroMach(20, 101325, 13325, 0.02, 0.019, 0.019), 0.5, places=1)

    def test_DensitaAria2(self):
        self.assertAlmostEqual(DensitaAria2(20, 101325, 13325, 0.02, 0.019, 0.019), 1.06, places=2)

    def test_viscositaDinamicaAir(self):
        self.assertAlmostEqual(viscositaDinamicaAir(20, 101325, 13325, 0.02, 0.019, 0.019), 1.8e-5, places=6)

    def test_numeroReynolds(self):
        self.assertAlmostEqual(numeroReynolds(20, 101325, 13325, 0.02, 0.019, 0.019), 189000, places=-3)

    def test_Coefficiente_efflusso_aria(self):
        self.assertAlmostEqual(Coefficiente_efflusso_aria(20, 101325, 13325, 0.042, 0.02, 0.019, 0.019), 0.9891, places=2)       

    def test_portata_aria(self):
        self.assertAlmostEqual(portata_aria(20, 101325, 40, 13325, 0.042, 0.02, 0.019, 0.019), 0.050196, places=3)

############# TEST benzina ###############################################################################################

    def test_densitBenzina(self):
        self.assertAlmostEqual(densitBenzina(20), 716.5605, places=4)

    def test_coefficiente_attrito_benzina(self):
        self.assertAlmostEqual(coefficiente_attrito_benzina(20, 101325, 13325, 0.02, 0.019, 0.019, 0.017, 0.045, 0.00097), 0.0327, places=3)
        
    def test_rapporto_aria_benzina(self):
        self.assertAlmostEqual(rapporto_aria_benzina(20, 101325, 40, 13325, 0.042, 0.02, 0.019, 0.019, 0.017, 0.045, 0.00097, 0.002), 14.63, places=1)

if __name__ == '__main__':
    unittest.main()