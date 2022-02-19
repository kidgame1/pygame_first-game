#太空生存戰
from ast import PyCF_ALLOW_TOP_LEVEL_AWAIT
import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

WHITE = (255,255,255)
BLACK = (0, 0, 0)
GREEN = (0,255,0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# 遊戲初始化 and 創建視窗
pygame.init()
pygame.mixer.init() #音效初始化
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #創建視窗，寬度與高度
pygame.display.set_caption("第一個遊戲") #更改視窗標題
clock = pygame.time.Clock() #創建一個物件，可對時間做管理和操控

# 載入圖片，載入前要先把 pygame 初始化，不然會發生錯誤
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()      # os.path 代表 python 現在的位置；convert 是轉換圖片 pygame 較容易讀取的格式
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()              #飛機
player_mini_img = pygame.transform.scale(player_img, (25, 19))                          #生命顯示，用飛機圖
player_mini_img.set_colorkey(BLACK)
pygame.display.set_icon(player_mini_img) #更改視窗圖片
# rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()                  #石頭
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()              #子彈
rock_imags = []                                                                          #設定多種石頭，定義為一個列表
for i in range(7):                                                                       #利用for迴圈，載入多個石頭圖案
    rock_imags.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())  #字串裡無法使用變數，前面加上f，即可在字串裡使用變數

expl_anim = {}                                                                           #載入爆炸圖片，用字典存放
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim["lg"].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim["sm"].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim["player"].append(player_expl_img)
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()


#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))      # os.path 代表 python 現在的位置，載入子彈射擊聲音
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))      # os.path 代表 python 現在的位置，載入子彈升級聲音
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))      # os.path 代表 python 現在的位置，載入護盾聲音
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))      # os.path 代表 python 現在的位置，載入死亡聲音
expl_sounds = [                                                           # os.path 代表 python 現在的位置，載入石頭爆炸聲音，音效有兩種，所以用列表
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")),
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))            #載入背景音樂
pygame.mixer.music.set_volume(0.5)                                                #設定音樂聲音大小，參數填寫為0~1





# font_name = pygame.font.match_font('arial')         #載入字體，從電腦裡載入符合的字體
font_name = os.path.join("font.ttf")                #載入字體
def draw_text(surf, text, size, x, y):              #分數的文字顯示：畫在地平面、文字、大小，X座標，Y座標
    font = pygame.font.Font(font_name, size)        #創建一個文字物件，字體，大小
    text_surface = font.render(text, True, WHITE)        #文字，True反鋸齒，顏色
    text_rect = text_surface.get_rect()             #定位
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():                                     #創建石頭
    r = Rock()                                      #每碰撞一次，就從新創建一顆石頭，並重新加入群組裡
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, x, y):                    #生命條的顯示：畫在地平面、文字、大小，X座標，Y座標
    if hp < 0:                                      #避免畫出負的血量
        hp = 0
    BAR_LENGTH = 100                                #設定寬度
    BAR_HEIGHT = 10                                 #設定高度
    fill = (hp/100)*BAR_LENGTH                      #設定要填滿多少
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)                    #畫出裡面填滿的方形
    pygame.draw.rect(surf, WHITE, outline_rect, 2)              #畫出外框

