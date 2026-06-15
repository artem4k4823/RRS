import fastfeedparser


feed = fastfeedparser.parse('https://habr.com/ru/rss/hub/python/all/')

for entry in feed.entries:
    print(entry.title)
    print(entry.link)
    print(entry.published)  