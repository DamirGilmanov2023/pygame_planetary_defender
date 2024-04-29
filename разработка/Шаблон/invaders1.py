import random
import time
import pygame, sys
from pygame.locals import *
import pygame as pg
import pygame.mixer 
import pygame.time
import math

pygame.init()
clock = pygame.time.Clock()
sc = pygame.display.set_mode((1000, 800))
pygame.display.set_caption('Invaders')
rocketimg = pg.image.load('rocket.png')
enemyimg = pg.image.load('enemy.png')
pygame.display.set_icon(rocketimg)
pygame.mixer.music.load("rugged.mp3")
mixer = pygame.mixer
mixer.init()
pygame.mixer.music.play(loops=-1, start=0.0, fade_ms=0)
fire=mixer.Sound("fire1.mp3")
smert=mixer.Sound("smert.mp3")
enemyimg = 0
ochki = 0
sperm=True #Флаг - разрешить стрелять
sperm_sc=1 #Счетчик, по истечении которого, сперма становится True
buffer=[] #Буфер в котором пульки игрока
m_sperm=True #Монстр Флаг - разрешить стрелять
m_sperm_sc=30 #Монстр Счетчик, по истечении которого, сперма монстра становится True
m_buffer=[] #Буфер в котором пульки монстров
rocketx = 500 #Начальная позиция фалической ракеты суборбитального назначения
rockety = 700
roc=0

WHITE = (255, 255, 255) #это белый цвет
RED=(255,0,0) #а это красный цвет
GREEN=(0,255,0) #а это зеленый цвет
DERMO=(127,95,0) #а это  цвет
ROZA=(255,20,147)
speed=1 #Скорость движения монстров
monst = [] #Массив монстров в котором хранятся их положения по х и у
ur=1
start=True


#Заполняем массив монстров 
def draw_monst(ur):
	global monst,enemyimg
	if ur==1:
		enemyimg = pg.image.load('enemy.png')
	elif ur==2:
		enemyimg = pg.image.load('enemy2.png')
	else:
		enemyimg = pg.image.load('enemy3.png')
	i=100
	while i<=1000:
		j=20
		while j<=600:
			vr=[]
			vr.append(i)
			vr.append(j)
			monst.append(vr)
			j+=40
		i+=50

#Функция отрисовки ракеты
def rocket():
	global roc
	roc=sc.blit(rocketimg, (rocketx, rockety))

#Функция отрисовки монстра(ов)
def enemy(enemyx, enemyy, i):
	sc.blit(enemyimg, (enemyx, enemyy))

#Функция расчета расстояния
def Chpok(enemyx, enemyy, pulyax, pulyay):
	rast = math.sqrt(math.pow(enemyx-pulyax,2) + math.pow(enemyy-pulyay,2))
	if rast < 15:
		smert.play()
		return True
	else:
		return False


