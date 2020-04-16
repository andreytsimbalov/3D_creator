
import numpy as np
import math as m
import pygame
from pygame.locals import *
import random

from OpenGL.GL import *
from OpenGL.GLU import *

#pyuic5 mainwindow.ui -o mainwindow.py

def prav_fig(r, c, n):  # рисование правильных фигур
    fc = []
    for i in range(n):
        ans = []
        phi = i * m.pi * 2 / n
        ans += [c[0] + r * m.sin(phi)]
        ans += [c[1] + r * m.cos(phi)]
        ans += [c[2]]

        fc += [ans]
    #print(fc)
    return fc


def qwe(n):  # построение правильной пирамиды
    a = []
    for i in range(1, n + 1):
        b = [0]
        b += [i]
        a += [b]

        b = [i]
        b += [(i) % (n) + 1]
        a += [b]
    return a


def Figure():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()





def main():
    pygame.init()
    display = (600, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 52.0)
    glTranslatef(0.0, 0.0, -6)  # расположение на дисплее

    x = 0
    y = 0
    z = 0
    while True:

        for event in pygame.event.get():  # обработка нажатия на клавиши вращения
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x -= 1
                elif event.key == pygame.K_RIGHT:
                    x += 1
                elif event.key == pygame.K_UP:
                    y -= 1
                elif event.key == pygame.K_DOWN:
                    y += 1
                elif event.key == pygame.K_w:
                    z -= 1
                elif event.key == pygame.K_s:
                    z += 1
            elif event.type == pygame.KEYUP:
                x = 0
                y = 0
                z = 0
        glRotatef(1, y, x, z)  # скорость и углы вращения модели
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Figure()
        pygame.display.flip()
        pygame.time.wait(10)


