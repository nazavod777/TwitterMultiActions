# -*- coding: utf8 -*-
from pyuseragents import random as random_useragent
from requests import Session, get
from random import choice, randint
from time import sleep, time
from msvcrt import getch
from os import system, listdir
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from json import loads, load
from bs4 import BeautifulSoup
from base64 import b64encode
from names import get_full_name, get_first_name, get_last_name
from multiprocessing.dummy import Pool
from re import match
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

disable_warnings()


def clear(): return system('cls')


logger.remove()
logger.add(stderr,
           format="<white>{time:HH:mm:ss}</white> | <level>"
           "{level: <8}</level> | <cyan>"
           "{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('TwitterMultiActions V2 | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n'
      'Donate (any evm) - 0xdd8185984AC02E5d9394a278d23271Fb1C9DC54c\n')

wallets_addresses = None
all_images_files = []

with open('countries.json', 'r', encoding='utf-8') as file:
    file_list = load(file)

files = [str(f.absolute())
         for f in Path('Cookies').glob("**/*")
         if Path(str(f.absolute())).suffix == '.txt']

with open('accounts.txt', 'r', encoding='utf-8') as file:
    accounts_cookies = file.read()\
                        .replace(''''"''', ''''\\"''')\
                        .replace('''"\'''', '''\\"\'''')\
                        .replace("'", '"')\
                        .replace("False", "false")\
                        .replace("True", "true")\
                        .replace("None", "null")\
                        .splitlines()

for current_folder in files:
    with open(current_folder, 'r', encoding='utf-8') as file:
        current_cookie = file.read().replace('	', ' ')

        if len(current_cookie) > 0:
            accounts_cookies.append(current_cookie)

logger.success(f'?????????????? ?????????????????? {len(accounts_cookies)} ??????????????????\n')

user_action = int(input('1. ???????????????? ????????????????\n'
                        '2. ???????????????? ??????????????????????\n'
                        '3. ???????????????? ??????????????\n'
                        '4. ???????????????? ??????????\n'
                        '5. ???????????????? ??????????????????????\n'
                        '6. ???????????????? ?????????? ????????????????????\n'
                        '7. ?????????????? ???????? ?? ?????????????? ????????????????\n'
                        '8. ???????????????? @username ???? ???????????? ????????????????\n'
                        '9. ???????????????? ???????????????? ???? ???????????? ????????????????\n'
                        '10. ???????????????? ???????????? ???? ???????????? ????????????????\n'
                        '11. ???????????????? ?????? ???? ???????????? ????????????????\n'
                        '12. ???????????????? ?????? ???? ???????????? ????????????????\n'
                        '13. ???????????????? ???????????????????????????? ???? ???????????? ????????????????\n'
                        '14. ???????????????? @username ?? ?????????????? ???????????????? ?? .txt\n'
                        '15. ???????????????????????????? ?????????? ?????????????? ???? ??????????????????\n'
                        '?????????????? ?????????? ???????????? ????????????????: '))
print('')

threads = int(input('Threads: '))

# ???????????????? ????????????????
if user_action == 1:
    usernames_to_subscribe_source = int(input('???????????????? ???????????? ?????????? @username ?????? ???????????????? '
                                              '(1 - ???????????? ??????????????; '
                                              '2 - ?????????????????????????? ???? ?????????????????? ????????????????): '))

    if usernames_to_subscribe_source == 1:
        username_to_subscribe = str(input('?????????????? @username ?????????????? '
                                          '(????????????????, ?????????????????? ?????????? ??????????????, ?????? ????????????????): '))\
                                          .replace('@', '')\
                                          .replace(' ', '')
        username_to_subscribe_list = username_to_subscribe.split(',')

    else:
        username_to_subscribe_length = int(input('?????????????? ???????????????????? ??????????????????, '
                                                 '???? ?????????????? ?????????? ??????????????????????: '))

# ???????????????? ??????????????????????
elif user_action == 2:
    username_to_subscribe = str(input('?????????????? @username ?????????????? '
                                      '(????????????????, ?????????????????? ?????????? ??????????????, ?????? ????????????????): '))\
                                      .replace('@', '')\
                                      .replace(' ', '')
    username_to_subscribe_list = username_to_subscribe.split(',')

# ???????????????? ?????????????? / ???????????????? ??????????
elif user_action in (3, 4):
    tweet_url = str(input('?????????????? ???????????? ???? ????????: '))
    tweet_id = tweet_url.split('status/')[-1]\
                        .split('/')[0]\
                        .split('?')[0]\
                        .split('&')[0]\
                        .replace(' ', '')

# ???????????????? ??????????????????????
elif user_action == 5:
    tweet_url = str(input('?????????????? ???????????? ???? ????????: '))
    tweet_id = tweet_url.split('status/')[-1]\
                        .split('/')[0].split('?')[0]\
                        .split('&')[0].replace(' ', '')

    tag_users = str(input('???????????????? ????????????? (y/N): ')).lower()

    if tag_users == 'y':
        how_much_users_tag = int(input('?????????????? ???????????? ???????????????????? ?????????????????: '))
        tag_users_source = int(input('???????????????? ???????????? ?????????????????? @username ?????? ???????? '
                                     '(1 - ?????????????????? ??????????????????; 2 - ???? .txt ??????????): '))

        if tag_users_source == 2:
            tag_users_folder = input('???????????????????? .txt ?? @username\'s ?????? ????????: ')

    need_phrase_for_comment = str(input('???????????????? ???????? ?????????? ?? ??????????????????????? (y/N): ')).lower()

    if need_phrase_for_comment == 'y':
        phrase_for_comment = str(input('?????????????? ??????????: '))

    need_send_wallet = str(input('???????????????????? ???????????????? ???? .txt ?? ??????????????????????? (y/N): ')).lower()

    if need_send_wallet == 'y':
        wallets_txt_folder = str(input('???????????????????? .txt ???????? ?? ????????????????????: '))

        with open(wallets_txt_folder, 'r', encoding='utf-8') as file:
            wallets_addresses = [row.strip() for row in file]

