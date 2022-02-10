from tkinter import *
import random

renkler = ('red', 'blue', 'orange', 'green', 'gray')

carpan = 10  # Boyutlari pixele cevirmek icin kullanilir

siralar = (1, 3, 1, 2, 3, 1, 2, 3, 1)
yonler = (1, 0, 1, 0, 1, 0, 1, 1, 0)  # 0:normal, 1: 90 derece donuk


class Cisim:

	def __init__(self, tip, t, h, y):
		self.tip = tip
		self.yon = y  # 0:normal, 1: 90 derece donuk


		if y > 0:
			self.taban = h
			self.yuks = t
		else:
			self.taban = t
			self.yuks = h

		self.yerlesti = 0  # yerlesince 1 olacak
		self.x1 = 0
		self.x2 = 0
		self.y1 = 0
		self.y2 = 0

	def yerlestir(self, x, y):
		delta = 0.1
		self.x1 = x + delta
		self.y1 = y + delta
		self.x2 = self.x1 + self.taban - delta
		self.y2 = self.y1 + self.yuks - delta
		self.yerlesti = 1

	def cakisiyormu(self, x, y, dx, dy):
		r1 = (x, y, x + dx, y + dy)
		r2 = (self.x1, self.y1, self.x2, self.y2)

		if ((r1[0] < r2[2]) and (r1[2] > r2[0]) and (r1[1] < r2[3]) and (r1[3] > r2[1])):
			return True
		else:
			return False


class Zincir:
	def __init__(self, siralar, yonler):
		self.zeminyuksekligi = 12
		self.maksimumzemingenisligi = 100

		self.siralar = siralar
		self.yonler = yonler
		self.zincir = list()
		self.kullanilangenislik = 0
		self.zinciryap()

	def zinciryap(self):
		#  sekilleri olusturalim
		for sira, yon in zip(self.siralar, self.yonler):
			taban, yuks, adet = cisimler[sira]
			cisim = Cisim(sira, taban, yuks, yon)
			self.zincir.append(cisim)

	def cismi_zemineyerlestir(self, dx, dy):
		for xx in range(0, self.maksimumzemingenisligi, 1):
			for yy in range(0, self.zeminyuksekligi, 1):
				yerlesmiscisimler = [yc for yc in self.zincir if yc.yerlesti == 1]
				for yerlesmiscisim in yerlesmiscisimler:
					cevap = yerlesmiscisim.cakisiyormu(xx, yy, dx, dy)
					if cevap == True:
						break
				else:
					# Zeminin kenarına geldik mi
					if (yy + dy) <= self.zeminyuksekligi:
						return xx, yy
		else:
			print('Hata oluyor. %s metre genişlik yetmiyor.' % self.maksimumzemingenisligi)
			return -1, -1

	def cisimleri_zemineyerlestir(self):
		for cisim in self.zincir:
			dx, dy = cisim.taban, cisim.yuks
			x, y = self.cismi_zemineyerlestir(dx, dy)
			if x > -1:
				cisim.yerlestir(x, y)
				if x + dx > self.kullanilangenislik:
					self.kullanilangenislik = x + dx
			else:
				print('Hata')
				return

	def bas(self):
		print('Kullanılan:', self.kullanilangenislik)
		satir = "Tip:%s Taban:%s Yuks:%s Yon:%s Yerlesti:%s x1:%3.1f y1:%3.1f x2:%3.1f y2:%3.1f "
		for c in self.zincir:
			print(satir % (c.tip, c.taban, c.yuks, c.yon, c.yerlesti, c.x1, c.y1, c.x2, c.y2))


class Hesap:
	def __init__(self):
		self.random_cekirdegi = 999
		self.ilkjenerasyonAdedi = 5

		self.tipler = []
		self.bireyler = dict()
		self.cisimler = dict()
		self.dnalar   = dict()

		self.dnaAdet = 0

		self.zeminyuksekligi = 12
		# tip: taban, h, adet
		# self.cisimler = {1: (2, 3, 4), 2: (4, 5, 2), 3: (1, 4, 3)}
		# self.dnalar = {1: (2, 3), 2: (2, 3), 3: (2, 3), 4: (2, 3),
		#			   5: (4, 5), 6: (4, 5),
		#			   7: (1, 4), 8: (1, 4), 9: (1, 4)}

		self.dosyaOku()
		self.dnaUret()

	def dosyaOku(self):
		filename = "bilgi.txt"
		with open(filename, 'r') as f:
			lines = f.readlines()

		self.zeminyuksekligi = int(lines[0])
		for line in lines[2:]:
			a = tuple(map(int, line.split()))
			# print(a)
			self.tipler.append(a[0])
			self.cisimler[a[0]] = a[1:]
		#print(self.cisimler)

	def dnaUret(self):
		sira = 0
		for tip in self.tipler:
			taban, yuks, adet = self.cisimler[tip]
			for adetsay in range(adet):
				sira += 1
				self.dnalar[sira] = (taban, yuks)
		self.dnaAdet = sira
		print('dnalar:',self.dnalar)

	def ilkjenerasyonuUret(self):
		random.seed(self.random_cekirdegi)
		siralardizisi = [n for n in range(1, self.dnaAdet+1)]
		# print('Sira:',siralardizisi)

		#Yönler
		for jen in range(1, self.ilkjenerasyonAdedi+1):
			yonlerdizisi = [random.randint(0,1) for nn in range(self.dnaAdet)]
			random.shuffle(siralardizisi)
			# print(siralardizisi, yonlerdizisi)
			# print(jen)
			self.bireyler[jen] = tuple(siralardizisi), tuple(yonlerdizisi)
		print(self.bireyler)

	def bireyHesapla(self, bireyno):
		bireysira, bireyyon = self.bireyler[bireyno]
		zincir = Zincir(bireysira, bireyyon)


if __name__ == "__main__":
	Hesap().ilkjenerasyonuUret()
	exit()
	zincir1 = Zincir(siralar, yonler)
	zincir1.cisimleri_zemineyerlestir()
	zincir1.bas()