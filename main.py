# Map_Array[y][x]
# Object_Array[y][x]

# Map 데이터
# 맵 데이터 벽 2
# 맵 데이터 플레이어가 먹은 맵 2
# dir = 방향
# 1 = 위 2 = 오른쪽 3 = 아래 4 = 왼쪽
# Object 데이터
import copy
import curses
import collections
import random
from Show_map import *
from Global import *
from tkinter.filedialog import askopenfilename

Size=40 #min(stdscr_y,stdscr_x)
Map_Size_num = Size * Size
Map_Max_X = Size
Map_Max_Y = Size
Wall_num = 0
Blank_num = 0
Line_str = "."
Character_str = "＝"
Map_Array = [[Blank_str] * Size for i in range(Size)]
Object_Array = [[Blank_str] * Size for i in range(Size)]
Object_Array[0][0] = Character_str

#pygame.mixer.music.load(soundfile)
#Move_Sound = pygame.mixer.Sound("statics/Move.wav")

stdscr = curses.initscr()




stdscr_y, stdscr_x = stdscr.getmaxyx()
dir = 0
Pos_x = 0
Pos_y = 0
CoolDown = 0
Wall_num = 0
Blank_num = 0
loop_arr = [[-1, 0], [1, 0], [0, -1], [0, 1]]
check_arr = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

#좌우로 움직이는 몬스터
class Monster:
    def __init__(self, x, y, dir, type):
        self.x = x
        self.y = y
        self.dir = dir
        self.type = type
        self.cooldown = 0
        self.type3cooldown = 0
    def Move(self):
        TmpMov = Object_Array[self.y][self.x]
        Object_Array[self.y][self.x] = Blank_str
        if(Map_Array[self.y][self.x] == Wall_str):
            return
        #좌우로 움직이는 타입
        if self.type == 1:
            if(self.dir == 2):
                self.x+=1
                if(self.x >= Map_Max_X - 1 or Map_Array[self.y][self.x+1] == Wall_str):
                    self.dir = 4
            if(self.dir == 4):
                self.x -= 1
                if(self.x <= 1 or Map_Array[self.y][self.x-1] == Wall_str):
                    self.dir = 2
        #상하로 움직이는 타입
        if self.type == 2:
            if (self.dir == 3):
                self.y += 1
                if (self.y >= Map_Max_Y - 1 or Map_Array[self.y+1][self.x] == Wall_str):
                    self.dir = 1
            if (self.dir == 1):
                self.y -= 1
                if (self.y <= 1 or Map_Array[self.y-1][self.x] == Wall_str):
                    self.dir = 3
        #랜덤으로 움직이는 타입
        if self.type == 3:
            self.type3cooldown += 1
            if(self.type3cooldown >= 5):
                self.dir = random.randint(1,4)
                self.type3cooldown = 0
            if (self.dir == 1):
                if (self.y <= 1 or Map_Array[self.y-1][self.x] == Wall_str): self.dir = 3
                else: self.y -= 1
            if (self.dir == 2):
                if (self.x >= Map_Max_X - 1 or Map_Array[self.y][self.x + 1] == Wall_str):
                    self.dir = 4
                else: self.x += 1
            if (self.dir == 4):
                if (self.x <= 1 or Map_Array[self.y][self.x - 1] == Wall_str): self.dir = 2
                else: self.x -= 1
            if (self.dir == 3):
                if (self.y >= Map_Max_Y - 1 or Map_Array[self.y+1][self.x] == Wall_str): self.dir = 1
                else: self.y += 1
        if(Map_Array[self.y][self.x] == Line_str):
            End(stdscr,Size)
        Object_Array[self.y][self.x] = Monster_str
        Show_map_movement(stdscr,self.x,self.y,self.dir,Wall_num,Blank_num,Map_Array,Object_Array,Size)
        self.cooldown = 0