# ???????????????? ?????????? ????????????????????
elif user_action == 6:
    how_much_users_first_users_to_subs = input('???? ?????????????? ?????????? ?????????????????? ??????????????????????? '
                                               '(???????? ?????????? ?????????????????????? ?????????? ?????????? ???????????????????? - '
                                               '?????????????? Enter, ???????? ?????????????? 0): ')

    if len(how_much_users_first_users_to_subs) == 0 or how_much_users_first_users_to_subs == '0':
        how_much_users_first_users_to_subs = None

    else:
        how_much_users_first_users_to_subs: int

# ???????????????? ?????????? ?? ?????????????? ????????????????
elif user_action == 7:
    text_to_tweet_source = int(input('???????????????? ???????????? ???????????????? ???????????? ?????? ???????????????? ?????????? '
                                     '(1 - ???????????? ?? ??????????????; 2 - ???????????????????? ????????): '))

    if text_to_tweet_source == 2:
        text_to_tweet_folder = str(input('???????????????????? .txt ???????? ?? ?????????????? ?????? ??????????: '))
        text_to_tweet_type = int(input('???????????????? ???????????? ???????????????? ???????????? ?????? ?????????? ???? ?????????? '
                                       '(1 - ???? ?????????????? ?????? ?????????????? ????????????????; '
                                       '2 - ?????????????????? ?????????? ?????? ????????????????; '
                                       '3 - ?????????????????? ?????????? ?? ??????????????????): '))

        with open(text_to_tweet_folder, 'r', encoding='utf-8') as file:
            text_to_tweet_list = [row.strip() for row in file]

    else:
        current_text_to_tweet_input = str(input('?????????????? ?????????? ?????? ??????????: '))

# ?????????? @username ???? ???????????? ????????????????
elif user_action == 8:
    names_source = int(input('???????????????? ???????????? ?????????????? @usernames '
                             '(1 - ???? ??????????; '
                             '2 - ??????????????????): '))

    if names_source == 1:
        usernames_folder = str(input('???????????????????? .txt ???????? ?? @usernames: '))

# ?????????? ???????????????? ???? ???????????? ????????????????
elif user_action == 9:
    avatars_source = int(input('???????????????? ???????????? ???????????????? ???????????????? '
                               '(1 - ???? ??????????; '
                               '2 - ?????????????????? ?? thispersondoesnotexist.com): '))

    if avatars_source == 1:
        images_folder = str(input('???????????????????? ?????????? ?? ????????????????????: '))

# ?????????? ?????????????? ???? ???????????? ????????????????
elif user_action == 10:
    images_folder = str(input('???????????????????? ?????????? ?? ??????????????????: '))

# ?????????? ?????? ???? ???????????? ????????????????
elif user_action == 11:
    bio_source = str(input('???????????????????? .txt ???????? ?? ?????? (???????????? ?? ?????????? ????????????): '))

# ?????????? ?????????????? ???? ??????????????????
elif user_action == 15:
    folder_to_old_passwords = input('???????????????????? .txt ???????? ?? ???????????????? ???? ?????????????????? '
                                    '(?? ?????????????????????? 1??1 ?? cookies): ')

    with open(folder_to_old_passwords, 'r') as file:
        old_passwords_list = [row.strip() for row in file]

user_sleep_option = str(input('???????????????????????? ???????????????? ?????????? ?????????????????????? ????????????????? (y/N): ')).lower()

if user_sleep_option == 'y':
    user_time_to_sleep = int(input('?????????????? ?????????? ?? ???????????????? ?????? ?????? ?????????? ????????????????????: '))

use_proxies = str(input('???????????????????????? Proxy? (y/N): ')).lower()

if use_proxies == 'y':
    proxy_type = str(input('?????????????? ?????? Proxy (http; https; socks4; socks5): '))

    proxies = []


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def take_proxies(length):
    proxies = []

    while len(proxies) < length:
        with open('proxies.txt') as file:
            for row in file:
                proxies.append(row.strip())

    return(proxies[:length])


def get_all_images_in_folder():
    return(listdir(images_folder))


def get_random_bio_from_file():
    with open(bio_source, 'r', encoding='utf-8') as file:
        bio = file.readlines()

    return(choice(bio))


def get_random_username_from_file(length):
    with open(tag_users_folder, 'r', encoding='utf-8') as file:
        usernames = [row.strip() for row in file]

    return_usernames = [usernames.pop(randint(0, len(usernames) - 1))
                        for _ in range(length)]

    return(return_usernames)


def handle_errors(data):
    if not data.ok:
        raise Wrong_Response(data)

    try:
        if loads(data.text).get('errors'):
            if loads(data.text)['errors'][0]['message'] ==\
                    'Your account is suspended and is not permitted to access this feature.':
                raise Own_Account_Suspended('')
            else:
                raise Wrong_Response(data)

        reason = loads(data.text)['data']['user']['result']['reason']
        raise Account_Suspended(reason)

    except Exception:
        return


class Wrong_Response(BaseException):
    pass


class Wrong_UserAgent(BaseException):
    pass


class Account_Suspended(BaseException):
    pass


class Own_Account_Suspended(BaseException):
    pass


