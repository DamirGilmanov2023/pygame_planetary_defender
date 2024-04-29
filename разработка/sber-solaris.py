import pygame
import sys
import os
import random
from random import randint
import time
import math

pygame.init()
clock = pygame.time.Clock()
FPS = 60
#WINDOW_SIZE = (1000, 638)
WINDOW_SIZE = (1000, 660)
screen = pygame.display.set_mode(WINDOW_SIZE)
planet=pygame.image.load('./img/planet.png')
planet2=pygame.image.load('./img/planet2.png')
rocketimg = pygame.image.load('./img/rocket.png')
frag=[]
frag.append(pygame.image.load('./img/frag1.png'))
frag.append(pygame.image.load('./img/frag2.png'))
frag.append(pygame.image.load('./img/frag3.png'))
#interceptor=pygame.draw.polygon(screen,(210,210,64),([455,569],[480,569],[480,560],[500,560],[500,569],[525,569],[490,534]))
rocketx = 490
rockety = 560
stars=[]
for i in range(10):
    stars.append(pygame.image.load(f'./img/star{i+1}.png'))
stars_pos=[[45,54],[98,211],[205,143],[468,85],[520,243],[678,101],[678,254],[731,181],[836,112],[941,197]]
home=pygame.image.load('./img/home.png')
start_pos_line=[[323,False, 0, 1,False,    1,         3,       310,   randint(320,350),False,     1,         3,       310,   randint(620,650)]]    
                #x   start  t0 a yama_flag yama_scale yama_div y_yama x_yama           yama_flag  yama_scale yama_div y_yama x_yama
                #0     1    2  3     4         5          6       7     8                9         10         11       12     13
#start_pos_line0=[[338,False,0,1],[361,False,0,1],[392,False,0,1],[442,False,0,1],[522,False,0,1]]
yama=pygame.image.load('./img/yama.png')
sperm=True #Флаг - разрешить стрелять
sperm_sc=1 #Счетчик, по истечении которого, сперма становится True
buffer=[] #Буфер в котором пульки игрока
start_time=time.time()
fire_time=time.time()
soplo_set = [pygame.image.load(f"./img/soplo{i}.png") for i in range(1, 6)]
asl=0
v=[]
red_nebo=0
score=0
energy=10
f1 = pygame.font.Font(None, 32)
f2 = pygame.font.Font(None, 200)
vzr_set=[pygame.image.load(f"./img/vzr{i}.png") for i in range(1,6)]
vzr=[]
flag_end=False
fire_audio=pygame.mixer.Sound('./audio/fire.mp3')
fire_frag_audio=pygame.mixer.Sound('./audio/fire_frag.mp3')
uron_audio=pygame.mixer.Sound('./audio/uron.mp3')
vzr_audio=pygame.mixer.Sound('./audio/vzr.mp3')
vzr_audio.set_volume(0.5)
pygame.mixer.music.load('./audio/Skulls.mp3')
pygame.mixer.music.play()
#Функция расчета расстояния
def Chpok(enemyx, enemyy, pulyax, pulyay):
    rast = math.sqrt(math.pow(enemyx-pulyax,2) + math.pow(enemyy-pulyay,2))
    if rast < 25:
        return True
    else:
        return False
def get_triangle_area(Xa,Ya,Xb,Yb,Xc,Yc):
    return abs((Xa-Xc)*(Yb-Yc)+(Xb-Xc)*(Yc-Ya))
