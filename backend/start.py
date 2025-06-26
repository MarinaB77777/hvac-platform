import os
import uvicorn
import shutil

# ✅ Просто проверяем путь
tesseract_path = shutil.which("tesseract")
print(f"🔍 Проверка tesseract path: {tesseract_path}")

if not tesseract_path:
    print("❗️tesseract не найден в PATH, указываем вручную")
    os.environ["TESSERACT_CMD"] = "/usr/bin/tesseract"
else:
    print(f"✅ Используется tesseract: {tesseract_path}")
    os.environ["TESSERACT_CMD"] = tesseract_path

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port)