class App():
    def __init__(self, cookies_str, current_proxy):
        self.current_proxy = current_proxy
        self.cookies_str = cookies_str
        self.lang = ''
        self.session = Session()
        self.session.headers.update({
            'user-agent': random_useragent(),
            'Origin': 'https://mobile.twitter.com',
            'Referer': 'https://mobile.twitter.com/',
            'x-twitter-active-user': 'yes',
            'x-twitter-auth-type': 'OAuth2Session',
            'x-twitter-client-language': 'en',
            'content-type': 'application/json',
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7',
            })

        self.session_unblock = Session()
        self.session_unblock.headers.update({
            'accept': 'text/html,application/xhtml+xml,application/'
                      'xml;q=0.9,image/avif,image/webp,image/'
                      'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru,en;q=0.9,vi;q=0.8,es;q=0.7',
            'referer': 'https://twitter.com/i/flow/login',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': self.session.headers['user-agent']
        })

        if self.current_proxy:
            self.session.proxies.update({
                'http': f'{proxy_type}://{self.current_proxy}',
                'https': f'{proxy_type}://{self.current_proxy}'})

            self.session_unblock.proxies.update({
                'http': f'{proxy_type}://{self.current_proxy}',
                'https': f'{proxy_type}://{self.current_proxy}'})

    def get_random_avatar_from_web(self):
        r = get('https://thispersondoesnotexist.com/image')
        return(b64encode(r.content))

    def get_random_image_from_list(self, folder):
        global all_images_files

        if len(all_images_files) < 1:
            all_images_files = get_all_images_in_folder()

        random_file = choice(all_images_files)
        all_images_files.remove(random_file)

        return(b64encode(open(f'{folder}\\{random_file}', 'rb').read()))

    def get_random_usernames(self, length):
        users_list = []

        for _ in range(length):
            try:
                first3 = "".join([choice("abcdefghijklmnopqrstuvwxyz013456789")
                                  for _ in range(3)])
                r = self.session.get('https://twitter.com/i/api/1.1/'
                                     'search/typeahead.json?q='
                                     + str(first3) + '&src=compose&'
                                     'result_type=users&context_text=' + str(first3),
                                     verify=False)

                users_list.append('@' + loads(r.text)['users'][0]['screen_name'])

            except Exception:
                pass

        else:
            return(users_list)

    def get_values(self):
        for _ in range(15):
            try:
                r = self.session.get('https://twitter.com/home',
                                     verify=False)

                handle_errors(r)

                url_to_get_query_ids = BeautifulSoup(r.text, 'lxml')\
                    .find_all('link',
                              {'rel': 'preload', 'as': 'script', 'crossorigin': 'anonymous'})[-1]\
                    .get('href')

                r = self.session.get(url_to_get_query_ids,
                                     verify=False)

                handle_errors(r)

                self.queryIdforSubscribe = r.text.split('",operationName:"TweetResultByRestId')[0]\
                                                 .split('"')[-1]
                self.queryIdforRetweet = r.text.split('",operationName:"CreateRetweet')[0]\
                                               .split('"')[-1]
                self.queryIdforLike = r.text.split('",operationName:"FavoriteTweet')[0]\
                                            .split('"')[-1]
                self.queryIdforComment = r.text.split('",operationName:"CreateTweet"')[0]\
                                               .split('"')[-1]
                self.queryIdforFollowers = r.text.split('",operationName:"Followers')[0]\
                                                 .split('"')[-1]
                self.queryIdforUserByScreenName = r.text.split('",operationName:'
                                                               '"UserByScreenName')[0]\
                                                        .split('"')[-1]
                self.queryIdforCreateTweet = r.text.split('",operationName:"CreateTweet"')[0]\
                                                   .split('"')[-1]
                self.queryIdforDataSaverMode = r.text.split('"A",operationName:"DataSaverMode"')[0]\
                                                     .split('"')[-1]
                self.action_refresh = r.text.split('ACTION_REFRESH",i="')[-1]\
                                            .split('"')[0]
                bearer_token = 'Bearer ' + r.text.split('r="ACTION_FLUSH"')[-1]\
                                                 .split(',s="')[1]\
                                                 .split('"')[0]

                if match('^[??-????-??????a-zA-Z0-9._/"=%# |+,:\}\{\-\n\r]+ '
                         '[??-????-??????a-zA-Z0-9._/"=%# |+,:\}\{\-\n\r]+ '
                         '[??-????-??????a-zA-Z0-9._/"=%# |+,:\}\{\-\n\r]+ '
                         '[??-????-??????a-zA-Z0-9._/"=%# |+,:\}\{\-\n\r]+ '
                         '[??-????-??????a-zA-Z0-9._/"=%# |+,:\}\{\-\n\r]+ '
                         '[??-????-??????a-zA-Z0-9._/"=%# |+,:\}\{\-\n\r]+ '
                         '[??-????-??????a-zA-Z0-9._/"=%# |+,:\}\{\-\n\r]+',
                         self.cookies_str):

                    for current_cookie_value in self.cookies_str.split('\n'):
                        self.session.cookies[current_cookie_value.strip().split()[5]]\
                            = current_cookie_value.strip().split()[6]
                        self.session_unblock.cookies[current_cookie_value.strip().split()[5]]\
                            = current_cookie_value.strip().split()[6]

                        if current_cookie_value.strip().split()[5] == 'ct0':
                            csrf_token = current_cookie_value.strip().split()[6]

                        if current_cookie_value.strip().split()[5] == 'lang':
                            self.lang = current_cookie_value.strip().split()[6]

                elif self.cookies_str[:1] == '[' and self.cookies_str[-1:] == ']':
                    for current_cookie_value in \
                            loads('[' + self.cookies_str.split('[')[-1]
                                  .replace(''''"''', ''''\\"''')
                                  .replace('''"\'''', '''\\"\'''')
                                  .replace("'", '"')
                                  .replace("False", "false")
                                  .replace("True", "true")
                                  .replace("None", "null")):

                        self.session.cookies[current_cookie_value['name']]\
                             = current_cookie_value['value']

                        self.session_unblock.cookies[current_cookie_value['name']]\
                            = current_cookie_value['value']

                        if current_cookie_value['name'] == 'ct0':
                            csrf_token = current_cookie_value['value']

                        elif current_cookie_value['name'] == 'lang':
                            self.lang = current_cookie_value['value']

                else:
                    self.session.headers.update({'cookie': self.cookies_str})
                    self.session_unblock.headers.update({'cookie': self.cookies_str})
                    csrf_token = self.cookies_str.split('ct0=')[-1].split(';')[0]

                    self.lang = self.cookies_str.split('lang=')[-1].split(';')[0]

                self.session.headers.update({
                    'authorization': bearer_token,
                    'x-csrf-token': csrf_token})

                self.first_step()

            except Exception as error:
                logger.error(f'???????????? ?????? ?????????????????? ?????????????????? ????????????????????: {str(error)}')
                continue

            except Wrong_Response:
                new_ua = random_useragent()
                self.session.headers.update({'user-agent': new_ua})
                self.session_unblock.headers.update({'user-agent': new_ua})
                continue

            else:
                return(True)

        with open('errors.txt', 'a') as file:
            file.write(f'None | {self.cookies_str}\n')

        return(False)

    def first_step(self):
        self.session.post('https://api.twitter.com/1.1/jot/client_event.json',
                          data='category=perftown&'
                               'log=[{"description":"rweb:cookiesMetadata:load",'
                               '"product":"rweb",'
                               '"event_value":' + str(int(time())) + str(randint(0, 9)) + '}]',
                          headers={'content-type': 'application/x-www-form-urlencoded'},
                          verify=False)

        self.session.post('https://twitter.com/i/api/1.1/attribution/event.json',
                          json={"event": "open"},
                          headers={'content-type': 'application/json'},
                          verify=False)

        self.session.get('https://twitter.com/i/api/1.1/account/settings.json?'
                         'include_mention_filter=true&'
                         'include_nsfw_user_flag=true&'
                         'include_nsfw_admin_flag=true&'
                         'include_ranked_timeline=true&'
                         'include_alt_text_compose=true&'
                         'ext=ssoConnections&'
                         'include_country_code=true&'
                         'include_ext_dm_nsfw_media_filter=true&'
                         'include_ext_sharing_audiospaces_listening_data_with_followers=true',
                         verify=False)

        self.session.get('https://twitter.com/manifest.json',
                         verify=False)

        self.session.post('https://api.twitter.com/1.1/jot/client_event.json',
                          data='debug=true&'
                               'log=[{"_category_":"client_event",'
                               '"format_version":2,'
                               '"triggered_on":' + str(int(time()))
                               + str(randint(100, 999)) + ',"message":"normal/blue500/darker",'
                               '"items":[],'
                               '"event_namespace":{"page":"app","component":'
                               '"theme","action":"launch","client":"m5"},'
                               '"client_event_sequence_start_timestamp":'
                               + str(int(time())) + str(randint(100, 999)) +
                               ',"client_event_sequence_number":0,'
                               '"client_app_id":"' + str(self.action_refresh) + '"}]',
                          headers={'content-type': 'application/x-www-form-urlencoded'},
                          verify=False)

        self.session.get('https://twitter.com/i/api/2/badge_count/badge_count.json?'
                         'supports_ntab_urt=1',
                         verify=False)

        self.session.post('https://twitter.com/i/api/1.1/branch/init.json',
                          json={},
                          headers={'content-type': 'application/json'},
                          verify=False)

        self.session.get(f'https://twitter.com/i/api/graphql/{self.queryIdforDataSaverMode}'
                         '/DataSaverMode?variables={"device_id":"Windows/Chrome"}',
                         verify=False)

        sequenceStartTimestampMs = int(f'{int(time())}{random_with_N_digits(3)}')
        visibilityPctDwellStartMs = str(int(f'{int(time())}{random_with_N_digits(3)}')
                                        - int(random_with_N_digits(4)))
        visibilityPctDwellEndMs = str(int(visibilityPctDwellStartMs) - randint(0, 100))

        self.session.post('https://twitter.com/i/api/1.1/jot/ces/p2',
                          json={
                              "events": [
                                  {"sequenceStartTimestampMs": sequenceStartTimestampMs,
                                   "sequenceNumber": 0,
                                   "createdAtMs": sequenceStartTimestampMs,
                                   "event":
                                   {"behavioralEvent": {
                                    "v1":
                                    {"context":
                                     {"v1":
                                      {}},
                                     "action":
                                     {"impress":
                                      {"v2":
                                       {"minVisibilityPct": 0,
                                        "minDwellMs": 0,
                                        "visibilityPctDwellStartMs": ""
                                        + visibilityPctDwellStartMs + "",
                                        "visibilityPctDwellEndMs": ""
                                        + visibilityPctDwellEndMs + "",
                                        "count": 1}
                                       }
                                      },
                                        "targetView":
                                        {"v1":
                                         {"viewHierarchy":
                                          [{"statefulView":
                                           {"v1":
                                            {"viewType": "profile",
                                             "viewState":
                                             {"emptyness": {}}
                                             }
                                            }
                                            }]}
                                         }
                                     }
                                    }
                                    }
                                   }],
                              "header": {"createdAtMs": sequenceStartTimestampMs - randint(0, 100),
                                         "retryAttempt": 0}
                          },
                          verify=False)

    def unfreeze_account(self):
        for _ in range(15):
            try:
                r = self.session_unblock.get('https://twitter.com/account/access',
                                             verify=False)

                if '<p class="errorButton">'\
                   '<a href="https://help.twitter.com/using-twitter/twitter-supported-browsers">'\
                        in r.text:
                    raise Wrong_UserAgent('')

                handle_errors(r)

                authenticity_token = BeautifulSoup(r.text, 'lxml')\
                    .find('input', {'name': 'authenticity_token'}).get('value')
                assignment_token = BeautifulSoup(r.text, 'lxml')\
                    .find('input', {'name': 'assignment_token'}).get('value')

                r = self.session_unblock.post('https://twitter.com/account/access',
                                              headers={
                                                  'accept': 'text/html,application/'
                                                            'xhtml+xml,application/'
                                                            'xml;q=0.9,image/avif,image/'
                                                            'webp,image/apng,*/*;'
                                                            'q=0.8,application/'
                                                            'signed-exchange;'
                                                            'v=b3;q=0.9',
                                                  'content-type': 'application/'
                                                                  'x-www-form-urlencoded',
                                                  'origin': 'https://twitter.com',
                                                  'referer': 'https://twitter.com/account/access'},
                                              data=f'authenticity_token={authenticity_token}&'
                                                   f'assignment_token={assignment_token}&'
                                                   f'lang={self.lang}&'
                                                   'flow=',
                                              verify=False)

                handle_errors(r)

                if 'Due to a technical issue, we couldn\'t complete this request. '\
                        'Please try again.' in r.text:
                    raise Wrong_Response('')

            except Exception as error:
                logger.error(f'???????????? ?????? ???????????? ?????????????????? ????????????????????: {str(error)}')

            except Wrong_Response as error:
                response_formated = str(r.text.replace('\n', ''))
                logger.error(f'???????????? ?????? ???????????? ?????????????????? ????????????????????: '
                             f'{str(error)}, ?????? ????????????: {str(r.status_code)}, '
                             f'??????????: {response_formated}')

            except Wrong_UserAgent:
                new_ua = random_useragent()
                self.session_unblock.headers['user-agent'] = new_ua
                self.session.headers['user-agent'] = new_ua

            else:
                logger.success('?????????????????? ???????????????????? ?????????????? ??????????')

                return(True)

        return(False)

    def get_username(self, write_option):
        for _ in range(4):
            try:
                r = self.session.get('https://mobile.twitter.com/i/api/1.1/account/settings.json?'
                                     'include_mention_filter=true&'
                                     'include_nsfw_user_flag=true&'
                                     'include_nsfw_admin_flag=true&'
                                     'include_ranked_timeline=true&'
                                     'include_alt_text_compose=true&'
                                     'ext=ssoConnections&'
                                     'include_country_code=true&'
                                     'include_ext_dm_nsfw_media_filter=true&'
                                     'include_ext_sharing_audiospaces_lis'
                                     'tening_data_with_followers='
                                     'true',
                                     verify=False)

                handle_errors(r)

                self.username = str(loads(r.text)['screen_name'])

                if write_option:
                    with open('usernames.txt', 'a') as file:
                        file.write(f'{self.username}\n')

                    logger.success(f'?????????????? ?????????????? @username: {self.username}')

                else:
                    logger.success(f'{self.username} | ?????????????? ?????????????? ??????????????????????????')

            except Wrong_Response as error:
                if 'errors' in loads(r.text).keys():
                    if loads(r.text)['errors'][0]['message'] == 'Could not authenticate you':
                        logger.error(f'???????????????????? cookies: {self.cookies_str}')

                        with open('invalid_cookies.txt', 'a') as file:
                            file.write(f'{self.cookies_str}\n')

                        return(False, None)

                    elif loads(r.text)['errors'][0]['message'] == \
                            'To protect our users from spam and other malicious activity, '\
                            'this account is temporarily locked. '\
                            'Please log in to https://twitter.com to unlock your account.':

                        logger.error(f'{self.cookies_str} | ???????????????????? ?????????????????? ????????????????????, '
                                     f'???????????? ??????????')

                        if not self.unfreeze_account():
                            logger.error(f'{self.cookies_str} | '
                                         '???? ?????????????? ?????????? ?????????????????? ????????????????????')

                            with open('temporarily_locked_cookies.txt', 'a') as file:
                                file.write(f'{self.cookies_str}\n')

                            with open('temporarily_locked_proxies.txt', 'a') as file:
                                file.write(f'{self.current_proxy}\n')

                            return(False, None)

                        else:
                            continue

                else:
                    logger.error(f'???????????? ?????? ?????????????????? @username: {str(error)}, '
                                 f'?????? ????????????: {str(r.status_code)}, '
                                 f'??????????: {str(r.text)}, ????????????: {self.cookies_str}')

            except Exception as error:
                response = r.text.replace('\n', '').replace('\r', '')
                logger.error(f'???????????? ?????? ?????????????????? @username: {str(error)}, '
                             f'??????????: {response}, ????????????: {self.cookies_str}')

            else:
                return(True, self.username)

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

        return(False, None)

    def mass_follow(self, current_username_to_subscribe):
        if self.username != current_username_to_subscribe:
            for _ in range(3):
                try:
                    r = self.session.get(f'https://mobile.twitter.com/i/api/graphql/'
                                         f'{self.queryIdforUserByScreenName}'
                                         + '/UserByScreenName?variables='
                                         '{"screen_name":"' + current_username_to_subscribe
                                         .replace('@', '') + '",'
                                         '"withSafetyModeUserFields":true,'
                                         '"withSuperFollowsUserFields":true}',
                                         headers={
                                            'content-type': 'application/x-www-form-urlencoded'},
                                         verify=False)

                    handle_errors(r)

                    rest_id = str(loads(r.text)['data']['user']['result']['rest_id'])

                    r = self.session.post('https://mobile.twitter.com/i/api/1.1/'
                                          'friendships/create.json',
                                          data='include_profile_interstitial_type=1&'
                                               'include_blocking=1&'
                                               'include_blocked_by=1&'
                                               'include_followed_by=1&'
                                               'include_want_retweets=1&'
                                               'include_mute_edge=1&'
                                               'include_can_dm=1&'
                                               'include_can_media_tag=1&'
                                               'include_ext_has_nft_avatar=1&'
                                               'skip_status=1&'
                                               'user_id=' + rest_id,
                                          headers={
                                              'content-type': 'application/x-www-form-urlencoded'},
                                          verify=False)

                    handle_errors(r)

                except Exception as error:
                    logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????: {str(error)}')

                except Wrong_Response as error:
                    logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????: {str(error)}, '
                                 f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

                except Account_Suspended as error:
                    logger.error(f'{self.username} | ??????????????, ???? ?????????????? ???? ?????????????????? ?????????????????????? '
                                 f'??????????????????, ??????????????: {str(error)}')

                    return(1)

                except Own_Account_Suspended:
                    logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                    with open('suspended_accounts.txt', 'a') as file:
                        file.write(f'{self.username} | {self.cookies_str}\n')

                    with open('suspended_proxies.txt', 'a') as file:
                        file.write(f'{self.current_proxy}\n')

                    return

                else:
                    logger.success(f'{self.username} | '
                                   f'?????????????? ?????????????? ???????????????????? ???? {current_username_to_subscribe}')

                    return

            with open('errors.txt', 'a') as file:
                file.write(f'{self.username} | {self.cookies_str}\n')

    def mass_retweets(self):
        for _ in range(3):
            try:
                r = self.session.post(f'https://twitter.com/i/api/graphql/'
                                      f'{self.queryIdforRetweet}/CreateRetweet',
                                      headers={'content-type': 'application/json'},
                                      json={"variables":
                                            {"tweet_id": tweet_id,
                                             "dark_request": False},
                                            "queryId": self.queryIdforRetweet},
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ??????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ??????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ?????????????????? ???????? {tweet_url}')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def mass_likes(self):
        for _ in range(3):
            try:
                r = self.session.post(f'https://mobile.twitter.com/i/api/graphql/'
                                      f'{self.queryIdforLike}/FavoriteTweet',
                                      headers={'content-type': 'application/json'},
                                      json={"variables":
                                            {"tweet_id": tweet_id},
                                            "queryId": self.queryIdforRetweet},
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ?????????????? ???????? {tweet_url}')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def mass_comments(self, address):
        for _ in range(3):
            try:
                fullmesage = ''

                if tag_users == 'y':
                    users_to_tag = []

                    if tag_users_source == 1:
                        users_to_tag = self.get_random_usernames(how_much_users_tag)

                    else:
                        users_to_tag = get_random_username_from_file(how_much_users_tag)

                    fullmesage += '\n'.join(users_to_tag)

                if need_phrase_for_comment == 'y':
                    fullmesage += '\n' + phrase_for_comment

                if address:
                    fullmesage += '\n' + address

                r = self.session.post(f'https://twitter.com/i/api/graphql/'
                                      f'{self.queryIdforComment}/CreateTweet',
                                      headers={'content-type': 'application/json'},
                                      json={
                                            "variables": {
                                             "tweet_text": fullmesage,
                                             "reply": {
                                              "in_reply_to_tweet_id": tweet_id,
                                              "exclude_reply_user_ids": []
                                             },
                                             "media": {
                                              "media_entities": [],
                                              "possibly_sensitive": False
                                             },
                                             "withDownvotePerspective": False,
                                             "withReactionsMetadata": False,
                                             "withReactionsPerspective": False,
                                             "withSuperFollowsTweetFields": True,
                                             "withSuperFollowsUserFields": True,
                                             "semantic_annotation_ids": [],
                                             "dark_request": False
                                            },
                                            "features": {
                                                "dont_mention_me_view_api_enabled": True,
                                                "interactive_text_enabled": True,
                                                "responsive_web_edit_tweet_api_enabled": False,
                                                "responsive_web_enhance_cards_enabled": False,
                                                "responsive_web_uc_gql_enabled": False,
                                                "standardized_nudges_misinfo": False,
                                                "nudges_enabled": False,
                                                "vibe_tweet_context_enabled": False
                                            },
                                            "queryId": self.queryIdforComment
                                            },
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????????????: '
                             f'{str(error)}, ?????? ????????????: {str(r.status_code)}, '
                             f'??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | '
                               f'?????????????? ?????????????? ???????????????? ?????????????????????? ?????? {tweet_url}')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def mass_tweets(self, text_to_tweet):
        for _ in range(3):
            try:
                r = self.session.post(f'https://twitter.com/i/api/graphql/'
                                      f'{self.queryIdforCreateTweet}/CreateTweet',
                                      json={
                                            "variables": {
                                             "tweet_text": text_to_tweet,
                                             "media": {
                                              "media_entities": [],
                                              "possibly_sensitive": False
                                             },
                                             "withDownvotePerspective": False,
                                             "withReactionsMetadata": False,
                                             "withReactionsPerspective": False,
                                             "withSuperFollowsTweetFields": True,
                                             "withSuperFollowsUserFields": True,
                                             "semantic_annotation_ids": [],
                                             "dark_request": False
                                            },
                                            "features": {
                                                "dont_mention_me_view_api_enabled": True,
                                                "interactive_text_enabled": True,
                                                "responsive_web_edit_tweet_api_enabled": False,
                                                "responsive_web_enhance_cards_enabled": False,
                                                "responsive_web_uc_gql_enabled": False,
                                                "standardized_nudges_misinfo": False,
                                                "nudges_enabled": False,
                                                "vibe_tweet_context_enabled": False
                                            },
                                            "queryId": self.queryIdforCreateTweet
                                            },
                                      headers={'content-type': 'application/json'},
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ???????????????? ????????')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def mass_unfollow(self, current_username_to_subscribe):
        for _ in range(3):
            try:
                r = self.session.get(f'https://mobile.twitter.com/i/api/graphql/'
                                     f'{self.queryIdforUserByScreenName}'
                                     + '/UserByScreenName?variables='
                                     '{"screen_name":"' + current_username_to_subscribe
                                     + '","withSafetyModeUserFields":true,'
                                     '"withSuperFollowsUserFields":true}',
                                     headers={'content-type': 'application/x-www-form-urlencoded'},
                                     verify=False)

                handle_errors(r)

                rest_id = str(loads(r.text)['data']['user']['result']['rest_id'])

                r = self.session.post('https://twitter.com/i/api/1.1/friendships/destroy.json',
                                      headers={'content-type': 'application/x-www-form-urlencoded'},
                                      data='include_profile_interstitial_type=1&'
                                           'include_blocking=1&'
                                           'include_blocked_by=1&'
                                           'include_followed_by=1&'
                                           'include_want_retweets=1&'
                                           'include_mute_edge=1&'
                                           'include_can_dm=1&'
                                           'include_can_media_tag=1&'
                                           'include_ext_has_nft_avatar=1&'
                                           f'skip_status=1&user_id={rest_id}',
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????? ????????????????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ?????????????????? ???? '
                               f'{current_username_to_subscribe}')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def get_random_username(self):
        while True:
            try:
                r = get('https://story-shack-cdn-v2.glitch.me/'
                        'generators/username-generator?count=2')

                if not r.ok:
                    raise Wrong_Response(r)

                random_username = loads(r.text)['data'][0]['name'] + str(randint(1, 10000))

            except Exception as error:
                logger.error(f'{self.username} | ???? ?????????????? ???????????????? ?????????????????? @username, '
                             f'????????????: {str(error)}, ???????????? ?????? ??????')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???? ?????????????? ???????????????? ?????????????????? @username, '
                             f'????????????: {str(error)}, ?????? ????????????: '
                             f'{str(r.status_code)}, ??????????: {str(r.text)}, ???????????? ?????? ??????')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ?????????????????? @username: '
                               f'{random_username}')

                return(random_username)

    def change_username(self, new_username):
        for _ in range(3):
            try:
                if new_username:
                    random_username = new_username
                else:
                    random_username = self.get_random_username()

                r = self.session.post('https://twitter.com/i/api/1.1/account/settings.json',
                                      headers={'content-type': 'application/x-www-form-urlencoded'},
                                      data='include_mention_filter=true&'
                                           'include_nsfw_user_flag=true&'
                                           'include_nsfw_admin_flag=true&'
                                           'include_ranked_timeline=true&'
                                           'include_alt_text_compose=true&'
                                           f'screen_name={random_username}',
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? @username: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? @username: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                with open('new_usernames.txt', 'a') as file:
                    file.write(f'{random_username}:{self.cookies_str}\n')

                logger.success(f'{self.username} | ?????????????? ???????????? @username ???? {random_username}')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def change_avatar(self, avatar_data):
        for _ in range(3):
            try:
                r = self.session.post("https://twitter.com/i/api/1.1/"
                                      "account/update_profile_image.json",
                                      data={"image": avatar_data},
                                      headers={'content-type': 'application/x-www-form-urlencoded'},
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? ????????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? ????????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ???????????? ????????????????')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def change_banner(self, banner_data):
        for _ in range(3):
            try:
                r = self.session.post("https://twitter.com/i/api/1.1/"
                                      "account/update_profile_banner.json",
                                      data={"banner": banner_data},
                                      headers={'content-type': 'application/x-www-form-urlencoded'},
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? ??????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? ??????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ???????????? ????????????')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def change_profile(self, action):
        for _ in range(3):
            try:
                r = self.session.get('https://twitter.com/i/api/graphql/'
                                     'Bhlf1dYJ3bYCKmLfeEQ31A/UserByScreenName?variables='
                                     '{"screen_name":"' + self.username + '",'
                                     '"withSafetyModeUserFields":true,'
                                     '"withSuperFollowsUserFields":true}',
                                     verify=False)

                handle_errors(r)

                old_desc = loads(r.text)['data']['user']['result']['legacy']['description']
                old_name = loads(r.text)['data']['user']['result']['legacy']['name']
                old_location = loads(r.text)['data']['user']['result']['legacy']['location']

                if action == 'username':
                    random_full_name = choice([get_full_name(), get_first_name(), get_last_name()])
                    r = self.session.post('https://twitter.com/i/api/1.1/'
                                          'account/update_profile.json',
                                          headers={
                                              'content-type': 'application/x-www-form-urlencoded'},
                                          data=f'displayNameMaxLength=50&name={random_full_name}&'
                                               f'description={old_desc}&'
                                               f'location={old_location}'.encode('utf-8'),
                                          verify=False)

                elif action == 'bio':
                    new_bio = get_random_bio_from_file()
                    r = self.session.post('https://twitter.com/i/api/1.1/'
                                          'account/update_profile.json',
                                          headers={
                                              'content-type': 'application/x-www-form-urlencoded'},
                                          data=f'displayNameMaxLength=50&'
                                               f'name={old_name}&'
                                               f'description={new_bio}&'
                                               f'location={old_location}'.encode('utf-8'),
                                          verify=False)

                elif action == 'location':
                    new_location = choice(file_list['countries']['country'])['countryName']
                    r = self.session.post('https://twitter.com/i/api/1.1/'
                                          'account/update_profile.json',
                                          headers={
                                              'content-type': 'application/x-www-form-urlencoded'},
                                          data=f'displayNameMaxLength=50&'
                                               f'name={old_name}'
                                               f'&description={old_desc}'
                                               f'&location={new_location}'.encode('utf-8'),
                                          verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????????? ??????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ???????????????????? ??????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ???????????? ????????????????/??????/??????????????')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')

    def change_passwords(self, old_password):
        for _ in range(3):
            try:
                new_password = "".join([
                               choice("abcdefghijklmnopqrstuvwxyz"
                                      "ABCDEFGHIJKLMNOPQRSTUVWXYZ013456789_")
                               for _ in range(25)])

                r = self.session.post('https://twitter.com/i/api/i/account/change_password.json',
                                      headers={'content-type': 'application/x-www-form-urlencoded'},
                                      data=f'current_password={old_password}&'
                                           f'password={new_password}&'
                                           f'password_confirmation={new_password}',
                                      verify=False)

                handle_errors(r)

            except Exception as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? ????????????: {str(error)}')

            except Wrong_Response as error:
                logger.error(f'{self.username} | ???????????? ?????? ?????????? ????????????: {str(error)}, '
                             f'?????? ????????????: {str(r.status_code)}, ??????????: {str(r.text)}')

            except Own_Account_Suspended:
                logger.error(f'{self.username} | ?????? ?????????????? ????????????????????????')

                with open('suspended_accounts.txt', 'a') as file:
                    file.write(f'{self.username} | {self.cookies_str}\n')

                with open('suspended_proxies.txt', 'a') as file:
                    file.write(f'{self.current_proxy}\n')

                return

            else:
                logger.success(f'{self.username} | ?????????????? ?????????????? ???????????? ????????????')

                with open('change_password_result.txt', 'a') as file:
                    file.write(f'{self.username}:{new_password}\n')

                return

        with open('errors.txt', 'a') as file:
            file.write(f'{self.username} | {self.cookies_str}\n')


def start(current_cookies_str, proxy_str, wallet_address, changed_username):
    app = App(current_cookies_str, proxy_str)
    app_get_values_response = app.get_values()

    if app_get_values_response:
        if user_action == 14:
            get_username_status, current_username = app.get_username(True)

        else:
            get_username_status, current_username = app.get_username(None)

        if get_username_status:
            if user_action == 1:
                if usernames_to_subscribe_source == 2:
                    username_to_subscribe_list_local =\
                        app.get_random_usernames(username_to_subscribe_length)

                else:
                    username_to_subscribe_list_local = username_to_subscribe_list

                for username_to_subscribe in username_to_subscribe_list_local:
                    app.mass_follow(username_to_subscribe)

            elif user_action == 2:
                for username_to_subscribe in username_to_subscribe_list:
                    app.mass_unfollow(username_to_subscribe)

            elif user_action == 3:
                app.mass_retweets()

            elif user_action == 4:
                app.mass_likes()

            elif user_action == 5:
                app.mass_comments(wallet_address)

            elif user_action == 6:
                if len(all_usernames) > 1:
                    if not how_much_users_first_users_to_subs:
                        accounts_subs_length = len(all_usernames)

                    else:
                        accounts_subs_length = int(how_much_users_first_users_to_subs)

                    already_used = []

                    for _ in range(accounts_subs_length):
                        while True:
                            new_username = choice(all_usernames)

                            if new_username not in already_used:
                                already_used.append(new_username)

                                if app.mass_follow(new_username) == 1:
                                    continue

                                else:
                                    break

                        if user_sleep_option == 'y':
                            sleep(user_time_to_sleep)

            elif user_action == 7:
                if text_to_tweet_source == 2:
                    if text_to_tweet_type == 1:
                        current_text_to_tweet = text_to_tweet_list.pop(0)

                    elif text_to_tweet_type == 2:
                        current_text_to_tweet = text_to_tweet_list.pop(randint(0,
                                                                       len(text_to_tweet_list)-1))
                    else:
                        current_text_to_tweet = choice(text_to_tweet_list)

                else:
                    current_text_to_tweet = current_text_to_tweet_input

                app.mass_tweets(current_text_to_tweet)

            elif user_action == 8:
                app.change_username(changed_username)

            elif user_action == 9:
                if avatars_source == 2:
                    avatar_data = app.get_random_avatar_from_web()

                else:
                    avatar_data = app.get_random_image_from_list(images_folder)

                app.change_avatar(avatar_data)

            elif user_action == 10:
                banner_data = app.get_random_image_from_list(images_folder)

                app.change_banner(banner_data)

            elif user_action == 11:
                app.change_profile('bio')

            elif user_action == 12:
                app.change_profile('username')

            elif user_action == 13:
                app.change_profile('location')

            elif user_action == 15:
                app.change_passwords(old_passwords_list)

    if user_sleep_option == 'y':
        sleep(user_time_to_sleep)


def get_usernames(current_cookies_str, proxy_str):
    app = App(current_cookies_str, proxy_str)
    app_get_values_response = app.get_values()

    if app_get_values_response:
        get_username_status, current_username = app.get_username(None)

        if get_username_status:
            return(current_username)

        else:
            return(None)


if __name__ == '__main__':
    clear()
    pool = Pool(threads)

    if use_proxies == 'y':
        while len(proxies) < len(accounts_cookies):
            proxies = take_proxies(len(accounts_cookies))

    else:
        proxies = [None for _ in range(len(accounts_cookies))]

    wallets_addresses = [None for _ in range(len(accounts_cookies))]
    new_usernames_list = [None for _ in range(len(accounts_cookies))]

    if user_action == 6:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            results = executor.map(get_usernames, accounts_cookies, proxies)

        all_usernames = [result for result in results if result]

        if use_proxies == 'y':
            while len(proxies) < len(accounts_cookies):
                proxies = take_proxies(len(accounts_cookies))

        else:
            proxies = [None for _ in range(len(accounts_cookies))]

    if user_action == 8:
        if names_source == 1:
            with open(usernames_folder, 'r', encoding='utf-8') as file:
                new_usernames_list = [row.strip() for row in file]

    with ThreadPoolExecutor(max_workers=threads) as executor:
        executor.map(start, accounts_cookies, proxies, wallets_addresses, new_usernames_list)

    logger.success('???????????? ?????????????? ??????????????????')
    print('\nPress Any Key To Exit..')
    getch()
    exit()
