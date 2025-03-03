# 使用 Python 3.10 官方映像檔
FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝相依套件
COPY requirements.txt .

# 建立獨立的虛擬環境（避免污染系統環境）
RUN pip install --no-cache-dir -r requirements.txt

# 預設執行 bot
CMD ["python", "main.py"]
