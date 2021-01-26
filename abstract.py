import pygame
import random


class abstract:
    def __init__(self):

        # 移動先の可否を表すpath_listを取得
        self.path=self.path_list()

        # 行動回数の初期化
        self.count=0

        # 移動先の座標を表すmove_listを取得
        self.move=self.move_list()

        # エピソードの終了を判定するdoneの初期化
        self.done=False

        #画面のサイズの設定
        window_size=(320, 320)

        # Pygameを初期化
        pygame.init()

        # 描画画面の作成
        self.screen=pygame.display.set_mode(window_size)

        #グリッドサイズを設定
        self.grid_size=64

        #ネズミ, チーズ, 背景の画像のパスをそれぞれ設定
        agent_img_path='images/agent.png'
        cheese_img_path='images/cheese.png'
        bg_img_path='images/background.png'

        #各種画像の設定
        self.agent=pygame.image.load(agent_img_path)
        self.agent=pygame.transform.smoothscale(self.agent,(self.grid_size, self.grid_size))
        
        self.cheese=pygame.image.load(cheese_img_path)
        self.cheese=pygame.transform.smoothscale(self.cheese,(self.grid_size, self.grid_size))
        
        self.img_bg=pygame.image.load(bg_img_path)

        #背景画像の左上と右下の角の座標を取得
        self.rect_bg=self.img_bg.get_rect()

        #ネズミ(=エージェント)とチーズ(=報酬)の初期位置を設定
        self.a_pos=1
        self.r_pos=2

    def path_list(self):
        """
        各部屋から移動可能な部屋を表すlistを返す
        """
        effect_path_list=[
            [1,1,1,1,1],
            [1,1,0,0,0],
            [1,0,1,0,0],
            [1,0,0,1,0],
            [1,0,0,0,1]
        ]

        return effect_path_list

    def move_list(self):
        """
        各部屋の座標を返す
        """
        move=[
            [160,160],
            [220,90],
            [90,220],
            [220,220],
            [90,90]
        ]
        
        return move

    def step(self,action):
        """
        一回分の行動を実行
        """

        # 行動回数を更新
        self.count+=1

        # エージェントの行動がvalidかをcheck関数で確認
        reward=0
        self.a_pos,self.r_pos,reward=self.check(action)

        # カウントが100に達したらdone = True
        if self.count==100:
            self.done=True
            self.count=0

        # 移動した場所の番号と、報酬と、doneを返す
        return self.a_pos, reward, self.done

    def check(self, tar_pos):
        """
        チェックした移動先と新しい報酬の座標と報酬を返す
        """

        # 報酬を初期化
        reward=0

        # もしエージェントの選択した部屋へ移動不可能であったら
        if self.path[self.a_pos][tar_pos]==0:
            return self.a_pos, self.r_pos, reward
        # もしエージェントの選択した部屋へ移動可能であり、移動先に報酬があったら
        elif tar_pos==self.r_pos:
            #報酬を獲得したので、報酬は+1した上で、位置は新たな場所に更新
            return tar_pos, self.r_pos%4+1, reward+1.
        # もしエージェントの選択した部屋へ移動可能であり、移動先に報酬がなかったら
        else:
            return tar_pos, self.r_pos, reward


    def render(self):
        """
        ゲームを画面に表示する
        """
        
        #self.moveかネズミの移動先の座標を取得
        agent_pos=self.move[self.a_pos]
        
        #self.moveかチーズの移動先の座標を取得
        reward_pos=self.move[self.r_pos]
        
        #背景画像を表示
        self.screen.blit(self.img_bg, self.rect_bg)
        
        #チーズを画面に表示
        self.screen.blit(self.cheese,(reward_pos[0]-self.grid_size/2, reward_pos[1]-self.grid_size/2))
        
        #ネズミを画面に表示
        self.screen.blit(self.agent,(agent_pos[0]-self.grid_size/2, agent_pos[1]-self.grid_size/2))
        
        #画面を更新
        pygame.display.flip()

    def reset(self):
        """
        一定回数実行したら、環境をリセットする。

        """
        #チーズの座標を初期位置に戻す
        self.r_pos=2

        #ネズミの座標を初期位置に戻す
        self.a_pos=1

        self.done=False

        return self.a_pos
