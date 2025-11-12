import os
import json
import time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
HISTORY_DIR = os.path.join(BASE_DIR, "src", "WeatheriaBackend", "weatheria", "history")
INDEX_FILE = os.path.join(HISTORY_DIR, "index.json")

CHECK_INTERVAL = 5


def get_csv_files():
    """Obtiene los nombres de archivos CSV en la carpeta."""
    return sorted([
        f for f in os.listdir(HISTORY_DIR)
        if f.lower().endswith(".csv")
    ])


def update_index_json():
    """Actualiza el archivo index.json con la lista actual de CSV."""
    files = get_csv_files()
    data = {"files": files}

    with open(INDEX_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"index.json actualizado con {len(files)} archivos.")


def watch_folder():
    """Monitorea continuamente la carpeta y actualiza si hay cambios."""
    print("Monitoreando cambios en:", HISTORY_DIR)
    last_files = set()

    while True:
        try:
            current_files = set(get_csv_files())
            if current_files != last_files:
                update_index_json()
                last_files = current_files
            time.sleep(CHECK_INTERVAL)
        except KeyboardInterrupt:
            print("\nMonitoreo detenido.")
            break
        except Exception as e:
            print("Error:", e)
            time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    if not os.path.exists(HISTORY_DIR):
        os.makedirs(HISTORY_DIR)
    watch_folder()