def Chpok_player(Xa,Ya,Xb,Yb,Xc,Yc,X0,Y0):
    '''usl1=(Xa-X0)*(Yb-Ya)-(Xb-Xa)*(Ya-Y0)
    usl2=(Xb-X0)*(Yc-Yb)-(Xc-Xb)*(Yb-Y0)
    usl3=(Xc-X0)*(Ya-Yc)-(Xa-Xc)*(Yc-Y0)
    print(usl1,usl2,usl3)
    if usl1<=0 and usl2<=0 and usl3<=0:
        return True
    if usl1>=0 and usl2>=0 and usl3>=0:
        return True'''
    
    '''alpha=((Yb-Yc)*(X0-Xc)+(Xc-Xb)*(Y0-Yc))/((Yb-Yc)*(Xa-Xc)+(Xc-Xb)*(Ya-Yc))
    beta=((Yc-Ya)*(X0-Xc)+(Xa-Xc)*(Y0-Yc))/((Yb-Yc)*(Xa-Xc)+(Xc-Xb)*(Ya-Yc))
    gamma=1-alpha-beta
    if alpha>0 and beta>0 and gamma>0:
        return True
    return False'''
    #Ya=Ya*(-1)
    #Yb=Yb*(-1)
    #Yc=Yc*(-1)
    #Y0=Y0*(-1)
    tr_area = get_triangle_area(Xa,Ya,Xb,Yb,Xc,Yc)  # Площадь основного треугольника
    tr_area2 = get_triangle_area(Xa,Ya,Xb,Yb,X0,Y0)  # Площади треугольника, образованного из 2 точек основного
    tr_area3 = get_triangle_area(Xa,Ya,X0,Y0,Xc,Yc)  # и точки, которая проверяется на принадлежность
    tr_area4 = get_triangle_area(Xb,Yb,X0,Y0,Xc,Yc)  # к треугольнику
    # Если площади образованных треугольников равны, то точка в треугольнике
    return tr_area == tr_area2 + tr_area3 + tr_area4
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    clock.tick(FPS)
    if flag_end:
        i=0
        FPS=10
        while i < 660:
            pygame.draw.rect(screen,(randint(0,255),randint(0,255),randint(0,255)),(0,i,1000,20))
            i+=20
        screen.blit(f2.render(f'Score: {score}',True,(randint(0,255),randint(0,255),randint(0,255))), (180,265))
        pygame.display.update()
        continue
    screen.fill((104,25,154))               #Земля
    if red_nebo!=0:
        red_nebo-=1
        pygame.draw.rect(screen, (255,51,136), (0, 0, 1000, 316))   #Небо
        screen.blit(planet2,(303,105))          #Планета
    else:
        pygame.draw.rect(screen, (20,0,144), (0, 0, 1000, 316))   #Небо
        screen.blit(planet,(303,105))          #Планета
    for i in range(10):                    #Звезды
        stars_pos[i][1]-=0.3
        screen.blit(stars[i],stars_pos[i])
        if stars_pos[i][1]<0:
            stars_pos[i][1]=285
    screen.blit(home,(0,285))              #Дома
    for spl in start_pos_line:             #Линии на земле
        if not spl[1]:
            spl[1]=True
            spl[2]=time.time()
        if spl[1]:
            pygame.draw.line(screen,(0,0,0),[0,spl[0]+(time.time()-spl[2])*spl[3]],[1000,spl[0]+(time.time()-spl[2])*spl[3]],4)
            if spl[4]:
                spl[6]-=0.04
                spl[8]-=4
                spl[5]=pygame.transform.scale(yama,(yama.get_width()/spl[6],yama.get_height()/spl[6])) 
                screen.blit(spl[5],spl[5].get_rect(center=(spl[8],spl[7]+(time.time()-spl[2])*spl[3]*0.8)))
            if spl[9]:
                spl[11]-=0.04
                spl[13]+=4
                spl[10]=pygame.transform.scale(yama,(yama.get_width()/spl[11],yama.get_height()/spl[11])) 
                screen.blit(spl[10],spl[10].get_rect(center=(spl[13],spl[12]+(time.time()-spl[2])*spl[3]*0.8)))
            if spl[0]+(time.time()-spl[2])*spl[3] > 700:
                spl[3]=1
                spl[1]=False
                spl[4]=random.choice([True, False])
                spl[9]=random.choice([True, False])
                spl[6]=3
                spl[11]=3
                spl[8]=randint(320,350)
                spl[13]=randint(620,650)
            else:
                spl[3]+=10

    if time.time()-start_pos_line[len(start_pos_line)-1][2]>0.15 and len(start_pos_line)<4:  #Добавление новых линий на земле
        start_pos_line.append([323,False,0,1,False,1,3,310,randint(320,350),False,1,3,310,randint(620,650)])

    keys = pygame.key.get_pressed() #Какая кнопка нажата?
    if keys[pygame.K_LEFT]: #Если нажата клавиша влево, смещаем ракету влево
        rocketx -= 5
    if keys[pygame.K_RIGHT]: #Если нажата клавиша вправо, смещаем ракету вправо
        rocketx += 5
    if keys[pygame.K_UP]:
        rockety -= 2
    if keys[pygame.K_DOWN]:
        rockety += 2
    if rocketx <=0:#Ограничние для ракеты, чтобы не выходила за экран
        rocketx = 0
    elif rocketx >= 929:
        rocketx = 929
    if rockety <=325:
        rockety = 325
    elif rockety >= 560:
        rockety = 560
    screen.blit(rocketimg, (rocketx, rockety))
    screen.blit(soplo_set[asl // 12], (rocketx+24, rockety+45))
    asl += 1
    if asl == 60:
        asl = 0
    pressed_keys = pygame.key.get_pressed()
    if pressed_keys[pygame.K_SPACE]: #Обработка при стрельбе
        #fire.play()
        vr=[]
        vr.append(rocketx)
        vr.append(rockety)
        vr.append('player')
        if sperm: #Если стрельба разрешена, добавляем в буфер пуль координаты ракеты
            buffer.append(vr)
            fire_audio.play()
            sperm=False #Запрещаем стрельбу
    if len(buffer)!=0: #Если буфер не пуст
        i=0
        while i<len(buffer):
            if buffer[i][2]=='player':
                buffer[i][1]=buffer[i][1]-8 #уменьшаем координату у пули, чтобы летела вверх 
                if buffer[i][1]<=0: #Если пуля вышла за пределы экрана уничтожаем ее
                    buffer.pop(i)
                else:
                    pygame.draw.circle(screen, (181,83,40), [buffer[i][0]+35, buffer[i][1]], 5) #если не вышла, то отрисовка пули
            else: 
                if buffer[i][1]>=638: #Если пуля вышла за пределы экрана уничтожаем ее
                    buffer.pop(i)
                else:
                    if buffer[i][2]=='frag0':
                        buffer[i][1]=buffer[i][1]+8 #увеличиваем координату у пули, чтобы летела вверх
                        pygame.draw.circle(screen, (144,255,0), [buffer[i][0]+35, buffer[i][1]], 5) #если не вышла, то отрисовка пули
                    elif buffer[i][2]=='frag1':
                        buffer[i][1]=buffer[i][1]+10 #увеличиваем координату у пули, чтобы летела вверх
                        pygame.draw.circle(screen, (0,165,221), [buffer[i][0]+35, buffer[i][1]], 8) #если не вышла, то отрисовка пули
                    elif buffer[i][2]=='frag2':
                        buffer[i][1]=buffer[i][1]+12 #увеличиваем координату у пули, чтобы летела вверх
                        pygame.draw.circle(screen, (232,103,3), [buffer[i][0]+35, buffer[i][1]], 10) #если не вышла, то отрисовка пули
            i+=1
    if not sperm:   #если разрешения на стрельбу нет, тогда уменьшаем счетчик спермы, который при достижении нуля разрешит стрельбу
        sperm_sc-=1
    if sperm_sc<=0: #если счетчик спермы достиг нуля, разрешаем стрельбу
        sperm=True
        sperm_sc=20 #счетчик спермы заработает, когда запрещена стрельба
    if time.time()-start_time>1:
        start_time=time.time()
        vrag=randint(0,2)
        if vrag==0:
            v.append([randint(0,1000),-30,vrag,random.choice([-1,1]),random.choice([-1,1]),1,3.5]) #х,у,вид врага,множитель
        if vrag==1:
            v.append([randint(0,1000),-30,vrag,random.choice([-2,2]),random.choice([-2,2]),1,3.5]) #х,у,вид врага,множитель
        if vrag==2:
            v.append([randint(0,1000),-30,vrag,random.choice([-3,3]),random.choice([-3,3]),1,3.5]) #х,у,вид врага,множитель
    for f in v:
        f[0]+=f[3]
        f[1]+=f[4]
        #f[5]=pygame.transform.scale(frag[f[2]],(frag[f[2]].get_width()/f[6],frag[f[2]].get_height()/f[6])) 
        #screen.blit(f[5],f[5].get_rect(center=(f[0],f[1])))
        screen.blit(frag[f[2]],(f[0],f[1]))
        #if f[6]>1:
        #    f[6]-=0.05
        if f[0]<0 or f[0]>940:
            f[3]=f[3]*(-1)
        if f[1]<-30:
            f[4]=f[4]*(-1)
        elif f[1]>300:
            f[4]+=0.2
        fire=0
        if score<10:
            rand_time=randint(60,80)*0.01
            fire=randint(0,8)
        elif score<20:
            rand_time=randint(40,60)*0.01
            fire=randint(0,6)
        elif score<30:
            rand_time=randint(20,40)*0.01
            fire=randint(0,4)
        else:
            rand_time=randint(10,20)*0.01
            fire=randint(0,2)
        if time.time()-fire_time>rand_time:
            fire_time=time.time()
            #fire=random.choice([True,False,True])
            if not fire:
                buffer.append([f[0],f[1],f'frag{f[2]}'])
                fire_frag_audio.play()
    i=0
    while i<len(v):
        j=0
        while j<len(buffer):
            if Chpok(v[i][0]+30,v[i][1]+25,buffer[j][0]+35,buffer[j][1]) and buffer[j][2]=='player': #Если есть касание, удаляем соттветсвующую пулю и монстра
                vzr.append([v[i][0],v[i][1],0])
                vzr_audio.play()
                v.pop(i)
                buffer.pop(j)
                score+=1
                break
            j+=1
        i+=1
    i=0
    while i<len(v):
        if v[i][1]>638:
            v.pop(i)
        i+=1
    j=0
    while j<len(buffer):
        #if Chpok(rocketx , rockety, buffer[j][0], buffer[j][1]) and buffer[j][2]!='player':
        #if buffer[j][0]>=rocketx and buffer[j][0]<=rocketx+71 and buffer[j][1]>=rockety and buffer[j][1]<=rockety+:
        if Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,buffer[j][0]+35,buffer[j][1]) and buffer[j][2]!='player':
            red_nebo=60
            energy-=1
            buffer.pop(j)
            uron_audio.play()
            #time.sleep(0.5)
            #sys.exit(0)
        j+=1
    j=0
    while j<len(v):
        if v[j][2]==0:
            if Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0],v[j][1]) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0]+60,v[j][1]) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0]+60,v[j][1]+49) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0],v[j][1]+49):
                red_nebo=60
                energy-=1
                vzr.append([v[j][0],v[j][1],0])
                vzr_audio.play()
                v.pop(j)
                uron_audio.play()
                break
        if v[j][2]==1:
            if Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0],v[j][1]) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0]+60,v[j][1]) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0]+60,v[j][1]+47) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0],v[j][1]+47):
                red_nebo=60
                energy-=1
                vzr.append([v[j][0],v[j][1],0])
                vzr_audio.play()
                v.pop(j)
                uron_audio.play()
                break
        if v[j][2]==2:
            if Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0],v[j][1]) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0]+60,v[j][1]) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0]+60,v[j][1]+53) or \
            Chpok_player(rocketx+71,rockety+38,rocketx,rockety+38,rocketx+30.5,rockety,v[j][0],v[j][1]+53):
                red_nebo=60
                energy-=1
                vzr.append([v[j][0],v[j][1],0])
                vzr_audio.play()
                v.pop(j)
                uron_audio.play()
                break
        j+=1
    #pygame.draw.polygon(screen,(210,210,64),([rocketx,rockety+38],[rocketx+30.5,rockety],[rocketx+71,rockety+38]))
    #pygame.draw.circle(screen, (181,83,40), [rocketx+71,rockety+38], 2)
    #pygame.draw.circle(screen, (181,83,40), [rocketx,rockety+38], 2)
    #pygame.draw.circle(screen, (181,83,40), [rocketx+30.5,rockety], 2)
    pygame.draw.rect(screen, (0,0,0), (0, 638, 1000, 22))
    screen.blit(f1.render(f'Score: {score}',True,(255,255,255)), (30, 639))
    screen.blit(f1.render('Energy:',True,(255,255,255)), (600, 639))
    pos=690
    for en in range(energy):
        pygame.draw.rect(screen, (255,255,255), (pos, 639, 10, 21))
        pos+=20
    for vz in vzr:
        screen.blit(vzr_set[vz[2] // 12], (vz[0],vz[1]))
        vz[2] += 1
        if vz[2] == 60:
            vzr.remove(vz)
    if energy<=0:
        flag_end=True
    pygame.display.update()
