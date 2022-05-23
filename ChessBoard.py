import numpy as np
class ChessBoard:
    def __init__(self):
        #porn 1;bishop 2;knight 3;rook 4;queen 5:king 6;black -
        self.board = [
            [4,3,2,5,6,2,3,4],
            [1,1,1,1,1,1,1,1],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [-1,-1,-1,-1,-1,-1,-1,-1],
            [-4,-3,-2,-5,-6,-2,-3,-4]]
        self.ep_target=()
        self.can_castl_k=[1,-1] #both player can castling kingside
        self.can_castl_q=[1,-1]

    def can_move(self,pos,player):
        x=pos[0]
        y=pos[1]
        can_move_area = np.zeros((8,8))
        if(player * self.board[y][x]<=0):
            return can_move_area
        else:
            piece =  self.board[y][x]
            #ポーンの移動可能判定
            if(abs(piece)==1):
                for next_x in range(8):
                    for next_y in range(8):
                        if (x == next_x and next_y - y == player and self.board[next_y][next_x] == 0):
                            can_move_area[next_y][next_x]=1
                        elif (abs(next_x-x)==1 and next_y - y == player and self.board[next_y][next_x]*self.board[y][x]<0):
                            can_move_area[next_y][next_x]=1
                        #ポーンの最初の動き
                        elif ((player == 1 and y == 2-1) or (player == -1 and y == 7-1 )) and x == next_x and next_y - y == 2 * player and self.board[y+player][x] == self.board[next_y][next_x] == 0:
                            can_move_area[next_y][next_x]= 1
                        #アンパッサンの判定
                        elif len(self.ep_target)>0:
                            if abs(self.ep_target[0]-x)==1 and y == self.ep_target[1] and next_x == self.ep_target[0] and next_y - self.ep_target[1] == player :
                                can_move_area[next_y][next_x] = 1

            #ビショップの移動可能判定
            elif abs(piece) == 2:
                can_move_area = np.ones((8,8))
                for next_x in range(8):
                    for next_y in range(8):
                        if (abs(next_x-x) != abs(next_y-y)) or (self.board[next_y][next_x]*player>0):
                            can_move_area[next_y][next_x] = 0
                
                flag = False
                temp=list(pos)
                while(temp[0]+1<=7 and temp[1]+1<=7):
                    temp[0]+=1
                    temp[1]+=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True
                flag = False
                temp=list(pos)
                while(temp[0]+1<=7 and temp[1]-1>=0):
                    temp[0]+=1
                    temp[1]-=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True
                flag = False
                temp=list(pos)
                while(temp[0]-1>=0 and temp[1]+1<=7):
                    temp[0]-=1
                    temp[1]+=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True
                flag = False
                temp=list(pos)
                while(temp[0]-1>=0 and temp[1]-1>=0):
                    temp[0]-=1
                    temp[1]-=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True

            #ナイトの移動判定
            elif abs(piece)==3:
                for next_x in range(8):
                    for next_y in range(8):
                        if abs(next_x-x)+abs(next_y-y) == 3 and next_x != x and next_y != y and self.board[next_y][next_x]*player <= 0:
                            can_move_area[next_y][next_x] = 1

            #ルークの判定
            elif abs(piece)==4:
                can_move_area = np.ones((8,8))
                for next_x in range(8):
                    for next_y in range(8):
                        if (x!=next_x and y!=next_y) or self.board[next_y][next_x]*player > 0 :
                            can_move_area[next_y][next_x] = 0
                flag = False
                temp=pos[0]
                while(temp+1<=7):
                    temp+=1
                    if flag:
                        can_move_area[pos[1]][temp]= 0
                        continue
                    if(self.board[pos[1]][temp] != 0):
                        flag = True
                temp=pos[0]
                flag = False
                while(temp-1>=0):
                    temp-=1
                    if flag:
                        can_move_area[pos[1]][temp]= 0
                        continue
                    if(self.board[pos[1]][temp] != 0):
                        flag = True
                temp=pos[1]
                flag = False
                while(temp+1<=7):
                    temp+=1
                    if flag:
                        can_move_area[temp][pos[0]]= 0
                        continue
                    if(self.board[temp][pos[0]] != 0):
                        flag = True     
                temp=pos[1]
                flag = False
                while(temp-1>=0):
                    temp-=1
                    if flag:
                        can_move_area[temp][pos[0]]= 0
                        continue
                    if(self.board[temp][pos[0]] != 0):
                        flag = True 

            #クイーンの移動判定
            elif abs(piece)==5:
                can_move_area = np.ones((8,8))
                for next_x in range(8):
                    for next_y in range(8):
                        if ((x!=next_x and y!=next_y) and (abs(next_x-x) != abs(next_y-y))) or self.board[next_y][next_x]*player > 0 :
                            can_move_area[next_y][next_x] = 0
                #縦横の衝突判定
                flag = False
                temp=pos[0]
                while(temp+1<=7):
                    temp+=1
                    if flag:
                        can_move_area[pos[1]][temp]= 0
                        continue
                    if(self.board[pos[1]][temp] != 0):
                        flag = True
                temp=pos[0]
                flag = False
                while(temp-1>=0):
                    temp-=1
                    if flag:
                        can_move_area[pos[1]][temp]= 0
                        continue
                    if(self.board[pos[1]][temp] != 0):
                        flag = True
                temp=pos[1]
                flag = False
                while(temp+1<=7):
                    temp+=1
                    if flag:
                        can_move_area[temp][pos[0]]= 0
                        continue
                    if(self.board[temp][pos[0]] != 0):
                        flag = True     
                temp=pos[1]
                flag = False
                while(temp-1>=0):
                    temp-=1
                    if flag:
                        can_move_area[temp][pos[0]]= 0
                        continue
                    if(self.board[temp][pos[0]] != 0):
                        flag = True 
                #斜めの衝突判定
                flag = False
                temp=list(pos)
                while(temp[0]+1<=7 and temp[1]+1<=7):
                    temp[0]+=1
                    temp[1]+=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True
                flag = False
                temp=list(pos)
                while(temp[0]+1<=7 and temp[1]-1>=0):
                    temp[0]+=1
                    temp[1]-=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True
                flag = False
                temp=list(pos)
                while(temp[0]-1>=0 and temp[1]+1<=7):
                    temp[0]-=1
                    temp[1]+=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True
                flag = False
                temp=list(pos)
                while(temp[0]-1>=0 and temp[1]-1>=0):
                    temp[0]-=1
                    temp[1]-=1
                    if flag:
                        can_move_area[temp[1]][temp[0]]= 0
                        continue
                    if(self.board[temp[1]][temp[0]] != 0):
                        flag = True
            
            #キングの移動判定
            elif abs(piece)==6:
                for next_x in range(8):
                    for next_y in range(8):
                        if abs(next_y-y) <= 1 and abs(next_x-x) <= 1 and self.board[next_y][next_x]*player <=0:
                            can_move_area[next_y][next_x] = 1
                #キャスリングの判定
                if player == 1:
                    rank = 0
                else:
                    rank = 7
                #キングサイド
                if (player in self.can_castl_k) and self.board[rank][5]==self.board[rank][6]==0:
                    can_move_area[rank][6] = 1
                

                #クイーンサイド
                if (player in self.can_castl_q) and self.board[rank][1]==self.board[rank][2]==self.board[rank][3]==0:
                    can_move_area[rank][2] = 1
                   

            return can_move_area

                                                    
    
