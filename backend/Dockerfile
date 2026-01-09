FROM python:3.11

WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Python依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのソースをコピー
COPY . .

# DigiCert証明書（本番環境用、開発時はコメントアウト）
# COPY DigiCertGlobalRootG2.crt.pem /usr/local/share/ca-certificates/DigiCertGlobalRootG2.crt
# RUN update-ca-certificates

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]