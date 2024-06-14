    with open("file.txt", "w", encoding="utf-8") as file:
        file.write(browser.get_soup().prettify())