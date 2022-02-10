from tkinter import *
import random

carpan = 10  # Boyutlari pixele cevirmek icin kullanilir


class Cisim:

	def __init__(self, tip, t, h, y, renk):
		self.tip = tip
		self.yon = y  # 0:normal, 1: 90 derece donuk
		self.renk = renk

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
	def __init__(self, dnalar, siralar, yonler):
		self.zeminyuksekligi = 12
		self.maksimumzemingenisligi = 100

		self.dnalar = dnalar
		self.siralar = siralar
		self.yonler = yonler
		self.zincir = list()
		self.kullanilangenislik = 0
		self.zinciryap()

	def zinciryap(self):
		#  sekilleri olusturalim
		for sira, yon in zip(self.siralar, self.yonler):
			taban, yuks, renk = self.dnalar[sira]
			dna = Cisim(sira, taban, yuks, yon, renk)
			self.zincir.append(dna)

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
		satir = "Tip:%s Taban:%s Yuks:%s Yon:%s Yerlesti:%s Renk:%10s P1:[%5.1f,%5.1f] P2:[%5.1f,%5.1f] "
		for c in self.zincir:
			print(satir % (c.tip, c.taban, c.yuks, c.yon, c.yerlesti, c.renk, c.x1, c.y1, c.x2, c.y2))


class Hesap:
	def __init__(self):
		self.random_cekirdegi = 999
		self.BirNesildekiBireyAdedi = 5
		self.BirsonrakiNesileAktarilacakBireyAdedi=2
		self.NesilAdedi = 20
		self.mutasyon_yuzdesi  = 10

		self.renkler = ('red', 'blue', 'orange', 'green', 'gray',
						'pink', 'deep sky blue', 'sea green', 'brown')

		self.tipler = []
		self.nesiller = dict()
		self.bireyler = dict()
		self.cisimler = dict()
		self.dnalar   = dict()
		self.sonuclar = dict()

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
			renk = self.renkler[tip]
			for adetsay in range(adet):
				sira += 1
				self.dnalar[sira] = (taban, yuks, renk)
		self.dnaAdet = sira
		print('dnalar:',self.dnalar)

	def ilkjenerasyonuUret(self):
		random.seed(self.random_cekirdegi)
		siralardizisi = [n for n in range(1, self.dnaAdet+1)]
		# print('Sira:',siralardizisi)

		#Yönler
		for jen in range(1, self.BirNesildekiBireyAdedi+1):
			yonlerdizisi = [random.randint(0,1) for nn in range(self.dnaAdet)]
			random.shuffle(siralardizisi)
			# print(siralardizisi, yonlerdizisi)
			# print(jen)
			fitness = -1
			self.bireyler[jen] = tuple(siralardizisi), tuple(yonlerdizisi), fitness
		print(self.bireyler)

	def yenibireyCaprazlayarak(self, bireyno1, bireyno2):
		b1sira, b1yon, fit1 = self.bireyler[bireyno1]
		b2sira, b2yon, fit2 = self.bireyler[bireyno2]
		bolumyeri = random.randint(1, self.dnaAdet - 1)
		yenisira =b1sira[:bolumyeri] + b2sira[bolumyeri:]
		yeniyon = b1yon[:bolumyeri] + b2yon[bolumyeri:]

		#Mutasyon yapilacak mi?
		if random.randint(1,100) <= self.mutasyon_yuzdesi:
			mutasyon_yeri1 = random.randint(0, self.dnaAdet - 1)
			mutasyon_yeri2 = random.randint(0, self.dnaAdet - 1)
			mutdna1 = yenisira[mutasyon_yeri1]
			mutdna2 = yenisira[mutasyon_yeri2]
			yenisiralist = list(yenisira)
			yenisiralist[mutasyon_yeri1] = mutdna2
			yenisiralist[mutasyon_yeri2] = mutdna1
			yenisira = tuple(yenisiralist)

			mutasyon_yon_yeri = random.randint(0, self.dnaAdet - 1)
			mutasyon_yon_dna = yeniyon[mutasyon_yon_yeri]
			if mutasyon_yon_dna == 0:
				yeni_yon_dna = 1
			else:
				yeni_yon_dna = 0

			yeniyonlist = list(yeniyon)
			yeniyonlist[mutasyon_yon_yeri] =yeni_yon_dna
			yeniyon = tuple(yeniyonlist)

		return (yenisira, yeniyon, -1)



	def bireyHesapla(self, bireyno):
		bireysira, bireyyon, fitness = self.bireyler[bireyno]
		zincir = Zincir(self.dnalar, bireysira, bireyyon)
		zincir.cisimleri_zemineyerlestir()
		#zincir.bas()
		fitness = zincir.kullanilangenislik
		self.bireyler[bireyno] = bireysira, bireyyon, fitness
		self.sonuclar[bireyno] = fitness

	def rulet_secimi(self, population, fitnesses, num):
		gercek_fitnesses = [1.0 / f for f in fitnesses]
		total_fitness = float(sum(gercek_fitnesses))
		rel_fitness = [f / total_fitness for f in gercek_fitnesses]
		probs = [sum(rel_fitness[:i + 1]) for i in range(len(rel_fitness))]

		# Draw new population
		new_population = []
		for n in range(num):
			r = random.random()
			for (i, individual) in enumerate(population):
				if r <= probs[i]:
					new_population.append(individual)
					break
		return new_population

	def SonrakiNesliUret(self):
		# self.bireyler dict'inde bireylerin sira,yon ve fitnessleri var.
		# self.sonuclar dict'inde ise bireyno:fitness degerleri var.
		kucuktenbuyuyeFitnesslar = sorted(self.sonuclar, key=self.sonuclar.__getitem__)
		population = []
		fitnesses = []
		for k,v in self.sonuclar.items():
			population.append(k)
			fitnesses.append(v)
		population = tuple(population)
		fitnesses = tuple(fitnesses)

		yeniBireyler = dict()
		for b in range(self.BirsonrakiNesileAktarilacakBireyAdedi):
			key = kucuktenbuyuyeFitnesslar[b]
			yeniBireyler[b + 1] = self.bireyler[key]

		# Geri kalan bireyler genetik algoritma ile olusturulacak
		for b in range(self.BirsonrakiNesileAktarilacakBireyAdedi, self.BirNesildekiBireyAdedi ):
			birey1no, birey2no = self.rulet_secimi(population, fitnesses, 2)
			yeniBirey = self.yenibireyCaprazlayarak(birey1no, birey2no)
			yeniBireyler[b + 1] = yeniBirey

		# Artik self.bireyler'i bozuyoruz
		self.bireyler = yeniBireyler.copy()
		return

	def nesliHesapla(self):
		for bireyNo in range(1, self.BirNesildekiBireyAdedi + 1):
			self.bireyHesapla(bireyNo)
		print(self.sonuclar.values())


	def hesabaBasla(self):
		self.ilkjenerasyonuUret()
		self.nesliHesapla()
		# self.bireyler dictini self.nesiller dict'inde saklayalim
		self.nesiller[1] = self.bireyler.copy()
		print(self.nesiller)
		for nesil in range(2, self.NesilAdedi + 1):
			self.SonrakiNesliUret()
			self.nesliHesapla()
			self.nesiller[nesil] = self.bireyler.copy()


if __name__ == "__main__":
	hesap = Hesap()
	hesap.hesabaBasla()

