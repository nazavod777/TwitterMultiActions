# TwitterMultiActions

### Установка:

\# переносим все файлы в папку, в пути не должно быть кириллицы и пробелов

1. win+r -> cmd
2. cd /d ДиректорияСоСкриптом
ex: cd /d C\:TwitterMultiActions
3. pip install -r requirements.txt
4. python TwitterMultiActionsV2.py

В accounts.txt вписываем куки от аккаунтов, каждый с новой строки
Если вы используеет NetScape Cookies - создаете .txt файл под каждые куки в папке Cookies. Можете раскидать файлы в папке Cookies как вам удобно, бот найдет все .txt файлы в папке
При использовании прокси и одновременно двух типов Cookie (netscape + json/str) приоритет соотношения прокси:куки будет передан json/str, а уже после netscape, т.е напр. если вы имеете 10 прокси, 5 netscape cookies и 5 json cookies, то первые 5 прокси будут использоваться для json cookies, а слеующие 5 для netscape
Берем их из F12 в браузере и вкладки Network (само слово 'cookie' копировать не нужно)

Если прокси будут не работать - пробуйте менять тип прокси (с https на http)
