import sqlite3
import sys
from PyQt5.Qt import *


class ucret(QWidget):
    def __init__(self):
        super().__init__()
        self.setUI()
    def setUI(self):
        self.setWindowTitle("Ek Ders")
        self.setWindowIcon(QIcon("para.png"))

        lblBaslik=QLabel("Ek Ders İcmal")
        lblBaslik.setFont(QFont("Arial",18,QFont.Bold))
        lblGunduz=QLabel("Gündüz :")
        lblGece=QLabel("Gece :")
        lblKoor=QLabel("Koordinatörlük :")
        lblNobet=QLabel("Nöbet :")
        lblSosyal=QLabel("Sosyal Etkinlik :")


        self.textGunduz=QLineEdit()
        self.textGunduz.textChanged.connect(lambda: self.numaraKontrol(self.textGunduz,self.textGunduz.text()))
        self.textGece=QLineEdit()
        self.textGece.textChanged.connect(lambda: self.numaraKontrol(self.textGece, self.textGece.text()))
        self.textKoor=QLineEdit()
        self.textKoor.textChanged.connect(lambda: self.numaraKontrol(self.textKoor, self.textKoor.text()))
        self.textNobet=QLineEdit()
        self.textNobet.textChanged.connect(lambda: self.numaraKontrol(self.textNobet, self.textNobet.text()))
        self.textSosyal=QLineEdit()
        self.textSosyal.textChanged.connect(lambda: self.numaraKontrol(self.textSosyal, self.textSosyal.text()))



        btnKatsayi = QPushButton("Katsayı Güncelle")
        btnKatsayi.clicked.connect(self.dialogAc)

        btnHesap=QPushButton("Hesapla")
        btnHesap.clicked.connect(self.hesapla)

        forumSol=QFormLayout()
        forumSol.addRow(QLabel(),lblBaslik)
        forumSol.addRow(lblGunduz,self.textGunduz)
        forumSol.addRow(lblGece,self.textGece)
        forumSol.addRow(lblNobet,self.textNobet)
        forumSol.addRow(lblSosyal,self.textSosyal)
        forumSol.addRow(lblKoor,self.textKoor)
        forumSol.addRow(btnKatsayi, btnHesap)

        lblBas = QLabel("Hesap Tutarları")
        lblBas.setFont(QFont("Arial", 18, QFont.Bold))
        lblBrut=QLabel("Brüt Toplam :")
        lblKesinti=QLabel("Kesinti Toplam :")
        lblNet=QLabel("Net Ödenecek :")

        self.textBrut=QLineEdit()
        self.textBrut.setEnabled(False)
        self.textBrut.setFont(QFont("Arial", 12, QFont.Bold))
        self.textKesinti=QLineEdit()
        self.textKesinti.setEnabled(False)
        self.textKesinti.setFont(QFont("Arial", 12, QFont.Bold))
        self.textNet=QLineEdit()
        self.textNet.setEnabled(False)
        self.textNet.setFont(QFont("Arial", 12, QFont.Bold))

        self.cbLisans=QCheckBox("Yüksek Lisans Mezunuyum")

        lblCombo = QLabel("Vergi Dilimi :")
        self.comboVergiDilimi = QComboBox()
        self.comboVergiDilimi.addItem("15")
        self.comboVergiDilimi.addItem("20")
        self.comboVergiDilimi.addItem("27")
        self.comboVergiDilimi.addItem("35")



        forumSag=QFormLayout()
        forumSag.addRow(QLabel(), lblBas)
        forumSag.addRow(QLabel(), self.cbLisans)
        forumSag.addRow(lblCombo, self.comboVergiDilimi)
        forumSag.addRow(lblBrut, self.textBrut)
        forumSag.addRow(lblKesinti, self.textKesinti)
        forumSag.addRow(lblNet, self.textNet)


        h_box=QHBoxLayout()
        h_box.addLayout(forumSol)
        h_box.addSpacing(50)
        h_box.addLayout(forumSag)
        self.setLayout(h_box)
        self.show()

    def dialogAc(self):
        self.pen=katsayi()
        self.pen.show()

    def hesapla(self):
        gunduz=self.textGunduz.text()
        gece=self.textGece.text()
        sosyal=self.textSosyal.text()
        koor=self.textKoor.text()
        nobet=self.textNobet.text()
        vergiDilimi=float(self.comboVergiDilimi.currentText())

        if gunduz=="":
            gunduz=0
        else:
            gunduz=int(self.textGunduz.text())

        if gece=="":
            gece=0
        else:
            gece=int(self.textGece.text())

        if sosyal=="":
            sosyal=0
        else:
            sosyal=int(self.textSosyal.text())

        if koor=="":
            koor=0
        else:
            koor=int(self.textKoor.text())

        if nobet=="":
            nobet=0
        else:
            nobet=int(self.textNobet.text())

        baglanti = sqlite3.connect("ucretVT.db")
        islec = baglanti.cursor()
        islec.execute("""CREATE TABLE IF NOT EXISTS sabitler(mmk, vergi, gunduz, gece)""")
        islec.execute("""SELECT  mmk, vergi, gunduz, gece FROM sabitler WHERE rowid=1""")
        for row in islec:
            self.mmk=row[0]
            self.vergiOrani=row[1]
            self.gunduzKatsayi=row[2]
            self.geceKatsayi=row[3]
        baglanti.commit()
        baglanti.close()
        topGunduz=gunduz+koor+sosyal+nobet
        topGece=gece
        brut=0
        brutGunduz = float(topGunduz)*float(self.mmk)*float(self.gunduzKatsayi)
        brutGece= float(topGece)*float(self.mmk)*float(self.geceKatsayi)
        if not self.cbLisans.isChecked():
            brut=brutGece+brutGunduz
        if self.cbLisans.isChecked():
            brut = brutGece + brutGunduz + (brutGece + brutGunduz) * 5 / 100

        gv = brut*float(vergiDilimi)/100
        dv = brut*float(self.vergiOrani)/1000
        kesinti=gv+dv
        net=brut-kesinti

        self.textBrut.setText(str(round(brut,2)) + " TL")
        self.textKesinti.setText(str(round(kesinti,2)) + " TL")
        self.textNet.setText(str(round(net,2)) + " TL")

    def numaraKontrol(self, kutu,e):
        if e.isdigit()==False:
            sayi = len(e)-1
            e = e[:sayi]
            kutu.setText(e)
            kutu.setFocus()
            if sayi!=-1:
                mesaj = QMessageBox.warning(self, 'Uyarı!',"Sadece Sayı Giriniz!",QMessageBox.Ok)






