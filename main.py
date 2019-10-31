#Map_Array[y][x]
#Object_Array[y][x]

# Map 데이터
# 맵 데이터 벽 2
# 맵 데이터 플레이어가 먹은 맵 2
# dir = 방향
#Object 데이터

import curses
Size=70 #min(stdscr_y,stdscr_x)
Win_Ground_Percentage = 75
Map_Max_X = Size
Map_Max_Y = Size
stdscr = curses.initscr()

#stdscr_y, stdscr_x = stdscr.getmaxyx()
curses.resize_term(Map_Max_Y+1,Map_Max_X*2+1)
if(Size <= 30):
    stdscr.nodelay(int(350 / Size*1.5))
else:
    stdscr.nodelay(1)
stdscr_y, stdscr_x = stdscr.getmaxyx()
dir=0
Pos_x = 0
Pos_y = 0
CoolDown = 0
curses.nl()


Map_Array = [["□"] * Size for i in range(Size)]
Object_Array = [["□"] * Size for i in range(Size)]
def Pos_Movement():
    global Pos_y
    global Pos_x
    global dir
    global CoolDown
    c = stdscr.getch() # 숫자값으로 반환
    if (0 < c < 256):   #다른 문자 입력시
        c = chr(c)      #숫자를 문자로 변환
        if (c in 'Ww') and (dir != 1): dir = 1
        elif (c in 'Dd') and (dir != 2): dir = 2
        elif (c in 'Ss') and (dir != 3): dir = 3
        elif (c in 'Aa') and (dir != 4): dir = 4
        else:  pass
    else: pass  #탈출
    CoolDown += 1
    if (CoolDown == 75):
        if(Map_Array[Pos_y][Pos_x] != "■"):
            Map_Array[Pos_y][Pos_x] = "."
        if (dir == 1 and Pos_y != 0): Pos_y -= 1
        if (dir == 2 and Pos_x != Map_Max_X-1): Pos_x += 1
        if (dir == 3 and Pos_y != Map_Max_Y-1): Pos_y += 1
        if (dir == 4 and Pos_x != 0): Pos_x -= 1
        CoolDown = 0
    return
def Map_init():
    for i in range(0,Size):
        Map_Array[0][i] = "■"
        Map_Array[-1][i] = "■"
        Map_Array[i][0] = "■"
        Map_Array[i][-1] = "■"
    return

def Show_map(Pos_x, Pos_y):
    stdscr.clear()
    #비동기화 오류 보정을 위해 임시변수에 좌표값 저장
    Tmpx = Pos_x
    Tmpy = Pos_y
    TmpStr = Map_Array[Tmpy][Tmpx]
    Map_Array[Tmpy][Tmpx] = "＝"
    for i in range(0, Size):
        result=""
        for j in range(0, Size):
            if(Map_Array[i][j] == "□"):
                result += "　　"
            else:
                result += Map_Array[i][j]*2
           #stdscr.addch(i,j*2,Map_Array[i][j])
        stdscr.addstr(i, 0, str(result))
        #stdscr.addstr(i, 0, result.encode('UTF-8'))
    print(stdscr_y)
    #stdscr.addch(25, 25, "ㅁ")
    stdscr.refresh()
    Map_Array[Tmpy][Tmpx] = TmpStr
    return

def main(screen):
    Map_init()
    screen.clear()
    #멀티쓰레드 시작
    #th1 = Process(target=Pos_Movement, args=(1,))
    #th1.start()
    Timer=0
    CoolDown = 0
    while (1):
        Timer+=1
        Pos_Movement()
        Show_map(Pos_x, Pos_y)

curses.wrapper(main)




