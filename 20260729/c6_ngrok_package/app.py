import os
import time
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI(title="Local File Browser Node - Class 6")

# 瀏覽當前目錄 (程式所在目錄)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.get("/api/files")
def list_current_dir_files():
    """讀取當前程式所在目錄的所有檔案與子資料夾"""
    items = []
    try:
        for name in os.listdir(CURRENT_DIR):
            # 隱藏檔略過
            if name.startswith('.'):
                continue
            filepath = os.path.join(CURRENT_DIR, name)
            is_dir = os.path.isdir(filepath)
            stat = os.stat(filepath)
            items.append({
                "name": name,
                "is_dir": is_dir,
                "size_bytes": stat.st_size if not is_dir else 0,
                "size_display": f"{round(stat.st_size / 1024, 2)} KB" if not is_dir else "資料夾",
                "modified": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stat.st_mtime))
            })
        # 資料夾在前的排序
        items.sort(key=lambda x: (not x["is_dir"], x["name"].lower()))
        return {
            "status": "success",
            "current_dir": CURRENT_DIR,
            "items": items
        }
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/api/file-content")
def get_file_content(filename: str):
    """讀取當前目錄下的檔案內容 (純文字預覽)"""
    filepath = os.path.join(CURRENT_DIR, filename)
    if not os.path.exists(filepath) or os.path.isdir(filepath):
        return JSONResponse({"status": "error", "message": "檔案不存在或為資料夾"}, status_code=404)
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read(50000) # 讀取前 50KB 預覽
        return {"status": "success", "filename": filename, "content": content}
    except Exception as e:
        return JSONResponse({"status": "error", "message": str(e)}, status_code=500)