#タプルで受け取る,grab状態でクリックされると呼ばれる
    def move(self,pos,destination,player):
        #アンパッサンされた時
        if len(self.ep_target)>0 and abs(self.board[pos[1]][pos[0]])==1 and self.ep_target[0] == destination[0] and abs(pos[0]-self.ep_target[0])==1:
            self.board[self.ep_target[1]][self.ep_target[0]]=0
        #アンパッサン判定用のログ
        if(abs(self.board[pos[1]][pos[0]])==1 and abs(destination[1]-pos[1])==2):
            self.ep_target=destination
        else:
            self.ep_target=()
        #キャスリング判定用のログ
        if abs(self.board[pos[1]][pos[0]])==6:
            if player in self.can_castl_k:
                self.can_castl_k.remove(player)
            elif player in self.can_castl_q:
                self.can_castl_q.remove(player)
        elif abs(self.board[pos[1]][pos[0]])==4:
            if pos[0]==0 and (player in self.can_castl_q):
                self.can_castl_q.remove(player)
            elif pos[0]==7 and (player in self.can_castl_k):
                self.can_castl_k.remove(player)
        #キャスリング時
        if abs(destination[0]-pos[0]) == 2 and abs(self.board[pos[1]][pos[0]])==6:
            if destination[0]-pos[0] > 0:
                self.move((7,destination[1]),(5,destination[1]),player)
            else:
                self.move((0,destination[1]),(3,destination[1]),player)
        #プロモーション処理
        if abs(self.board[pos[1]][pos[0]])==1:
            if player == 1 and destination[1] == 7:
                self.board[destination[1]][destination[0]]=5
                self.board[pos[1]][pos[0]]=0
                return
            elif player == -1 and destination[1] == 0:
                self.board[destination[1]][destination[0]]=5
                self.board[pos[1]][pos[0]]=0
                return

        #移動処理
        self.board[destination[1]][destination[0]]=self.board[pos[1]][pos[0]]
        self.board[pos[1]][pos[0]]=0