#실제로 칸을 채울때 사용되는 함수
def Fill_Blank(Fill_y,Fill_x,FillCount):
    global Wall_num
    global Blank_num
    Tmpdeque = collections.deque()
    Tmpdeque.append([Fill_y,Fill_x])
    for i in range(0, Size):
        for j in range(0,Size):
            if Map_Array[i][j] == Line_str:
                Wall_num += 1
                Blank_num -= 1
                Map_Array[i][j] = Wall_str
    if(FillCount != 7):
        while True:
            if not Tmpdeque:
                return
            tmpy, tmpx = Tmpdeque.popleft()

            for line in loop_arr:
                try:
                    if (Map_Array[tmpy + line[0]][tmpx + line[1]] == Blank_str):
                        Wall_num += 1
                        Blank_num -= 1
                        Map_Array[tmpy + line[0]][tmpx + line[1]] = Wall_str
                        Tmpdeque.append([tmpy + line[0], tmpx + line[1]])
                        Show_map_full_refresh(stdscr,Wall_num,Blank_num, Map_Array, Size)
                except:
                    pass

           # pygame.mixer.music.stop()
           # pygame.mixer.Sound.play(Move_Sound)

def Flood_Fill():
    # TmpArr = 맵 검사용 Arr, 마음대로 조작해도됨
    TmpArr = copy.deepcopy(Map_Array)
    Tmpdeque = collections.deque()
    Fill_Blank_Arr = [0,0,0,0,0,0,0,0]
    # 점을 이었던 캐릭터 위치 상,하,좌,우,대각선 방향에서 검사를함
    # 검사한 점들 중에서 최소값이 있는 부분이 선으로 이은 곳
    for i in range(0,len(check_arr)):
        # 빈 칸을 발견하면 -> BFS실행
        try:
            if TmpArr[Pos_y+check_arr[i][0]][Pos_x+check_arr[i][1]] == Blank_str:
                Tmpdeque.append([Pos_y+check_arr[i][0], Pos_x+check_arr[i][1]])
                Fill_Blank_Arr[i], TmpArr = BFS(TmpArr, Tmpdeque)
        except:
            pass
    Fillmin = 0
    Fillindex = 0
    for i in range(0,len(Fill_Blank_Arr)):
        if(Fill_Blank_Arr[i] != 0 and (Fillmin == 0 or Fillmin > Fill_Blank_Arr[i])):
            Fillmin = Fill_Blank_Arr[i]
            Fillindex = i
    FillCount = Fill_Blank_Arr.count(0)
    Fill_Blank(Pos_y+check_arr[Fillindex][0],Pos_x+check_arr[Fillindex][1],FillCount)

    return


def Pos_Movement():
    global Pos_y
    global Pos_x
    global dir
    global CoolDown
    c = stdscr.getch()  # 숫자값으로 반환
    IsMoved = 0
    if (0 < c < 256):  # 다른 문자 입력시
        c = chr(c)
        if (c in 'Ww') and (dir != 1):
            dir = 1
        elif (c in 'Dd') and (dir != 2):
            dir = 2
        elif (c in 'Ss') and (dir != 3):
            dir = 3
        elif (c in 'Aa') and (dir != 4):
            dir = 4
        else:
            pass
    CoolDown += 1
    mob1.cooldown += 1
    mob2.cooldown += 1
    mob3.cooldown += 1
    mob4.cooldown += 1
    mob5.cooldown += 1
    if(mob1.cooldown == Monster_Cooldown):
        mob1.Move()
    if (mob2.cooldown == Monster_Cooldown):
        mob2.Move()
    if (mob3.cooldown == Monster_Cooldown):
        mob3.Move()
    if (mob4.cooldown == Monster_Cooldown):
        mob4.Move()
    if (mob5.cooldown == Monster_Cooldown):
        mob5.Move()
    if (CoolDown == Max_Cooldown):
        if (Map_Array[Pos_y][Pos_x] != Wall_str):
            Map_Array[Pos_y][Pos_x] = Line_str
        Character = Object_Array[Pos_y][Pos_x]
        Object_Array[Pos_y][Pos_x] = Blank_str
        Bef_Map_Data = Map_Array[Pos_y][Pos_x]
        if (dir == 1 and Pos_y > 0): Pos_y -= 1; IsMoved = 1
        if (dir == 2 and Pos_x < Map_Max_X - 1): Pos_x += 1; IsMoved = 1
        if dir == 3 and Pos_y < Map_Max_Y - 1: Pos_y += 1; IsMoved = 1
        if (dir == 4 and Pos_x > 0): Pos_x -= 1; IsMoved = 1

        CoolDown = 0

        Object_Array[Pos_y][Pos_x] = Character
        Now_Map_Data = Map_Array[Pos_y][Pos_x]
        if(IsMoved == 1):
            if (Bef_Map_Data == Line_str and Now_Map_Data == Wall_str):
                # TODO: FLOOD FILL
                Flood_Fill()
                Show_map_full_refresh(stdscr,Wall_num,Blank_num, Map_Array, Size)
                pass
            elif (Bef_Map_Data == Line_str and Now_Map_Data == Line_str):
                End(stdscr,Size)
            else:
                Show_map_movement(stdscr,Pos_x,Pos_y,dir,Wall_num,Blank_num,Map_Array,Object_Array,Size)
            isMoved = 0
        if(round((Wall_num/Map_Size_num)*100,0) >= Win_Percentage):
            sleep(1)
            Win(stdscr,Size)

    return


