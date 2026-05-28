from pages.login_page import LoginPage
from pages.siswa_page import SiswaPage
from pages.nilai_page import NilaiPage
from pages.kehadiran_page import KehadiranPage
from pages.motivasi_page import MotivasiPage
from pages.disiplin_page import DisiplinPage
from pages.prediksi_page import PrediksiPage

app = PrediksiPage()
app = DisiplinPage()
app = MotivasiPage()
app = KehadiranPage()
app = NilaiPage()
app = SiswaPage()
app = LoginPage()
app.mainloop
