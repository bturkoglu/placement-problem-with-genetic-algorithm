from prg5 import Hesap, Zincir

from tkinter import *

class Cizim(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()

		self.canvas_width = 820
		self.canvas_height = 700

		self.hesap = Hesap()
		self.cizilecekNesilNo = self.hesap.NesilAdedi
		self.cizilecekBireyNo = 1

		self.okunacak_alanlar = (('Bir Nesildeki Birey Adedi', self.hesap.BirNesildekiBireyAdedi),
								 ('Yeni Nesile Taşınacak Birey Adedi', self.hesap.BirsonrakiNesileAktarilacakBireyAdedi),
								 ('Nesil Sayısı', self.hesap.NesilAdedi),
								 ('Mutasyon %', self.hesap.mutasyon_yuzdesi),
								 ('Random Çekirdeği', self.hesap.random_cekirdegi),
								 ('Çizilecek Nesil No', self.cizilecekNesilNo),
								 ('Çizilecek Birey No', self.cizilecekBireyNo),
								 )


		self.okunan_degerler = {}

		self.tuslari_yap()


	def alanlari_oku(self):
		self.hesap.BirNesildekiBireyAdedi = int(self.okunan_degerler['Bir Nesildeki Birey Adedi'].get())
		self.hesap.BirsonrakiNesileAktarilacakBireyAdedi = int(self.okunan_degerler['Yeni Nesile Taşınacak Birey Adedi'].get())
		self.hesap.NesilAdedi = int(self.okunan_degerler['Nesil Sayısı'].get())
		self.hesap.mutasyon_yuzdesi = int(self.okunan_degerler['Mutasyon %'].get())
		self.hesap.random_cekirdegi = int(self.okunan_degerler['Random Çekirdeği'].get())

		self.cizilecekNesilNo = int(self.okunan_degerler['Çizilecek Nesil No'].get())
		self.cizilecekBireyNo = int(self.okunan_degerler['Çizilecek Birey No'].get())
		if self.cizilecekNesilNo not in range(1, self.hesap.NesilAdedi + 1):
			self.cizilecekNesilNo = self.hesap.NesilAdedi
		if self.cizilecekBireyNo not in range(1, self.hesap.BirNesildekiBireyAdedi + 1):
			self.cizilecekBireyNo = self.hesap.BirNesildekiBireyAdedi

	def tuslari_yap(self):
		# Ekranın soluna tuşlar için bir frame yapalım
		f = Frame(self, width=150, height=self.canvas_height, bd=8, relief=RAISED)
		f.pack(side=LEFT, fill=Y)

		# Entry'ler
		frmEntry = Frame(f, bd=3, relief=RAISED)
		frmEntry.pack(side=TOP)
		for alan in self.okunacak_alanlar:
			lab = Label(frmEntry, text=alan[0])
			ent = Entry(frmEntry, justify=CENTER, bd=3)
			ent.insert(0, alan[1])
			lab2 = Label(frmEntry, text=' ')

			lab.pack(side=TOP)
			ent.pack(side=TOP, padx=5)
			lab2.pack(side=TOP)
			self.okunan_degerler[alan[0]] = ent

		# Butonlar
		frmButton = Frame(f, bd=3)
		frmButton.pack(side=TOP, pady=10, fill=X)

		buttonpck = dict(pady=5, side=TOP, expand=YES, fill=X)

		b = Button(frmButton, text='Hesaba Başla', command=self.hesabaBasla)
		b.pack(**buttonpck)
		self.b = b

		b2 = Button(frmButton, text='Çiz',
					command=self.ciz,
					state='disabled')
		b2.pack(**buttonpck)
		self.b2 = b2

		b3 = Button(frmButton, text='İleri > ',
					command=self.ileri,
					state='disabled')
		b3.pack(**buttonpck)
		self.b3 = b3

		b5 = Button(frmButton, text=' < Geri ',
					command=self.geri,
					state='disabled')
		b5.pack(**buttonpck)
		self.b5 = b5

		b4 = Button(frmButton, text='Çıkış',
					command=self.quit)
		b4.pack(**buttonpck)


		# Bilgi
		l = Label(self, text='Bilgi: ', fg='red', bd=4, relief=RAISED)
		l.pack(side=TOP, fill=X)
		self.l = l

		# Canvas
		w = Canvas(self, width=self.canvas_width, height=self.canvas_height,
				   bd=8, relief=RAISED)
		w.pack()
		w.create_rectangle(15, 15, 815, 615)
		self.w = w

		# Copyright
		l = Label(self, text="\u00A9 2016 Her hakkı Bahaeddin TÜRKOĞLU'na aittir.", fg='red')
		l.pack(side=TOP, fill=X)

	def k(self, x):
		carpan = int(self.canvas_height / (1.5 * self.hesap.zeminyuksekligi))
		delta = 50
		return x*carpan + delta

	def ileri(self):
		self.cizilecekBireyNo += 1
		if self.cizilecekBireyNo > self.hesap.BirNesildekiBireyAdedi:
			self.cizilecekNesilNo += 1
			if self.cizilecekNesilNo > self.hesap.NesilAdedi:
				self.cizilecekNesilNo = self.hesap.NesilAdedi
				self.cizilecekBireyNo = self.hesap.BirNesildekiBireyAdedi
			else:
				self.cizilecekBireyNo = 1


		self.okunan_degerler['Çizilecek Nesil No'].delete(0, END)
		self.okunan_degerler['Çizilecek Nesil No'].insert(0,self.cizilecekNesilNo)
		self.okunan_degerler['Çizilecek Birey No'].delete(0, END)
		self.okunan_degerler['Çizilecek Birey No'].insert(0,self.cizilecekBireyNo)
		self.ciz()

	def geri(self):
		self.cizilecekBireyNo -= 1
		if self.cizilecekBireyNo < 1:
			self.cizilecekNesilNo -= 1
			if self.cizilecekNesilNo < 1:
				self.cizilecekNesilNo = 1
				self.cizilecekBireyNo = 1
			else:
				self.cizilecekBireyNo = self.hesap.BirNesildekiBireyAdedi

		self.okunan_degerler['Çizilecek Nesil No'].delete(0, END)
		self.okunan_degerler['Çizilecek Nesil No'].insert(0, self.cizilecekNesilNo)
		self.okunan_degerler['Çizilecek Birey No'].delete(0, END)
		self.okunan_degerler['Çizilecek Birey No'].insert(0, self.cizilecekBireyNo)
		self.ciz()

	def ciz(self):
		self.alanlari_oku()
		self.w.delete("all")
		birey = self.hesap.nesiller[self.cizilecekNesilNo][self.cizilecekBireyNo]
		bireysira, bireyyon, fitness = birey
		zincir = Zincir(self.hesap.dnalar, bireysira, bireyyon, self.hesap.zeminyuksekligi)
		zincir.cisimleri_zemineyerlestir()
		#zincir.bas()
		mesaj = '%s.Nesil    %s.Birey   Fitness:  %s     [Sıra: %s       Yön:  %s]'
		renk = 'blue'
		mesaj = mesaj % (self.cizilecekNesilNo, self.cizilecekBireyNo, fitness, bireysira, bireyyon)
		self.l.config(text=mesaj, fg=renk)

		# Koordinatları cizelim
		renk = 'gray'
		xboy = self.k(self.hesap.zeminyuksekligi*1.5)
		yboy = self.k(self.hesap.zeminyuksekligi)
		xekseni = [self.k(x) for x in range(int(self.hesap.zeminyuksekligi*1.5 + 1))]
		yekseni = [self.k(y) for y in range(self.hesap.zeminyuksekligi + 1)]
		for i,x in enumerate(xekseni):
			self.w.create_line(x,self.k(0),x, yboy, fill=renk)
			self.w.create_text(x, self.k(0)-10, text=str(i))
		for i,y in enumerate(yekseni):
			self.w.create_line(self.k(0), y, xboy, y, fill=renk)
			self.w.create_text(self.k(0) - 10, y, text=str(i))

		for c in zincir.zincir:
			self.w.create_rectangle(self.k(c.x1), self.k(c.y1),
									self.k(c.x2), self.k(c.y2),
									fill = c.renk)

	def stateler(self, s):
		if s == 1:  # Hesapla açık diğerleri kapalı
			self.b['state'] = 'normal'
			self.b2['state'] = 'disabled'
			self.b3['state'] = 'disabled'
			self.b5['state'] = 'disabled'
		elif s == 2:  # Hesapla kapalı, diğerleri açık
			self.b['state'] = 'disabled'
			self.b2['state'] = 'normal'
			self.b3['state'] = 'normal'
			self.b5['state'] = 'normal'

	def hesabaBasla(self):
		self.stateler(2)

		self.alanlari_oku()

		self.cizilecekNesilNo = self.hesap.NesilAdedi
		self.okunan_degerler['Çizilecek Nesil No'].delete(0, END)
		self.okunan_degerler['Çizilecek Nesil No'].insert(0,self.cizilecekNesilNo)

		self.hesap.hesabaBasla()
		self.ciz()


if __name__ == '__main__':
	root = Tk()
	root.title("Genetik Algoritma")
	cizim = Cizim(root)
	cizim.mainloop()