def Ur(ur):
	global rocketx,rockety,sperm,sperm_sc,monst,buffer,speed,m_sperm,m_buffer,m_sperm_sc,m_pulya,pulya,ochki
	if ur==1:
		sc.fill([120, 120, 120]) #Заполнение черным цветом на каждом кадре
		otr_pul=5
		speed_pul=3
		speed_sperm=15
		cvet=RED
	elif ur==2:
		sc.fill([255, 255, 255]) 
		otr_pul=6
		speed_pul=4
		speed_sperm=12
		cvet=DERMO
	else:
		sc.fill([255, 192, 203]) 
		otr_pul=7
		speed_pul=2
		speed_sperm=10
		cvet=ROZA

	keys = pygame.key.get_pressed() #Какая кнопка нажата?
	if keys[pygame.K_LEFT]: #Если нажата клавиша влево, смещаем ракету влево
		rocketx -= 10
	if keys[pygame.K_RIGHT]: #Если нажата клавиша вправо, смещаем ракету вправо
		rocketx += 10
	
	pressed_keys = pygame.key.get_pressed()
	if pressed_keys[pygame.K_SPACE]: #Обработка при стрельбе
		#fire.play()
		vr=[]
		vr.append(rocketx)
		vr.append(rockety)
		if sperm: #Если стрельба разрешена, добавляем в буфер пуль координаты ракеты
			buffer.append(vr)
			sperm=False #Запрещаем стрельбу
	
	if rocketx <=0: #Ограничние для ракеты, чтобы не выходила за экран
		rocketx = 0
	elif rocketx >= 940:
		rocketx = 940

	rocket() #Отрисовка ракеты
	if len(buffer)!=0: #Если буфер не пуст
		i=0
		while i<len(buffer):
			buffer[i][1]=buffer[i][1]-8 #уменьшаем координату у пули, чтобы летела вверх 
			if buffer[i][1]<=0: #Если пуля вышла за пределы экрана уничтожаем ее
				buffer.pop(i)
			else:
				pulya = pg.draw.circle(sc, GREEN, [buffer[i][0]+15, buffer[i][1]], 5) #если не вышла, то отрисовка пули
			i+=1

	if not sperm:   #если разрешения на стрельбу нет, тогда уменьшаем счетчик спермы, который при достижении нуля разрешит стрельбу
		sperm_sc-=1
	if sperm_sc<=0: #если счетчик спермы достиг нуля, разрешаем стрельбу
		sperm=True
		sperm_sc=10 #счетчик спермы заработает, когда запрещена стрельба
	i=0
	while i<len(monst): #обработка, если пуля попала в монстра
		j=0
		while j<len(buffer):
			if Chpok(monst[i][0], monst[i][1], buffer[j][0], buffer[j][1]): #Если есть касание, удаляем соттветсвующую пулю и монстра
				monst.pop(i)
				buffer.pop(j)
				ochki +=1
			j+=1
		i+=1

	i=0
	while i<len(monst)-1: #Отрисовка монстров
		enemy(monst[i][0], monst[i][1], i)
		i+=1

	for i in range(len(monst)-1): #Сдвигаем монстров 
		monst[i][0]+=speed

	for i in range(len(monst)-1): #Определяем сдвиг монстров влево или вправо
		if monst[i][0] > 1000:
			speed=-1
		elif monst[i][0] < 0:
			speed=1

	if len(m_buffer)!=0: #похожий буфер пуль, только для монстров
		i=0
		while i<len(m_buffer):
			m_buffer[i][1]=m_buffer[i][1]+speed_pul
			if m_buffer[i][1]>=800:
				m_buffer.pop(i)
			else:
				m_pulya = pg.draw.circle(sc, cvet, [m_buffer[i][0], m_buffer[i][1]], otr_pul)
			i+=1

	if not m_sperm:
		m_sperm_sc-=1
	if m_sperm_sc<=0:
		m_sperm=True
		m_sperm_sc=speed_sperm

	rand=random.randint(0,len(monst)-1)
	
	if m_sperm:
		vr=[]
		vr.append(monst[rand][0])
		vr.append(monst[rand][1])
		m_buffer.append(vr)
		m_sperm=False
	
	j=0
	while j<len(m_buffer):
		#if Chpok(rocketx , rockety, m_buffer[j][0], m_buffer[j][1]):
		if m_buffer[j][0]>=roc.left and m_buffer[j][0]<=roc.right and m_buffer[j][1]>=roc.top and m_buffer[j][1]<=roc.bottom:
			time.sleep(3)
			sys.exit(0)
		j+=1

	f1 = pygame.font.Font(None, 36)
	text1 = f1.render(f'Очко={ochki}',True,(180, 0, 0))
	sc.blit(text1, (10, 750))



while True:
	for event in pg.event.get(): #Организация выхода
		if event.type == pg.QUIT:
			sys.exit(0)
	if start:
		draw_monst(ur)
		start=False
	
	Ur(ur)
	if len(monst)<=1:
		ur+=1
		if ur>=4:
			ur=1
		start=True
	
	pg.display.update()
	clock.tick(60)