@app.get("/", response_class=HTMLResponse)
def index():
    """單檔內嵌 HTML 介面 (不需要額外前端檔案)"""
    html_content = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Node 本機檔案存取服務 (Port 8888)</title>
    <style>
        :root {
            --bg: #0f172a;
            --card-bg: rgba(30, 41, 59, 0.85);
            --accent-cyan: #06b6d4;
            --accent-green: #10b981;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --border: #334155;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: var(--bg); color: var(--text-primary); padding: 2rem 1rem; display: flex; justify-content: center; }
        .container { max-width: 900px; width: 100%; }
        .header { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; text-align: center; backdrop-filter: blur(10px); }
        .header h1 { color: var(--accent-cyan); font-size: 1.6rem; margin-bottom: 0.5rem; }
        .header p { color: var(--text-secondary); font-size: 0.95rem; }
        .path-badge { display: inline-block; background: rgba(6, 182, 212, 0.15); border: 1px solid var(--accent-cyan); color: var(--accent-cyan); padding: 0.38rem 0.9rem; border-radius: 20px; font-family: monospace; margin-top: 0.75rem; font-size: 0.88rem; word-break: break-all; }
        .file-list { background: var(--card-bg); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; backdrop-filter: blur(10px); }
        .file-item { display: flex; align-items: center; justify-content: space-between; padding: 1rem 1.25rem; border-bottom: 1px solid var(--border); transition: background 0.2s; }
        .file-item:last-child { border-bottom: none; }
        .file-item:hover { background: rgba(51, 65, 85, 0.5); }
        .file-info { display: flex; align-items: center; gap: 0.75rem; }
        .file-icon { font-size: 1.3rem; }
        .file-name { font-size: 1rem; font-weight: 600; color: var(--text-primary); }
        .file-meta { font-size: 0.85rem; color: var(--text-secondary); display: flex; gap: 1rem; align-items: center; margin-top: 0.25rem; }
        .btn-view { background: rgba(6, 182, 212, 0.2); border: 1px solid var(--accent-cyan); color: var(--accent-cyan); padding: 0.35rem 0.8rem; border-radius: 6px; cursor: pointer; font-size: 0.85rem; font-weight: 600; transition: all 0.2s; }
        .btn-view:hover { background: var(--accent-cyan); color: #000; }
        .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.8); backdrop-filter: blur(5px); justify-content: center; align-items: center; padding: 1rem; z-index: 100; }
        .modal-content { background: #1e293b; border: 1px solid var(--border); border-radius: 12px; max-width: 800px; width: 100%; max-height: 80vh; display: flex; flex-direction: column; overflow: hidden; }
        .modal-header { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.25rem; border-bottom: 1px solid var(--border); }
        .modal-title { color: var(--accent-cyan); font-weight: 700; }
        .modal-close { background: none; border: none; color: var(--text-secondary); font-size: 1.5rem; cursor: pointer; }
        .modal-body { padding: 1.25rem; overflow-y: auto; font-family: monospace; font-size: 0.9rem; color: #e2e8f0; white-space: pre-wrap; word-break: break-all; background: #0f172a; flex: 1; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📁 AI Node 本機檔案存取服務</h1>
            <p>銀河軟體 Class 6 教學實戰範例 | 瀏覽程式所在目錄</p>
            <div id="dirPath" class="path-badge">載入中...</div>
        </div>
        <div class="file-list" id="fileContainer">
            <div class="file-item"><span style="color:var(--text-secondary)">正在讀取本機目錄檔案...</span></div>
        </div>
    </div>

    <!-- 預覽 Modal -->
    <div id="viewModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <span id="modalFileName" class="modal-title">檔案預覽</span>
                <button class="modal-close" onclick="closeModal()">&times;</button>
            </div>
            <div id="modalBody" class="modal-body"></div>
        </div>
    </div>

    <script>
        async function fetchFiles() {
            try {
                const res = await fetch('/api/files');
                const data = await res.json();
                document.getElementById('dirPath').innerText = '📍 當前程式目錄: ' + data.current_dir;
                
                const container = document.getElementById('fileContainer');
                if (!data.items || data.items.length === 0) {
                    container.innerHTML = '<div class="file-item">目錄下尚無檔案</div>';
                    return;
                }
                
                container.innerHTML = data.items.map(item => `
                    <div class="file-item">
                        <div class="file-info">
                            <span class="file-icon">${item.is_dir ? '📁' : '📄'}</span>
                            <div>
                                <div class="file-name">${item.name}</div>
                                <div class="file-meta">
                                    <span>${item.size_display}</span>
                                    <span>修改時間: ${item.modified}</span>
                                </div>
                            </div>
                        </div>
                        ${!item.is_dir ? `<button class="btn-view" onclick="previewFile('${item.name}')">預覽內容</button>` : ''}
                    </div>
                `).join('');
            } catch (err) {
                document.getElementById('fileContainer').innerHTML = '<div class="file-item" style="color:#ef4444">讀取失敗: ' + err + '</div>';
            }
        }

        async function previewFile(filename) {
            document.getElementById('modalFileName').innerText = '📄 ' + filename;
            document.getElementById('modalBody').innerText = '載入檔案內容中...';
            document.getElementById('viewModal').style.display = 'flex';
            try {
                const res = await fetch('/api/file-content?filename=' + encodeURIComponent(filename));
                const data = await res.json();
                if (data.status === 'success') {
                    document.getElementById('modalBody').innerText = data.content;
                } else {
                    document.getElementById('modalBody').innerText = '❌ 錯誤: ' + data.message;
                }
            } catch (err) {
                document.getElementById('modalBody').innerText = '❌ 讀取失敗: ' + err;
            }
        }

        function closeModal() {
            document.getElementById('viewModal').style.display = 'none';
        }

        fetchFiles();
    </script>
</body>
</html>
"""
    return html_content

if __name__ == "__main__":
    print("=" * 65)
    print("Class 6 AI Node Local File Access Service (Port 8888)")
    print("Local URL: http://127.0.0.1:8888")
    print("Tunnel Command: ngrok http 127.0.0.1:8888")
    print("=" * 65)
    uvicorn.run("app:app", host="127.0.0.1", port=8888, reload=True)
