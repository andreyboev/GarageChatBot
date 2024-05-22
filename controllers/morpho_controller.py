import asyncio
from playwright.async_api import async_playwright

consonants = [u'б', u'в', u'г', u'д', u'ж', u'з', u'й', u'к',
              u'л', u'м', u'н', u'п', u'р', u'с', u'т', u'ф', u'х', u'ц', u'ч', u'ш', u'щ']
thud = [u'к', u'п', u'с', u'т', u'ф', u'х', u'ц', u'ч', u'ш', u'щ']
vowels = [u'а', u'у', u'о', u'ы', u'и', u'э', u'я', u'ю', u'ё', u'е']


def split2words(line):
    i = 0
    result = ''
    word = ''
    while i < len(line):
        c = line[i]
        if is_consonant(c) or is_vowel(c) \
                or c == u'ь' or c == u'Ь' or c == u'ъ' or c == u'Ъ':
            word += c
        else:
            if len(word) > 0:
                if len(word) <= 2:
                    result += word
                else:
                    result += split2syllables(word)
                word = ''
            result += c
        i += 1
    print(result.strip())


def split2syllables(word):
    splited = ''
    slog = ''
    i = 0
    # v = False
    scount = vowel_count(word)
    if scount == 1:
        return word

    while i < len(word):
        c = word[i]
        # добавляем букву в слог
        slog += c
        # если гласная
        if is_vowel(c):
            # смотрим что идет после
            # есть буквы
            if i + 1 < len(word):
                c1 = word[i + 1]
                # если согласная
                if is_consonant(c1):
                    # если последняя в слове - добавляем в слог и выходим
                    if i + 1 >= len(word) - 1:
                        slog += word[i + 1]
                        i += 1
                    else:
                        # не последняя,запоминем проверяем что идет после нее
                        c2 = word[i + 2]
                        # если идет Й и следом согласный - добавляем в слог
                        if (c1 == u'й' or c1 == u'Й') and is_consonant(c2):
                            slog += c1
                            i += 1
                        # если после звонкой не парной идет глухой согласный - добавляем в слог
                        elif (c1 in [u'м', u'н', u'р', u'л'] or c1 in [u'М', u'Н', u'Р', u'Л']) and is_thud(c2):
                            slog += c1
                            i += 1
                        elif i + 2 >= len(word) - 1 and (c2 == u'ь' or c2 == u'Ь' or c2 == u'ъ' or c2 == u'Ъ'):
                            # заканчивается на мягкий
                            i += 2
                            slog += c1 + c2
            splited += slog
            if i + 1 < len(word):
                splited += '-'
            slog = ''
        i += 1
    return splited


def vowel_count(word):
    cnt = 0
    for c in word:
        if is_vowel(c):
            cnt += 1


def is_consonant(char):
    x = char.lower()[0]
    for c in consonants:
        if c == x:
            return True


def is_thud(char):
    x = char.lower()[0]
    for c in thud:
        if c == x:
            return True


def is_vowel(char):
    x = char.lower()[0]
    for c in vowels:
        if c == x:
            return True
    return False

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Log

async def create_rhyme(text: str):
    '''syllables = split2syllables(word).split('-')
    if len(syllables) == 1 and len(syllables[0]) == 0:
        return f'хуйня'
    if len(syllables) == 1:
        return f'хуе{"".join(syllables)}'
    return f"хуе{"".join(syllables[1:])}"
    '''
    '''options = webdriver.FirefoxOptions()
    options.add_argument('headless')
    #options.add_argument('remote-debugging-pipe')
    driver = webdriver.Firefox(options=options)
    driver.get('https://maximal.github.io/reduplicator/#')
    element = driver.find_element(By.ID, "inp-text")
    element.clear()
    element.send_keys(text, Keys.ENTER)
    res_element = driver.find_element(By.ID, "hui-result")
    return res_element.text'''
    async with (async_playwright() as pw):
        browser = await pw.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto('https://maximal.github.io/reduplicator/#')
        input_element = await page.query_selector("#inp-text")
        await input_element.fill('')
        await input_element.type(text, delay=0)
        await page.keyboard.press("Enter")
        result_element = await page.query_selector("#hui-result")
        result = await result_element.inner_text()
        await browser.close()

    return result

import asyncio
print(asyncio.run(create_rhyme('Пень')))
#print(create_rhyme("Пень"))