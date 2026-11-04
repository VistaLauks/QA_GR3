import requests
import time

BASE_URL = "https://jsonplaceholder.typicode.com"

def demo_get_posts():
    print("\n--- GET /posts ---")
    resp = requests.get(f"{BASE_URL}/posts")
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Статус 200, получено {len(data)} постов")
        print(f"   Первый пост: {data[0]['title']}...")
    else:
        print(f"❌ Ошибка: {resp.status_code}")

def demo_get_single_post(post_id):
    print(f"\n--- GET /posts/{post_id} ---")
    resp = requests.get(f"{BASE_URL}/posts/{post_id}")
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Найден пост id={data['id']}, userId={data['userId']}")
        print(f"   Заголовок: {data['title']}...")
    else:
        print(f"❌ Не найден: {resp.status_code}")

def demo_create_post():
    print("\n--- POST /posts ---")
    payload = {"userId": 1, "title": "Новый пост", "body": "Тело поста"}
    resp = requests.post(f"{BASE_URL}/posts", json=payload)
    if resp.status_code == 201:
        data = resp.json()
        print(f"✅ Создан пост с id={data.get('id')}")
        print(f"   Заголовок: {data['title']}")
    else:
        print(f"❌ Ошибка: {resp.status_code}")

def demo_update_post():
    print("\n--- PUT /posts/1 ---")
    payload = {"id": 1, "userId": 1, "title": "Обновлён", "body": "Новое тело"}
    resp = requests.put(f"{BASE_URL}/posts/1", json=payload)
    if resp.status_code == 200:
        data = resp.json()
        print(f"✅ Обновлён: {data['title']}")
    else:
        print(f"❌ Ошибка: {resp.status_code}")

def demo_delete_post():
    print("\n--- DELETE /posts/1 ---")
    resp = requests.delete(f"{BASE_URL}/posts/1")
    if resp.status_code == 200:
        print("✅ Удалён (статус 200)")
    else:
        print(f"❌ Ошибка: {resp.status_code}")

def demo_response_time():
    print("\n--- Время ответа ---")
    start = time.time()
    requests.get(f"{BASE_URL}/posts/1")
    elapsed = time.time() - start
    print(f"✅ Время: {elapsed:.3f} сек")

if __name__ == "__main__":
    print("===== ТЕСТИРОВАНИЕ API =====")
    demo_get_posts()
    demo_get_single_post(1)
    demo_get_single_post(999)
    demo_create_post()
    demo_update_post()
    demo_delete_post()
    demo_response_time()