def draw_lives(surf, lives, img, x, y):             #命的顯示
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 32*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0,0))  #blit 是畫，代表要把圖片畫在視窗的哪裡
    draw_text(screen, '太空生存戰', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '← → 移動飛船,空白鍵發射子彈~', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按任意鍵開始遊戲', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        # 取得輸入
        for event in pygame.event.get():    #回傳現在的每個事件
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                waiting = False
                return False



class Player(pygame.sprite.Sprite):                 #飛船
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)         #呼叫sprite的初始函式
        self.image = pygame.transform.scale(player_img, (50,38))                     #image 表示顯示的圖片，然後把圖片轉換成想要的大小
        self.image.set_colorkey(BLACK)              #將黑色設為透明，因為圖片的底色是黑色
        self.rect = self.image.get_rect()           #rect用來定位圖片，這邊是指飛船，get_rect等於把圖片框起來
        self.radius = 20                            #設定一個半徑，用來判定碰撞用
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  #畫出一個圓在飛機上，還有給他對應的屬性，此行是用來確認判定用的，所以註解
        self.rect.centerx = (WIDTH/2)               #將物件的起始x設在中心，為寬度的一半    
        self.rect.bottom = (HEIGHT - 10)            #將物件的起始y設在底部，離最底高 10
        self.speedx = 8
        self.health = 100                           #飛船的生命值
        self.lives = 3                              #幾條命
        self.hidden = False                         #判斷飛船是否隱藏
        self.hide_time = 0                          #飛船隱藏時間
        self.gun = 1                                #設定子彈等級
        self.gun_time = 0

    
    def update(self): 
        now = pygame.time.get_ticks()
        if self.gun > 1 and now - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = now
 
        if self.hidden and now - self.hide_time > 1000:         #判斷飛船是否隱形，並顯示出來
            self.hidden = False
            self.rect.centerx = WIDTH/2               #將物件的起始x設在中心，為寬度的一半    
            self.rect.bottom = HEIGHT - 10            #將物件的起始y設在底部，離最底高 10

        key_pressed = pygame.key.get_pressed()      #判斷鍵盤的按鍵是否有被按壓，並回傳布林值
        if key_pressed[pygame.K_RIGHT]:                 #如果是要判斷別的按鍵，將 d 改為其他的即可
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx

        if self.rect.right > WIDTH:                 #判斷物件右邊的座標是否超過了螢幕寬度
            self.rect.right = WIDTH                 #將物件的右邊座標卡在視窗右邊
        if self.rect.left < 0:                      #判斷物件左邊的座標是否超過了螢幕寬度，XY沒負數
            self.rect.left = 0                      #將物件的左邊座標卡在視窗左邊
    
    def shoot(self):
        if not(self.hidden):
            if self.gun == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            elif self.gun >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):                                 #隱藏飛船
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()

class Rock(pygame.sprite.Sprite):                   #石頭
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)         #呼叫sprite的初始函式
        self.image_ori = random.choice(rock_imags)  #image 表示顯示的圖片，存放未失真(轉動)過的原圖，圖片有多張，所以用隨機的方式選取
        self.image_ori.set_colorkey(BLACK)          #將黑色設為透明，因為圖片的底色是黑色
        self.image = self.image_ori.copy()          
        self.rect = self.image.get_rect()           #rect用來定位圖片，這邊是指石頭，get_rect等於把圖片框起來
        self.radius = int(self.rect.width * 0.85 / 2)                            #設定一個半徑，用來判定碰撞用
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)  #畫出一個圓在石頭上，還有給他對應的屬性，此行是用來確認判定用的，所以註解
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)  #將物件的起始X設為隨機，隨機的範圍為小括號裡的兩個數之間，但因石頭也有寬度，所以要減掉
        self.rect.y = random.randrange(-180, -100)   #將物件的起始y設為隨機
        self.speedy = random.randrange(2, 10)       #設定物件垂直掉落速度為隨機
        self.speedx = random.randrange(-3, 3)       #設定物件水平掉落速度為隨機
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)   #設定石頭轉動的角度
    
    def rotate(self):                               #定義石頭轉動
        self.total_degree += self.rot_degree        #轉動的角度持續 增加
        self.total_degree = self.total_degree % 360 #避免超過360度，所以除360取餘數
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)   #pygame內建圖片轉動的函式，且每次轉動都會造成圖片些微失真，所以前面定義一個原檔，來使失真不會疊加
        center = self.rect.center                   #記住一開始的中心點
        self.rect = self.image.get_rect()           #對轉動後的圖片做重新定位
        self.rect.center = center                   #將轉動後的中心點，設定為新的中心點


    def update(self):
        self.rotate()
        self.rect.y += self.speedy                  #更新物件的y座標
        self.rect.x += self.speedx                  #更新物件的x座標
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0: #判斷，如果物件頂部超過底部視窗，重製設定，判斷超過左邊和右邊也是如此
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)  
            self.rect.y = random.randrange(-100, -40)   
            self.speedy = random.randrange(2, 10)       
            self.speedx = random.randrange(-3, 3)       

