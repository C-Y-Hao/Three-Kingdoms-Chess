from flask import Flask, request, jsonify  # 從 flask 套件匯入必要的工具
from flask import send_from_directory
from flask_cors import CORS                # 匯入跨網域工具（避免網頁被瀏覽器擋掉）
import json                                # 匯入處理 JSON 格式的工具
import subprocess
import os
import sys

app = Flask(__name__)                      # 建立一個網頁應用程式物件
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type"]
}})



# --- 路徑處理邏輯 (Mac 兼容版) ---
if getattr(sys, 'frozen', False):
    # 打包後的環境：sys.executable 是 server 執行檔路徑
    # Mac 的 .app 包裹中，這通常指向 Contents/MacOS/server
    BASE = os.path.dirname(sys.executable)
    STATIC_PATH = sys._MEIPASS
else:
    # 開發環境
    BASE = os.path.dirname(os.path.abspath(__file__))
    STATIC_PATH = BASE

CPP_EXE = os.path.join(BASE, "game")
ipc_dir = os.path.join(BASE, 'ipc')
if not os.path.exists(ipc_dir):
    os.makedirs(ipc_dir)

file_path = os.path.join(ipc_dir, 'hero_info.txt')

@app.route('/')
def home():
    # 讓它正確載入 index.html
    return send_from_directory(STATIC_PATH, "index_2.1.html")

@app.route('/start_game', methods=['POST'])
def start_game():
    data = request.json
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("init\n")
        
        # 1. 處理魏國 (wei)
        for hero in data['wei']:
            if hero['id'] % 100 == 0: # 曹操
                army = 5000
            else:                  # 魏國將領
                army = 4000
            line = f"{hero['id']} {hero['attack']} {hero['defense']} {hero['x']} {hero['y']} {army}\n"
            f.write(line)

        # 2. 處理蜀國 (shu)
        for hero in data['shu']:
            # 劉備 (2000) 和 蜀國將領 都是 2000
            army = 2000
            line = f"{hero['id']} {hero['attack']} {hero['defense']} {hero['x']} {hero['y']} {army}\n"
            f.write(line)

        # 3. 處理吳國 (wu)
        for hero in data['wu']:
            if hero['id'] == 3000:
                army = 5000
            else:
                army = 3000
            line = f"{hero['id']} {hero['attack']} {hero['defense']} {hero['x']} {hero['y']} {army}\n"
            f.write(line)
            
        for hero in data['yuan']:
            if hero['id'] == 4000:
                army = 5000
            else:
                army = 4000
            line = f"{hero['id']} {hero['attack']} {hero['defense']} {hero['x']} {hero['y']} {army}\n"
            f.write(line)
        for hero in data['dong']:
            if hero['id'] == 5000:
                army = 4000
            else:
                army = 3000
            line = f"{hero['id']} {hero['attack']} {hero['defense']} {hero['x']} {hero['y']} {army}\n"
            f.write(line)
        for hero in data['yellow']:
            if hero['id'] == 6000:
                army = 4000
            else:
                army = 4000
            line = f"{hero['id']} {hero['attack']} {hero['defense']} {hero['x']} {hero['y']} {army}\n"
            f.write(line)
        for hero in data['han']:
            if hero['id'] == 7000:
                army = 4000
            else:
                army = 4000
            line = f"{hero['id']} {hero['attack']} {hero['defense']} {hero['x']} {hero['y']} {army}\n"
            f.write(line)
    if os.path.exists(CPP_EXE):
        # 檢查是否有執行權限 (0o755 代表可讀可執行)
        if not os.access(CPP_EXE, os.X_OK):
            os.chmod(CPP_EXE, 0o755)
    process = subprocess.run(
        [CPP_EXE],
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd=BASE  # <--- 加入這行，讓 C++ 知道自己在路徑 BASE 執行
    )
    print("--- C++ 原始輸出開始 ---")
    print(process.stdout)
    print("--- C++ 原始輸出結束 ---")
    return jsonify(json.loads(process.stdout))
        
@app.route('/move_hero', methods=['POST'])
def move_hero():
    data = request.json
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"notinit\n{data['id']} {data['dir']}\n")
    if os.path.exists(CPP_EXE):
        # 檢查是否有執行權限 (0o755 代表可讀可執行)
        if not os.access(CPP_EXE, os.X_OK):
            os.chmod(CPP_EXE, 0o755)
    process = subprocess.run(
        [CPP_EXE],
        capture_output=True,
        text=True,
        encoding='utf-8',
        cwd=BASE  # <--- 加入這行，讓 C++ 知道自己在路徑 BASE 執行
    )
    print("--- C++ 原始輸出開始 ---")
    print(process.stdout)
    print("--- C++ 原始輸出結束 ---")
    return jsonify(json.loads(process.stdout))

if __name__ == '__main__':
    # Mac 專用：防止多進程 Socket 衝突
    import os
    os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'
    
    print("正在啟動伺服器... 請存取 http://127.0.0.1:5000")
    # 必須關閉 debug 和 use_reloader
    app.run(host='127.0.0.1', port=5001, debug=False, use_reloader=False)
