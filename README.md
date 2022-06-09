# TwitterMultiActions

## Установка:

> переносим все файлы в папку, в пути не должно быть кириллицы и пробелов

1. <kbd>Win</kbd> + <kbd>R</kbd> -> `cmd`
2. `cd /d ДиректорияСоСкриптом`
    example: `cd /d C\:TwitterMultiActions`
3. `pip install -r requirements.txt`
4. `python TwitterMultiActionsV2.py`

В [`accounts.txt`](accounts.txt) вписываем куки от аккаунтов, каждый с новой строки

## Настройка Cookies

Если вы используеет NetScape Cookies - создаете `.txt` файл под каждые куки в папке Cookies. Можете раскидать файлы в папке Cookies как вам удобно, бот найдет все `.txt` файлы в папке

При использовании прокси и одновременно двух типов Cookie (_netscape_ + _json/str_) приоритет соотношения прокси:куки будет передан _json/str_, а уже после _netscape_, т.е напр. если вы имеете 10 прокси, 5 _netscape cookies_ и 5 _json cookies_, то первые 5 прокси будут использоваться для _json cookies_, а слеующие 5 для _netscape_

Берем их из __Dev Tools__ в браузере (<kbd>F12</kbd>) и вкладки __Network__ (само слово `cookie` копировать не нужно)

Если прокси будут не работать - пробуйте менять тип прокси (с `https` на `http`)