def Map_init():
    global Wall_num
    global Blank_num
    # 임시적으로 벽 생성 -> 나중에 txt파일로 읽을거임
    for i in range(0, Size):
        Map_Array[0][i] = Wall_str
        Map_Array[-1][i] = Wall_str
        Map_Array[i][0] = Wall_str
        Map_Array[i][-1] = Wall_str
    # 벽 갯수 확인
    for i in range(0, Size):
        for j in range(0, Size):
            if Map_Array[i][j] == Wall_str:
                Wall_num += 1
            else:
                Blank_num += 1
    return
def Custom_Map_init():
    global Wall_num
    global Blank_num
    global Pos_x
    global Pos_y
    global Object_Array
    global Map_Array
    filename = askopenfilename()
    File = open(filename,"rt",encoding="UTF-8")
    i=0
    for line in File:
        if "Size" in line:
            Size = int(list(map(str,line.split("=")))[1])
            Map_Array = [[Blank_str] * Size for p in range(Size)]
            Object_Array = [[Blank_str] * Size for p in range(Size)]
        elif "XYPOS" in line:
            Pos_x, Pos_y = list(map(int,list(map(str, line.split("=")))[1].split(" ")))
        else:
            for j in range(0,len(line)-1):
                a = line[j]
                Map_Array[i-1][j] = a
        i+=1
    # 벽 갯수 확인
    for i in range(0, Size):
        for j in range(0, Size):
            if Map_Array[i][j] == Wall_str:
                Wall_num += 1
            else:
                Blank_num += 1
    return Size

#임시로 어디를 가져와야할지 정할때 사용하는 함수
def BFS(TmpArr, Tmpdeque):
    Fill_Blank = 0
    while True:
        if not Tmpdeque:
            return Fill_Blank, TmpArr
        tmpy, tmpx = Tmpdeque.pop()
        for line in loop_arr:
            try:
                if (TmpArr[tmpy + line[0]][tmpx + line[1]] == Blank_str):
                    Fill_Blank += 1
                    TmpArr[tmpy + line[0]][tmpx + line[1]] = "-1"
                    Tmpdeque.append([tmpy + line[0], tmpx + line[1]])
            except:
                pass

def main(screen):
    screen.clear()

    Timer = 0
    CoolDown = 0
    Show_map_Init(stdscr,Wall_num,Blank_num,Map_Array, Size)
    while (1):
        Timer += 1
        Pos_Movement()


if __name__ == '__main__':
    curses.echo()
    stdscr.addstr(0,0,"Use basic map: 1, Custom map: 2")
    stdscr.refresh()
    a =stdscr.getch()
    if (a == ord("1")):
        Map_init()
    else:
        Size = Custom_Map_init()
        Map_Size_num = Size * Size
        Map_Max_X = Size
        Map_Max_Y = Size

    mob1 = Monster(x=random.randint(1, Size - 1), y=random.randint(1, Size - 1), dir=2, type=1)
    mob2 = Monster(x=random.randint(1, Size - 1), y=random.randint(1, Size - 1), dir=3, type=2)
    mob3 = Monster(x=random.randint(1, Size - 1), y=random.randint(1, Size - 1), dir=3, type=3)
    mob4 = Monster(x=random.randint(1, Size - 1), y=random.randint(1, Size - 1), dir=4, type=1)
    mob5 = Monster(x=random.randint(1, Size - 1), y=random.randint(1, Size - 1), dir=3, type=3)
    curses.resize_term(Map_Max_Y + 1, Map_Max_X * 2 + 1 + 35)
    stdscr.nodelay(1000)
    curses.nl()
    curses.wrapper(main)
