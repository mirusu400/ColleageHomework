from Global import *
from time import sleep
import curses
#캐릭터가 움직일때마다 화면을 조금씩 바꿔주는 함수(캐릭터 따라가는 점 및 배경 복구)
def Show_map_movement(stdscr,Pos_x,Pos_y,dir,Wall_num,Blank_num,Map_Array,Object_Array,Size):
    # dir = 방향
    # 1 = 위 2 = 오른쪽 3 = 아래 4 = 왼쪽
    # 현재 위치 입력
    stdscr.addch(Pos_y, Pos_x * 2, Object_Array[Pos_y][Pos_x])
    #이전 위치 복원
    if dir == 1 and Pos_y > 0:
        stdscr.addch(Pos_y + 1, Pos_x * 2, Map_Array[Pos_y + 1][Pos_x].replace(Blank_str,"　"))

    elif dir == 2 and Pos_x < Size:
        stdscr.addch(Pos_y, Pos_x * 2 - 2, Map_Array[Pos_y][Pos_x - 1].replace(Blank_str,"　"))

    elif dir == 3 and Pos_y < Size:
        stdscr.addch(Pos_y - 1, Pos_x * 2, Map_Array[Pos_y - 1][Pos_x].replace(Blank_str,"　"))

    elif dir == 4 and Pos_x > 0:
        stdscr.addch(Pos_y, Pos_x * 2 + 2, Map_Array[Pos_y][Pos_x + 1].replace(Blank_str,"　"))

    #stdscr.addstr(25, Map_Max_X * 2 + 15,Map_Array[Pos_y][Pos_x - 1].replace(Blank_str,"　"))
    Show_map_GUI(stdscr,Wall_num,Blank_num,Size)

    stdscr.refresh()

    return

def Win(stdscr,Size):
    for i in range(0,Size):
        for j in range(0,Size):
            stdscr.addch(i, j * 2, "　")
    stdscr.addstr(Size // 2, Size, "You Win!")
    stdscr.refresh()
    sleep(10)
    exit()
def End(stdscr,Size):
    for i in range(0,Size):
        for j in range(0,Size):
            stdscr.addch(i, j * 2, "　")
    stdscr.addstr(Size//2,Size,"Game Over!")
    stdscr.refresh()
    sleep(10)
    exit()
    return
def Show_map_GUI(stdscr,Wall_num,Blank_num,Size):
    stdscr.addstr(15,Size*2+15,str(Wall_num).zfill(4))
    stdscr.addstr(16, Size*2+15, str(round((Wall_num/(Size * Size))*100,0)) + "%")
    stdscr.addstr(17, Size*2+15, str(Blank_num).zfill(4))
    stdscr.refresh()


#맵 초기화 함수
def Show_map_full_refresh(stdscr,Wall_num,Blank_num, Map_Array, Size):
    for i in range(0, Size):
        for j in range(0, Size):
            if(Map_Array[i][j] == Blank_str):
                stdscr.addch(i,j*2,"　")
            else:
                stdscr.addch(i,j*2,Map_Array[i][j])
    Show_map_GUI(stdscr,Wall_num,Blank_num,Size)
    stdscr.refresh()
    return
def Show_map_Init(stdscr,Wall_num,Blank_num, Map_Array, Size):
    for i in range(0, Size):
        for j in range(0, Size):
            if(Map_Array[i][j] == Blank_str):
                stdscr.addch(i,j*2,"　")
            else:
                stdscr.addch(i,j*2,Map_Array[i][j])
    stdscr.addstr(15, Size * 2 + 3, "Wall:")
    stdscr.addstr(16, Size * 2 + 3, "Percentage:")
    stdscr.addstr(17, Size * 2 + 3, "Blank:")
    Show_map_GUI(stdscr,Wall_num,Blank_num,Size)
    stdscr.refresh()
    return