class katsayi(QDialog):
    def __init__(self):
        super().__init__()
        self.setUI()
    def setUI(self):
        self.setWindowTitle("Güncel Katsayılar")

        lblMMK=QLabel("Memur Maaş Katsayısı :")
        lblVergi=QLabel("Vergi Oranı (Binde) :")
        lblGunduz=QLabel("Gündüz Oranı :")
        lblGece=QLabel("Gece Oranı :")

        self.textMMK=QLineEdit()
        self.textVergi=QLineEdit()
        self.textGunduz=QLineEdit()
        self.textGece=QLineEdit()

        btnGuncelle=QPushButton("Güncelle")
        btnGuncelle.clicked.connect(self.sabitler)

        forum=QFormLayout()
        forum.addRow(lblMMK, self.textMMK)
        forum.addRow(lblVergi,self.textVergi)
        forum.addRow(lblGunduz,self.textGunduz)
        forum.addRow(lblGece,self.textGece)
        forum.addRow(btnGuncelle)

        self.setLayout(forum)

        self.sabitIsle()


    def sabitler(self):
        mmk=self.textMMK.text()
        vergi=self.textVergi.text()
        gunduz=self.textGunduz.text()
        gece=self.textGece.text()
        baglanti=sqlite3.connect("ucretVT.db")
        islec=baglanti.cursor()
        islec.execute("""CREATE TABLE IF NOT EXISTS sabitler(mmk, vergi, gunduz, gece)""")
        islec.execute("""DELETE FROM sabitler""")
        islec.execute("""INSERT INTO sabitler VALUES("{}","{}","{}","{}") """.format(mmk, vergi, gunduz, gece))
        baglanti.commit()
        baglanti.close()
        self.close()

    def sabitIsle(self):
        baglanti=sqlite3.connect("ucretVT.db")
        islec=baglanti.cursor()
        islec.execute("""CREATE TABLE IF NOT EXISTS sabitler(mmk, vergi, gunduz, gece)""")
        islec.execute("""SELECT  mmk, vergi, gunduz, gece FROM sabitler WHERE rowid=1""")
        for row in islec:
            self.textMMK.setText(row[0])
            self.textVergi.setText(row[1])
            self.textGunduz.setText(row[2])
            self.textGece.setText(row[3])
        baglanti.commit()
        baglanti.close()

if __name__ == '__main__':
    uyg=QApplication(sys.argv)
    anaPen=ucret()
    sys.exit(uyg.exec())