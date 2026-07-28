# Class 6 AI Node Local File Service & ngrok Tunnel - AI Agent Setup Instructions

> 📋 **【學員專用】給 AI Agent 的複製貼上 Prompt**：
> 學員將資源包解壓後，開啟專案直接對自己的 AI Agent 傳送這段文字即可：
> 
> ```text
> Agent，請幫我部署並啟動這個資料夾裡的 Class 6 AI Node 服務。
> 
> 請按照以下步驟執行：
> 1. 讀取當前資料夾下的 README.md 說明文件。
> 2. 自動檢查並安裝缺少套件（例如 pip install fastapi uvicorn）。
> 3. 檢查系統是否有 ngrok 命令（若無或版本過舊請提示我或自動安裝）。
> 4. 啟動本機服務 (python app.py) 與連線通道 (ngrok http 127.0.0.1:8888)。
> 5. 成功後，請直接回報我可以使用的【對外 HTTPS 網址】與本機【http://localhost:8888】測試連結！
> ```

---

## 🎯 系統目標
在學員本機啟動一個監聽於 `Port 8888` 的 Python 檔案存取 API 服務（自動存取當前目錄），並使用 `ngrok` 建立安全的對外公網 HTTPS 穿透通道供手機或外部系統存取。

---

## 📋 雙操作模式 (Dual Execution Modes)

### 🚀 模式一：一鍵雙擊 .bat 批次檔模式 (最速體驗)
1. 雙擊 `start.bat` ➔ 自動檢查依賴套件並啟動 Python 服務 (`http://localhost:8888`)。
2. 雙擊 `start_ngrok.bat` ➔ 自動執行對外穿透連線 (`ngrok http 127.0.0.1:8888`)。

### 💻 模式二：CMD / PowerShell 手動命令列模式 (工程師深度實戰)
1. 開啟 CMD 視窗 1：進入資料夾並啟動 Python 服務：
   ```cmd
   cd c6_ngrok_package
   python app.py
   ```
2. 開啟 CMD 視窗 2：手動下達 ngrok 對外穿透指令：
   ```cmd
   ngrok http 127.0.0.1:8888
   ```

---

## 📋 AI Agent 自動化部署與檢測 SOP

### 步驟 1：檢查並安裝 Python 依賴套件
請 Agent 執行以下命令安裝 `fastapi` 與 `uvicorn`：

```bash
pip install fastapi uvicorn
```

---

### 步驟 2：檢查並自動安裝 ngrok

請 Agent 先檢測系統是否有 `ngrok` 命令：

```bash
ngrok --version
```

若回傳 `command not found` 或版本低於 `3.20.0`，請執行更新或自動安裝：

* **若已安裝但版本太舊**:
  ```cmd
  ngrok update
  ```

* **Windows (推薦 winget 或 choco)**:
  ```powershell
  winget install ngrok.ngrok
  # 或 
  choco install ngrok
  ```

* **macOS (Homebrew)**:
  ```bash
  brew install ngrok/ngrok/ngrok
  ```

* **Linux (Ubuntu/Debian)**:
  ```bash
  curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok
  ```

---

### 步驟 3：設定 ngrok Auth Token (首次使用)
提醒學員註冊 [dashboard.ngrok.com](https://dashboard.ngrok.com/signup) 並取得免費的 Authtoken，由 Agent 代為執行設定：

```bash
ngrok config add-authtoken <YOUR_NGROK_AUTHTOKEN>
```

---

### 步驟 4：啟動服務與對外通道抓取

1. **啟動本機 API 服務 (Port 8888)**：
   ```bash
   python app.py
   ```
   * 驗證網址：`http://localhost:8888` 或 `http://127.0.0.1:8888`

2. **啟動外網穿透通道 (另開 Terminal)**：
   ```bash
   ngrok http 127.0.0.1:8888
   ```
3. **抓取 Forwarding 公網 HTTPS 網址**：
   * Agent 可讀取 `http://127.0.0.1:4040/api/tunnels` 獲取最新的公網網址（例如：`https://xxxx.ngrok-free.dev`）並直接顯示給學員！

---

## 🔍 AI Agent 除錯指南 (Troubleshooting)

| 錯誤現象 | 可能原因 | 解決處置 |
| :--- | :--- | :--- |
| `ERR_NGROK_8012` | 尚未啟動 `start.bat` 或埠號未連通 | 先執行 `python app.py` 確保 `127.0.0.1:8888` 正常監聽 |
| `ERR_NGROK_121` / `version too old` | ngrok 版本過舊 (低於 3.20.0) | 執行 `ngrok update` 更新至最新版 |
| `Port 8888 Address already in use` | Port 8888 被其他程式佔用 | 執行 `netstat -ano \| findstr 8888` 找出 PID 並刪除，或於 `app.py` 修改 Port |
