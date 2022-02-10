from tkinter import *

# tip, taban, h, adet
cisimler = {1:(2,3,4), 2:(4,5,2), 3:(1,4,3)}
renkler = ('red','blue','orange','green','gray')

carpan = 10		# Boyutlari pixele cevirmek icin kullanilir

siralar	= (1,3,1,2,3,1,2,3,1)
yonler 	= (1,0,1,0,1,0,1,1,0)		# 0:normal, 1: 90 derece donuk


class Cisim:
	no = 1

	def __init__(self, tip, t, h, y):
		self.tip = tip
		self.yon = y  # 0:normal, 1: 90 derece donuk

		if y > 0:
			self.taban = h
			self.yuks = t
		else:
			self.taban = t
			self.yuks = h

		self.yerlesti = 0		# yerlesince 1 olacak
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

		if( (r1[0] < r2[2]) and (r1[2] > r2[0]) and (r1[1] < r2[3]) and (r1[3] > r2[1]) ):
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
				yerlesmiscisimler = [yc for yc in self.zincir if yc.yerlesti ==1]
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
			return -1,-1

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
		print('Kullanılan:',self.kullanilangenislik)
		satir = "Tip:%s Taban:%s Yuks:%s Yon:%s Yerlesti:%s x1:%3.1f y1:%3.1f x2:%3.1f y2:%3.1f "
		for c in self.zincir:
			print(satir % (c.tip, c.taban, c.yuks, c.yon, c.yerlesti, c.x1, c.y1, c.x2, c.y2 ))


if __name__ == "__main__":
	zincir1 = Zincir(siralar, yonler)
	zincir1.cisimleri_zemineyerlestir()
	zincir1.bas()