import os
import uvicorn
import subprocess


# 🛠 Установка Tesseract, если он не установлен
def install_tesseract_if_missing():
    try:
        result = subprocess.run(["which", "tesseract"], capture_output=True, text=True)
        if result.returncode != 0:
            print("🔧 Tesseract не найден. Устанавливаем...")
            subprocess.run(
                ["apt-get", "update"], check=True
            )
            subprocess.run(
                ["apt-get", "install", "-y", "tesseract-ocr"], check=True
            )
            print("✅ Tesseract успешно установлен")
        else:
            print(f"✅ Tesseract найден: {result.stdout.strip()}")
    except Exception as e:
        print(f"🔥 Ошибка при установке Tesseract: {e}")

install_tesseract_if_missing()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