class Bullet(pygame.sprite.Sprite):                 #子彈
    def __init__(self, x, y):                       #子彈是由飛船射出去，所以需要知道飛船當下的座標
        pygame.sprite.Sprite.__init__(self)         #呼叫sprite的初始函式
        self.image = bullet_img                     #image 表示顯示的圖片
        self.image.set_colorkey(BLACK)              #將黑色設為透明，因為圖片的底色是黑色
        self.rect = self.image.get_rect()           #rect用來定位圖片，這邊是指石頭，get_rect等於把圖片框起來
        self.rect.centerx = x                       #將物件的起始X設為回傳的值
        self.rect.bottom = y                        #將物件的起始y設為回傳的值
        self.speedy = -10                           #子彈是往上設，所以速度為負
    
    def update(self):
        self.rect.y += self.speedy                  #更新物件的y座標
        if self.rect.bottom < 0:                    #若子彈的底部超過上面的視窗
            self.kill()                             #將子彈這個物件從sprite的群組中移除，kill是sprite裡面的函式

class Explosion(pygame.sprite.Sprite):              #爆炸
    def __init__(self, center, size):               #爆炸的中心點，大爆炸或小爆炸
        pygame.sprite.Sprite.__init__(self)         #呼叫sprite的初始函式
        self.size = size
        self.image = expl_anim[self.size][0]        #image 表示顯示的圖片
        self.rect = self.image.get_rect()           #rect用來定位圖片
        self.rect.center = center                       #將物件的起始X設為回傳的值
        self.frame = 0                        
        self.last_update = pygame.time.get_ticks()                           #回傳初始化後的毫秒數
        self.frame_rate = 50
    
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):                 #寶物
    def __init__(self, center):                     
        pygame.sprite.Sprite.__init__(self)         #呼叫sprite的初始函式
        self.type = random.choice(['shield', 'gun'])
        self.image = power_imgs[self.type]                     #表示顯示的圖片
        self.image.set_colorkey(BLACK)              #將黑色設為透明，因為圖片的底色是黑色
        self.rect = self.image.get_rect()           #rect用來定位圖片，這邊是指石頭，get_rect等於把圖片框起來
        self.rect.center = center                  
        self.speedy = 3                           #東西往下掉，所以速度為正
    
    def update(self):
        self.rect.y += self.speedy                  #更新物件的y座標
        if self.rect.top > HEIGHT:                  
            self.kill()                             #將這個物件從sprite的群組中移除，kill是sprite裡面的函式


pygame.mixer.music.play(-1)                 #播放音樂的寫法，參數裡面為撥放的次數，一直播放就寫-1


# 遊戲迴圈
show_init = True
running = True

while running:
    if show_init:
        close = draw_init()
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        # rock = Rock()                                       #創建一顆石頭
        # all_sprites.add(rock)                               #將石頭加入all_sprites裡面
        for i in range(8):                                    #創建8顆石頭
            new_rock()
        score = 0

    clock.tick(FPS)
    # 取得輸入
    for event in pygame.event.get():    #回傳現在的每個事件
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()


    #更新遊戲
    all_sprites.update()                            #執行群組裡，每個update的函式
    #判斷石頭、子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)        #判斷物件是否碰撞，此函式微sprite內建的，後面的兩個布林值，為如果碰撞後，是否刪除物件
    for hit in hits:
        random.choice(expl_sounds).play()               #每次碰撞時載入石頭爆炸聲音
        score += hit.radius                             #每碰撞一次，就增加分數，並根據石頭的半徑來增加多或少
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    #判斷石頭、飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)    #判斷飛船與石頭是否碰撞，預設的圖形為矩形，現在改為較精準的圓形 
    for hit in hits:
        new_rock()
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = 100
            player.hide()               #復活後暫時隱藏飛船

    #判斷寶物、飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)        #判斷物件是否碰撞，此函式微sprite內建的
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > 100:
                player.health = 100
            shield_sound.play()
        elif hit.type == 'gun':
            player.gunup()
            gun_sound.play()

    if player.lives == 0 and not(death_expl.alive()):
        show_init = True


    #畫面顯示
    screen.fill(BLACK)          #設定螢幕顏色，分別為 R、G、B
    screen.blit(background_img, (0,0))  #blit 是畫，代表要把圖片畫在視窗的哪裡
    all_sprites.draw(screen)    #將 all_sprites 群組裡的東西畫到螢幕上
    draw_text(screen, str(score), 18, WIDTH/2, 10)
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15)
    pygame.display.update()     #更新畫面


pygame.quit