def rast(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def center(v):
    c = [0, 0, 0]
    for i in range(len(v)):
        c[0] += v[i][0]
        c[1] += v[i][1]
        c[2] += v[i][2]
    c[0] = c[0] / len(v)
    c[1] = c[1] / len(v)
    c[2] = c[2] / len(v)
    return c


def line_k(i1, i2):  # kx,ky
    #print([i1[1] - i2[1], i2[0] - i1[0]])
    return [i1[1] - i2[1], i2[0] - i1[0]]


def line_d(k, p):  # d
    #print(-p[0] * k[0] - p[1] * k[1])
    return -p[0] * k[0] - p[1] * k[1]


def point_per_two_lines(k, d1, d2):  # k[0]x+k[1]y+d=0 - уравнение прямой, работает толко для перпенд прямых
    x = 0
    y = 0

    if k[0] == 0 and k[1] == 0:
        print('k=0 0')
    if k[0] == 0:
        x = -d2 / k[1]
        y = -d1 / k[1]
    elif k[1] == 0:
        y = -d2 / k[0]
        x = -d1 / k[0]
    else:
        y = (d1 / k[0] - d2 / k[1]) * (k[0] * k[1] / (-k[0] ** 2 - k[1] ** 2))
        x = (-y * k[1] - d1) / k[0]
    return [x, y]


def lines_orientation(k, c, c2, i, p):
    d = line_d(k, c)
    t1 = k[0] * i[0] + k[1] * i[1] + d
    q = line_d(k, c2)
    t2 = k[0] * p[0] + k[1] * p[1] + q
    if t1 * t2 < 0:
        return False
    return True


def polygonizer_2(v1, v2):
    smesh=0
    if len(v1)<3:
        asd=[]+v1
        v1=[]+v2
        v2=[]+asd
        smesh =1
        print('smesh')
    fc = []
    sdvig = len(v1)
    sdvig1 = 0

    for i in range(len(v1)):
        b = [i]
        b += [(i + 1) % (len(v1))]
        fc += [b]

    for i in range(len(v2)):
        b = [sdvig + i]
        b += [sdvig + (i + 1) % (len(v2))]
        fc += [b]

    c1 = center(v1)
    c2 = center(v2)
    c1[0]=0
    c1[1] = 0
    c2[0] = 0
    c2[1] = 0

    c_1 = center(v1)
    c_2 = center(v2)

    for i in range(len(v1)):
        v1[i][0]-=c_1[0]
        v1[i][1] -= c_1[1]

    for i in range(len(v2)):
        v2[i][0]-=c_2[0]
        v2[i][1] -= c_2[1]

    #print(c1,c2)

    svaz = []

    for i in range(len(v1)):
        b = [v1[i]]
        b += [v1[(i - 1) % (len(v1))]]
        k = line_k(b[0], b[1])
        h = 0
        j_flag = 0
        for j in range(len(v2)):
            if lines_orientation(k, c1, c2, v1[i], v2[j]):
                d_centr = line_d([k[1], -k[0]], c2)
                d_point = line_d(k, v2[j])
                p_peres = point_per_two_lines(k, d_centr, d_point)
                h_contr = rast(c2, p_peres)
                if h_contr > h:
                    h = h_contr
                    j_flag = j
        svaz += [j_flag]
    #print(svaz)

    for i in range(len(svaz)):
        j = svaz[i]
        b = [i]
        b += [sdvig + j]
        fc += [b]
        b = [i]
        b += [j]
        #print(b)
        while j != svaz[(i + 1) % (len(svaz))]:
            j = (j + 1) % (len(v2))
            b = [i]
            b += [sdvig + j]
            fc += [b]
            b = [i]
            b += [j]
            #print(b)

    for i in range(len(v1)):
        v1[i][0]+=c_1[0]
        v1[i][1] += c_1[1]

    for i in range(len(v2)):
        v2[i][0]+=c_2[0]
        v2[i][1] += c_2[1]

    asd=len(v1+v2)
    #print(fc[asd:])
    print(fc)
    if smesh==1:
        n=len(v2)
        m=len(v1)
        for i in range(len(fc)):
            for j in range(2):
                if fc[i][j]<m:
                    fc[i][j]+=n
                else:
                    fc[i][j]-=m
        for i in range(n+m,len(fc)):
            fc[i].sort()

        a=[]
        a+=fc[m:m+n]
        a+=fc[:m]
        b=fc[m+n:]
        b.sort(key = lambda val: val[1])
        a+=b
        fc=[]+a


    print(fc)
    return fc


# def polygonizer(v1, v2):
#     fc = []
#     sdvig = len(v1)
#     sdvig1 = 0
#
#     for i in range(len(v1)):
#         b = [i]
#         b += [(i + 1) % (len(v1))]
#         fc += [b]
#
#     for i in range(len(v2)):
#         b = [sdvig + i]
#         b += [sdvig + (i + 1) % (len(v2))]
#         fc += [b]
#
#     for i in range(len(v1)):
#         rasts = []
#         for j in range(len(v2)):
#             rasts += [[rast(v1[i], v2[j]), j]]
#         rasts.sort()
#         fc += [[sdvig1 + i, sdvig + rasts[0][1]]]
#         fc += [[sdvig1 + i, sdvig + rasts[1][1]]]
#
#     for i in range(len(v2)):
#         rasts = []
#         for j in range(len(v1)):
#             rasts += [[rast(v2[i], v1[j]), j]]
#         rasts.sort()
#         fc += [[sdvig + i, sdvig1 + rasts[0][1]]]
#         fc += [[sdvig + i, sdvig1 + rasts[1][1]]]
#
#     return fc


def polygonizer_trangle(e,n,m):# строт боковые полигоны гистиона
    #print(e,n,m)
    fc = []
    for i in range(n):
        for j in range(m,len(e)):
            if (e[j][0]==i):
                for k in range(m, len(e)):
                    if (e[k][0] == (i+1)%(n)):
                        if e[k][1]==e[j][1]:
                            a=[i,(i+1)%(n),e[k][1]]
                            a.sort()

                            fc+=[a]


    for i in range(n,m):
        for j in range(m, len(e)):
            if (e[j][1] == i):
                for k in range(m, len(e)):
                    if (e[k][1] == ((i + 1-n) % (m-n))+n):
                        if e[k][0] == e[j][0]:
                            a = [i, (i + 1-n) % (m-n) +n, e[k][0]]
                            a.sort()
                            if a not in fc:
                                fc += [a]
                            else:
                                print('123', a)

    if n==3:
        fc+=[[0,1,2]]
    elif n>3:
        for i in range(1,n-1):
            fc += [[0, i, i+1]]

    k=m-n
    if k==3:
        fc+=[[n+0,n+1,n+2]]
    elif k>3:
        for i in range(n+1,k+n-1):
            fc += [[n, i, i+1]]

    print(fc)
    return fc


def normal(v):# нормаль к прямой по трём точкам
    a=np.array([[v[0][0],v[0][1],v[0][2]],[v[1][0],v[1][1],v[1][2]],[v[2][0],v[2][1],v[2][2]]])
    b=np.array([-1,-1,-1])

    # нужна настройка нормали при ранге 2

    # if np.linalg.matrix_rank(a)>2:
    #     x = np.linalg.solve(a, b)
    # else:
    #     if np.linalg.matrix_rank(a[0:2])==2:
    #         if np.linalg.matrix_rank(a[0:2][:,])

    try:
        x=np.linalg.solve(a, b)
    except:
        print('error_normal')
        # print(a)
        # print(np.linalg.matrix_rank(a))

        #x = np.linalg.solve(a, b)
        x=[1,1,1]
        #x=[0,0,0]
    dlina=(x[0]**2+x[1]**2+x[2]**2)**0.5
    if dlina<=0:
        print('error_dlina')
    return [-x[0]/dlina,-x[1]/dlina,-x[2]/dlina]


def fig_from_file(s,vert):# путь к файлу
    f = open(s, 'r')
    a=[]
    v=[]
    for s in f:
        j=[s.split()]
        for i in j:
            for k in i:
                a+=[float(k)]
    #print(a)

    k=1
    for i in range(int(a[0])):
        v1=[]
        for j in range(2):
            v1+=[a[k]]
            k+=1
        v1+=[vert]
        v+=[v1]
    #print(v)
    f.close()

    #print(v)
    return v

def modelGenerator(v,sloi):
    fc=[]
    k=-1
    vert=np.arange(-1,1.0000001,2/(sloi-1))
    for i in range(sloi):
        k+=1
        n=int(v[k])
        #print(n)
        vsl=[]
        for j in range(n):
            vi=[]
            for q in range(2):
                k+=1
                vi+=[v[k]]
            vi+=[vert[i]]
            vsl+=[vi]
        fc+=[vsl]
    #print(fc)
    return fc

if __name__ == "__main__":
    radius = 1
    count_of_fertex = 6

    mashtab=1

    # verticies=[[0,0,1]]+prav_fig(1,[0,0,0],count_of_fertex)
    # edges=qwe(count_of_fertex)

    # v1 = prav_fig(0.7, [0, 0, 1], 7)# + [[-2, 0, 1]]  # правильный Н гранник
    # v2 = prav_fig(1, [0.3, 0, 0], 7)  # правильный М гранник

    #print(v1)

    # v1 = prav_fig(0.7, [random.randint(1,10)/10, 0, 1], random.randint(3,10))  # + [[-2, 0, 1]]  # правильный Н гранник
    # v2 = prav_fig(1, [0, 0, 0], random.randint(3,10))  # правильный М гранник

    v1 = prav_fig(0.7*mashtab, [0, 0.5, 1*mashtab], 5)  # + [[-2, 0, 1]]  # правильный Н гранник
    v2 = prav_fig(1*mashtab, [0, 0.5, 0*mashtab], 7)  # правильный М гранник

    verticies = v1 + v2
    edges = polygonizer_2(v1, v2)
    #print(edges)
    # polygons = polygonizer_trangle(edges, len(v1),len(verticies))
    # print(normal([verticies[2],verticies[4],verticies[7]]))

    main()
    #
    # for i in range(5):
    #     v1 = prav_fig(0.7, [0, 0, 1], random.randint(3,10))  # + [[-2, 0, 1]]  # правильный Н гранник
    #     v2 = prav_fig(1, [0.3, 0, 0], 7)  # правильный М гранник
    #     verticies = v1 + v2
    #     edges = polygonizer_2(v1, v2)
    #     main()

