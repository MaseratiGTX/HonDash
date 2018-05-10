from unittest import TestCase, mock

from devices.kpro import Kpro


class TestKpro(TestCase):

    def setUp(self):
        # we are not unit testing USB features and find() may raise a
        # `usb.core.NoBackendError` e.g. on Docker
        with mock.patch('usb.core.find') as m_find:
            m_find.return_value = None
            self.kpro = Kpro()
        self.kpro.data0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                           0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.kpro.data1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def test_battery_v4(self):
        self.kpro.version = 4
        self.kpro.data1[4] = 123
        self.assertEqual(self.kpro.bat(), 12.3)

    def test_rpm_v4(self):
        self.kpro.version = 4
        self.kpro.data0[2] = 100
        self.kpro.data0[3] = 100
        self.assertEqual(self.kpro.rpm(), 6425)

    def test_tps_v4(self):
        self.kpro.version = 4
        self.kpro.data0[5] = 100
        self.assertEqual(self.kpro.tps(), 37)

    def test_ect_v4(self):
        self.kpro.version = 4
        self.kpro.data1[2] = 31
        self.assertEqual(self.kpro.ect(), 90)

    def test_ect_v3(self):
        self.kpro.version = 3
        self.kpro.data1[4] = 31
        self.assertEqual(self.kpro.ect(), 90)

    def test_ect_v2(self):
        self.kpro.version = 2
        self.kpro.data1[4] = 31
        self.assertEqual(self.kpro.ect(), 90)
