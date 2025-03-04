import json


def clear_file(project_name):
    with open(f"{project_name}_processed_posts.json", "w", encoding="utf-8") as f:
        f.truncate(0)
    print("Данные очищены")


def check_content(project_name):
    with open(f"{project_name}_processed_posts.json", "r", encoding="utf-8") as f:
        content = [json.loads(line.strip()) for line in f]
    for c in content:
        print(c)
        pass
    print()
    print(f"Всего {len(content)} элементов")


def clear_duplicates(project_name):
    with open(f"{project_name}_processed_posts.json", "r", encoding="utf-8") as f:
        unique_posts = {json.dumps(json.loads(line.strip()), sort_keys=True) for line in f}

    with open(f"{project_name}_processed_posts.json", "w", encoding="utf-8") as f:
        for post in unique_posts:
            f.write(post + "\n")

    print("Очистка от дубликатов завершена!")
