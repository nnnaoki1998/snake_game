from tkinter import *
import random

snake = []
snake_len = 1  # スタート時のヘビの長さ
block_size = 20  # ブロックのサイズ
#snake_color1, snake_color2 = "purple", "red"  # ヘビの色
food = {"x1":0, "x2":0, "y1":0, "y2":0}  # 餌の座標
food_color = "green"  # 餌の色
drt = ""  # 進行方向
w = 1200  # ウィンドウの幅
h = 800  # ウィンドウの高さ
rate = 5  # ヘビの成長速度
a = 1  # ヘビの加速度
per = 50  # 餌を食べて加速する確率
T = 100  # block_size/Tが速さとなる
is_gameover = False  # Trueでゲームオーバー

win = Tk()  # ウィンドウの作成
cv = Canvas(win, width = w, height = h)
cv.pack()

def start_game():  # ゲームの初期化
    global food, snake_len, drt, t, is_gameover
    snake.clear()  # snake配列を空にする
    drt = ""  # 進行方向を初期化
    t = T  # 速さを初期化
    # ヘビを生成
    for i in range(snake_len):
        x1 = random.randint(1, w/block_size-2) * block_size
        x2 = x1 + block_size
        y1 = random.randint(1, h/block_size-2) * block_size
        y2 = y1 + block_size
        snake.append([x1, y1, x2, y2])
    # 餌を枠内にランダムで配置
    food["x1"] = random.randint(1, w/block_size-2) * block_size
    food["x2"] = food["x1"] + block_size
    food["y1"] = random.randint(1, h/block_size-2) * block_size
    food["y2"] = food["y1"] + block_size

def draw_object():  # オブジェクトを描画
    cv.delete('all')
    cv.create_rectangle(0, 0, w, h, fill="black", width=0)
    cv.create_rectangle(0+block_size, 0+block_size, w-block_size, h-block_size, fill="white", width=0)  # 背景を描画
    for i in range(len(snake)):
        #snake_color = snake_color1 if i%2 == 0 else snake_color2
        #c = i if int(i/16)%2 == 0 else 15-i
        #snake_color = "#" + str(format(c%16,'x')) + "0" + str(format(15-c%16,'x'))
        if int(i/16)%3 == 0:
            r = str(format(15-i%16,'x'))
            g = str(format(i%16,'x'))
            b = "0"
        elif int(i/16)%3 == 1:
            r = "0"
            g = str(format(15-i%16,'x'))
            b = str(format(i%16,'x'))
        else:
            r = str(format(i%16,'x'))
            g = "0"
            b = str(format(15-i%16,'x'))
        snake_color = "#" + r + g + b
        cv.create_rectangle(snake[i][0], snake[i][1], snake[i][2], snake[i][3], fill=snake_color, width=0)  # ヘビを描画
    cv.create_rectangle(food["x1"], food["y1"], food["x2"], food["y2"], fill=food_color, width=0)  # 餌を描画

def move_snake():  # ヘビの移動,餌を食べたか判定,ゲームオーバーか判定
    global snake, food, t, is_gameover
    if is_gameover: return
    # 胴体が頭についてくる
    for i in range(1,len(snake))[::-1]:
        for j in range(4):
            snake[i][j] = snake[i-1][j]
    # ヘビが進む
    if drt == "left":    snake[0][0], snake[0][2] = snake[0][0]-block_size, snake[0][2]-block_size
    elif drt == "right": snake[0][0], snake[0][2] = snake[0][0]+block_size, snake[0][2]+block_size
    elif drt == "up":    snake[0][1], snake[0][3] = snake[0][1]-block_size, snake[0][3]-block_size
    elif drt == "down":  snake[0][1], snake[0][3] = snake[0][1]+block_size, snake[0][3]+block_size
    # 餌を食べた？
    if snake[0][0] == food["x1"] and snake[0][1] == food["y1"]:
        # ヘビが長くなる
        for i in range(rate):
            snake.append([0, 0, 0, 0])
        while True:
            # 新しい餌をランダムで配置
            food["x1"] = random.randint(1, w/block_size-2) * block_size
            food["x2"] = food["x1"] + block_size
            food["y1"] = random.randint(1, h/block_size-2) * block_size
            food["y2"] = food["y1"] + block_size
            # 餌とヘビが重なっていないか？
            is_over = False
            for i in range(len(snake)):
                if food["x1"] == snake[i][0] and food["y1"] == snake[i][1]:
                    is_over = True
                    break
            if is_over == False: break
        if random.randint(0, 100) <= per: t -= a  # per/100の確立でヘビが加速
    win.title("LENGTH of SNAKE = " + str(len(snake)))  # ウィンドウのタイトルにヘビの長さを表示
    # ゲームオーバー？
    if snake[0][0] <= 0 or snake[0][0] >= w-block_size or snake[0][1] <= 0 or snake[0][1] >= h-block_size: is_gameover = True  # 枠外？
    for i in range(1,len(snake)):
        if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:  # 体に衝突?
            is_gameover = True
            break
    if is_gameover: win.title("GAME OVER!! LENGTH of SNAKE = " + str(len(snake)))

def game_loop():  # 描画、移動を繰り返す
    draw_object()
    move_snake()
    win.after(t, game_loop)

def leftKey(event):  # 進行方向をキーボードで操作する
    global drt
    if len(snake) == 1 or drt != "right": drt = "left"

def rightKey(event):
    global drt
    if len(snake) == 1 or drt != "left":  drt = "right"

def upKey(event):
    global drt
    if len(snake) == 1 or drt != "down":  drt = "up"

def downKey(event):
    global drt
    if len(snake) == 1 or drt != "up":    drt = "down"

def click(e):  # クリックで再スタート
    global is_gameover
    if is_gameover:
        is_gameover = False
        start_game()

# マウスイベントの登録
win.bind('<Left>', leftKey)
win.bind('<Right>', rightKey)
win.bind('<Up>', upKey)
win.bind('<Down>', downKey)
win.bind('<Button>', click)

start_game()
game_loop()
win.mainloop()