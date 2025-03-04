from bs4 import BeautifulSoup

"""
Есть 3 варианта аутпута:
dict - словарь с постом
None - ложный пост
"Error: TryAgain" - пост с ошибкой
"""


def process_post(post):
    soup = BeautifulSoup(post, "html.parser")
    # Проверяем, является ли пост предупреждением "Try Again"
    if soup.get_text() == "Something went wrong. Try reloading.Retry":
        return "Error: TryAgain"

    try:
        # Найдем кусок кода, отвечающий за инф. об аккаунте
        acc_info = soup.find("div", {"class": "css-175oi2r r-18u37iz r-1wbh5a2 r-1ez5h0i"})
        # Нашли кусок, но сама ссылка несколькими классами ниже в дереве, ищем следующий span, он всегда 1.
        user_link = acc_info.find("span").contents[0]
        processed_post = {"user_link": user_link}
    except AttributeError as e:
        print("WHOLE POST ERROR:", e)
        print("element in error:", soup.prettify())
        return None

    # Теперь найдем время и тоже добавим в словарь.
    try:
        timestamp = soup.find("time")
        processed_post["timestamp"] = timestamp["datetime"]
    except Exception as e:
        processed_post["timestamp"] = None
        print("TIME ERROR:", e)
        print("element in error:", soup.prettify())

    # Вытащим текст. Тут сложнее: все вставки по типу эмодзи и других шрифтов разделяют текст на много классов.
    # Но все они внутри span, просто забираем содержимое.
    try:
        text_part = soup.find("div", {"data-testid": "tweetText"})
        spans = text_part.find_all("span")
        text = ""
        for span in spans:
            text += span.get_text().strip()
        processed_post["text"] = text
    except Exception as e:
        processed_post["text"] = None
        print("TEXT ERROR:", e)

    # Найдем статистику (лайки, просмотры...)
    order = ["replies", "reposts", "likes", "views"]
    try:
        stats = soup.find_all("div", {"class": "css-175oi2r r-18u37iz r-1h0z5md r-13awgt0"})
        i = -1
        for stat in stats:
            i += 1
            n = stat.get_text()
            if not n:
                n = 0
            processed_post[order[i]] = n
    except Exception as e:
        for el in order:
            processed_post[el] = None
        print("STATS ERROR:", e)

    return processed_post
