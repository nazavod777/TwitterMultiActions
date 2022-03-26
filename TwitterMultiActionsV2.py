from pyuseragents import random as random_useragent
from requests import Session
from random import choice
from time import sleep
from msvcrt import getch
from os import system
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from json import loads


disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('TwitterMultiActions V2 | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


user_action = int(input('1. Массовые подписки\n2. Массовые ретвиты\n3. Массовые лайки\n4. Массовые комментарии кошелька под постом\nВведите номер вашего действия: '))
print('\n')

if user_action == 1:
	username_to_subscribe = str(input('Введите юзернейм профиля для подписки: ')).replace('@', '')

elif user_action == 4:
	tweet_url = str(input('Введите ссылку на твит: '))
	tweet_id = tweet_url.split('status/')[-1]

	tag_users = str(input('Нужно-ли отмечать друзей? (y/N): '))

	if tag_users in ('y', 'Y'):
		how_much_users_tag = int(input('Сколько друзей необходимо отметить?: '))
	
	need_phrase_for_comment = str(input('Нужно-ли добавить вашу фразу к комментарию? (y/N): '))

	if need_phrase_for_comment in ('y',' Y'):
		phrase_for_comment = str(input('Введите фразу к комментарию: '))

	wallets_txt_folder = str(input('Перетяните файл с кошельками: '))

	with open(wallets_txt_folder, 'r') as file:
		wallets_addresses = [row.strip() for row in file]

else:
	tweet_url = str(input('Введите ссылку на твит: '))
	tweet_id = tweet_url.split('status/')[-1]

user_sleep_option = str(input('Использовать задержку между выполнением действий? (y/N): '))

if user_sleep_option in ('y', 'Y'):
	user_time_to_sleep = int(input('Введите время в секундах для сна между действиями: '))

use_proxies = str(input('Использовать Proxy? (y/N): '))

if use_proxies in ('y', 'Y'):
	proxy_type = str(input('Введите тип Proxy (http // https // socks4 // socks5): '))
	proxy_folder = str(input('Перетяняти TXT файл с Proxies (user:pass@ip:port // ip:port): '))


with open('accounts.txt', 'r') as file:
	accounts_cookies = [row.strip() for row in file]

def random_proxy_from_file():

	with open(proxy_folder, 'r') as file:
		proxies = file.readlines()
		
	return (choice(proxies))


class Wrong_Response(BaseException):
	def __init__(self, message):
		self.message = message


class MainWork():

	def __init__(self, cookies_str, csrf_token):

		self.cookies_str = cookies_str
		self.session = Session()
		self.session.headers.update({'user-agent': random_useragent(), 'Origin': 'https://mobile.twitter.com', 'Referer': 'https://mobile.twitter.com/', 'x-twitter-active-user': 'yes', 'x-twitter-auth-type': 'OAuth2Session', 'x-twitter-client-language': 'en', 'content-type': 'application/json'})

		r = self.session.get('https://abs.twimg.com/responsive-web/client-web/main.f3ada2b5.js', verify=False)
		self.queryIdforSubscribe = r.text.split('",operationName:"TweetResultByRestId",operationType:"query",metadata:{featureSwitches:[]}}},fDBV:function(e,t){e.exports={queryId:"')[-1].split('"')[0]
		self.queryIdforRetweet = r.text.split('"/share","/terms","/tos","/transparency","/tweetbutton","/user_spam_reports"]}')[-1].split(',operationName:"CreateRetweet')[0].split('queryId:"')[-1].split('"')[0]
		self.queryIdforLike = r.text.split('"x/WR":function(e,t){e.exports={queryId:"')[-1].split('"')[0]
		self.queryIdforComment = r.text.split('operationName:"ListProductSubscriptions",operationType:"query"')[-1].split('operationName:"CreateTweet')[0].split('queryId:"')[-1].split('"')[0]
		self.quertIdforFollowers = r.text.split('QK8Q:function(e,t){e.exports={queryId:"')[-1].split('"')[0]
		bearer_token = 'Bearer '+r.text.split('const r="ACTION_FLUSH",i="ACTION_REFRESH')[-1].split(',l="d_prefs"')[0].split(',s="')[-1].split('"')[0]

		self.session.headers.update({'authorization': bearer_token, 'cookie': self.cookies_str, 'x-csrf-token': csrf_token})

		if use_proxies in ('y', 'Y'):
			random_proxy_str = random_proxy_from_file()
			self.session.proxies.update({'http': f'{proxy_type}://{random_proxy_str}', 'https': f'{proxy_type}://{random_proxy_str}'})


	def get_username(self):
		r = self.session.get('https://mobile.twitter.com/i/api/1.1/account/settings.json?include_mention_filter=true&include_nsfw_user_flag=true&include_nsfw_admin_flag=true&include_ranked_timeline=true&include_alt_text_compose=true&ext=ssoConnections&include_country_code=true&include_ext_dm_nsfw_media_filter=true&include_ext_sharing_audiospaces_listening_data_with_followers=true', verify=False)

		try:
			self.username = str(loads(r.text)['screen_name'])

		except Exception as error:
			response = r.text.replace('\n', '').replace('\r', '')
			logger.error(f'Ошибка при получении юзернейма: {str(error)}, ответ: {response}, строка: {self.cookies_str}')
			return False

		else:
			return True


	def mass_subs(self):
		for _ in range(3):
			try:
				r = self.session.get('https://mobile.twitter.com/i/api/graphql/'+self.queryIdforSubscribe+'/UserByScreenName?variables={"screen_name":"'+username_to_subscribe+'","withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}', headers = {'content-type': 'application/x-www-form-urlencoded'}, verify=False)
				rest_id = str(loads(r.text)['data']['user']['result']['rest_id'])
				
				r = self.session.post('https://mobile.twitter.com/i/api/1.1/friendships/create.json', data='include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&id='+rest_id, headers = {'content-type': 'application/x-www-form-urlencoded'}, verify=False)

				if r.status_code != 200:
					raise Wrong_Response('wrong_response')
				

			except Exception as error:

				logger.error(f'{self.username} | Ошибка при массовой подписке: {str(error)}')
			
			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовой подписке: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно подписался на {username_to_subscribe}')

				break


	def mass_retweets(self):
		
		for _ in range(3):
			try:
				r = self.session.post('https://mobile.twitter.com/i/api/graphql/'+self.queryIdforRetweet+'/CreateRetweet', headers={'content-type': 'application/json'}, json={"variables":"{\"tweet_id\":\""+tweet_id+"\",\"dark_request\":false}","queryId":""+self.queryIdforRetweet+""}, verify=False)

				if r.status_code != 200:
					raise Wrong_Response('wrong_response')

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовом ретвитинге: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовом ретвитинге: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно ретвитнул пост {tweet_url}')

				break


	def mass_likes(self):

		for _ in range(3):
			try:
				r = self.session.post('https://mobile.twitter.com/i/api/graphql/'+self.queryIdforLike+'/FavoriteTweet', headers={'content-type': 'application/json'}, json={"variables":"{\"tweet_id\":\""+tweet_id+"\",\"dark_request\":false}","queryId":""+self.queryIdforRetweet+""}, verify=False)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовом лайкинге: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовом лайкинге: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно лайкнул пост {tweet_url}')

				break

	def mass_comments(self, address):

		for _ in range(3):
			try:
				if tag_users in ('y', 'Y'):
					users_to_tag = []

					for _ in range(how_much_users_tag):
						first3 = ''.join([choice('abcdefghijklmnopqrstuvwxyz013456789' if i != 3 else 'abcdefghijklmnopqrstuvwxyz013456789') for i in range(3)])
						r = self.session.get('https://twitter.com/i/api/1.1/search/typeahead.json?q='+str(first3)+'&src=compose&result_type=users&context_text='+str(first3))
						users_to_tag.append('@'+loads(r.text)['users'][0]['screen_name'])

					if need_phrase_for_comment in ('y', 'Y'):
						fullmesage = ' \\n'.join(users_to_tag)+'\\n'+address+'\\n'+phrase_for_comment
					else:
						fullmesage = ' \\n'.join(users_to_tag)+'\\n'+address
				
				else:
					if need_phrase_for_comment in ('y', 'Y'):
						fullmesage = '\\n'+address+'\\n'+phrase_for_comment
					else:
						fullmesage = '\\n'+address

				r = self.session.post('https://mobile.twitter.com/i/api/graphql/'+self.queryIdforComment+'/CreateTweet', headers={'content-type': 'application/json'}, json={"variables":"{\"tweet_text\":\""+fullmesage+"\",\"reply\":{\"in_reply_to_tweet_id\":\""+tweet_id+"\",\"exclude_reply_user_ids\":[]},\"media\":{\"media_entities\":[],\"possibly_sensitive\":false},\"withDownvotePerspective\":false,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true,\"withSuperFollowsUserFields\":true,\"semantic_annotation_ids\":[],\"dark_request\":false,\"withUserResults\":true,\"withBirdwatchPivots\":false}","queryId":""+self.queryIdforComment+""}, verify=False)
		
			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовых комментариях: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовых комментариях: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно отправил комментарий для {tweet_url}')

				break

if __name__ == '__main__':
	clear()
	
	for current_cookies_str in accounts_cookies:

		if 'wallets_addresses' in globals() and len(wallets_addresses) > 0 or 'wallets_addresses' not in globals():

			csrf_token = current_cookies_str.split('ct0=')[-1].split(';')[0]

			main_worker_obj = MainWork(current_cookies_str, csrf_token)
			get_username = main_worker_obj.get_username()

			if get_username:

				if user_action == 1:
					main_worker_obj.mass_subs()

				elif user_action == 2:
					main_worker_obj.mass_retweets()

				elif user_action == 3:
					main_worker_obj.mass_likes()

				elif user_action == 4:

					main_worker_obj.mass_comments(wallets_addresses.pop(0))

		else:
			break


		if user_sleep_option in ('y', 'Y'):
			sleep(user_time_to_sleep)


	logger.success('Работа успешно завершена')
	print('\nPress Any Key To Exit..')
	getch()
	exit()
