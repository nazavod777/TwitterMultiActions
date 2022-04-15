# -*- coding: utf-8 -*-
from pyuseragents import random as random_useragent
from requests import Session, get, post
from random import choice, randint
from time import sleep
from msvcrt import getch
from os import system, listdir
from ctypes import windll
from urllib3 import disable_warnings
from loguru import logger
from sys import stderr, exit
from json import loads
from bs4 import BeautifulSoup
from base64 import b64encode
from names import get_full_name

disable_warnings()
def clear(): return system('cls')
logger.remove()
logger.add(stderr, format="<white>{time:HH:mm:ss}</white> | <level>{level: <8}</level> | <cyan>{line}</cyan> - <white>{message}</white>")
windll.kernel32.SetConsoleTitleW('TwitterMultiActions V2 | by NAZAVOD')
print('Telegram channel - https://t.me/n4z4v0d\n')


with open('accounts.txt', 'r', encoding = 'utf-8') as file:
	accounts_cookies = [row.strip() for row in file]


user_action = int(input('1. Массовые подписки\n2. Массовый анфолловинг\n3. Массовые ретвиты\n4. Массовые лайки\n5. Массовые комментарии\n6. Подписка между аккаунтами\n7. Сделать твит с каждого аккаунта\n8. Изменить @username на каждом аккаунте\n9. Изменить аватарку на каждом аккаунте\n10. Изменить баннер на каждом аккаунте\n11. Изменить БИО на каждом аккаунте\n12. Изменить имя на каждом аккаунте\nВведите номер вашего действия: '))
print('')

wallets_addresses = True
all_images_files = []

if user_action in (1, 2):
	username_to_subscribe = str(input('Введите @username профиля (профилей, разделять через запятую, без пробелов): ')).replace('@', '').replace(' ', '')
	username_to_subscribe_list = username_to_subscribe.split(',')

elif user_action == 5:
	tweet_url = str(input('Введите ссылку на твит: '))
	tweet_id = tweet_url.split('status/')[-1].split('/')[0].split('?')[0].split('&')[0].replace(' ', '')

	tag_users = str(input('Отмечать друзей? (y/N): ')).lower()

	if tag_users == 'y':
		how_much_users_tag = int(input('Сколько друзей необходимо отметить?: '))
	
	need_phrase_for_comment = str(input('Добавить вашу фразу к комментарию? (y/N): ')).lower()

	if need_phrase_for_comment == 'y':
		phrase_for_comment = str(input('Введите фразу: '))

	need_send_wallet = str(input('Отправлять кошельки из .txt в комментарии? (y/N): ')).lower()

	if need_send_wallet == 'y':
		wallets_txt_folder = str(input('Перетяните .txt файл с кошельками: '))

		with open(wallets_txt_folder, 'r', encoding = 'utf-8') as file:
			wallets_addresses = [row.strip() for row in file]

elif user_action == 7:
	text_to_tweet_source = int(input('Выберите способ загрузка текста для отправки твита (1 - ввести в консоль; 2 - перетянуть файл): '))

	if text_to_tweet_source == 2:
		text_to_tweet_folder = str(input('Перетяните .txt файл с текстом для твита: '))
		text_to_tweet_type = int(input('Выберите способ загрузки текста для твита из файла (1 - по порядку для каждого аккаунта; 2 - случайный текст без повторов; 3 - случайный текст с повторами): '))

	else:
		current_text_to_tweet = str(input('Введите текст для твита: '))

	with open(text_to_tweet_folder, 'r', encoding = 'utf-8') as file:
		text_to_tweet_list = [row.strip() for row in file]

elif user_action in (3, 4):
	tweet_url = str(input('Введите ссылку на твит: '))
	tweet_id = tweet_url.split('status/')[-1].split('/')[0].split('?')[0].split('&')[0].replace(' ', '')

elif user_action == 9:
	avatars_source = int(input('Выберите способ загрузки аватарок (1 - из файла; 2 - случайные с thispersondoesnotexist.com): '))

	if avatars_source == 1:
		images_folder = str(input('Перетяните ПАПКУ с аватарками: '))

elif user_action == 10:
	images_folder = str(input('Перетяните ПАПКУ с баннерами: '))

elif user_action == 11:
	bio_source = str(input('Перетяните .txt файл с БИО (каждый с новой строки): '))

user_sleep_option = str(input('Использовать задержку между выполнением действий? (y/N): ')).lower()

if user_sleep_option == 'y':
	user_time_to_sleep = int(input('Введите время в секундах для сна между действиями: '))

use_proxies = str(input('Использовать Proxy? (y/N): ')).lower()

if use_proxies == 'y':
	proxy_type = str(input('Введите тип Proxy (http; https; socks4; socks5): '))
	proxy_folder = str(input('Перетяните .txt файл с Proxies (user:pass@ip:port; ip:port): '))


def random_proxy_from_file():
	with open(proxy_folder, 'r', encoding = 'utf-8') as file:
		proxies = file.readlines()
		
	return(choice(proxies))

def get_all_images_in_folder():
	return(listdir(images_folder))

def get_random_bio_from_file():
	with open(bio_source, 'r', encoding = 'utf-8') as file:
		bio = file.readlines()

	return(choice(bio))

class Wrong_Response(BaseException):
	def __init__(self, message):
		self.message = message


class MainWork():
	def __init__(self, cookies_str, csrf_token):
		self.cookies_str = cookies_str
		self.session = Session()
		self.session.headers.update({'user-agent': random_useragent(), 'Origin': 'https://mobile.twitter.com', 'Referer': 'https://mobile.twitter.com/', 'x-twitter-active-user': 'yes', 'x-twitter-auth-type': 'OAuth2Session', 'x-twitter-client-language': 'en', 'content-type': 'application/json'})

		if use_proxies == 'y':
			random_proxy_str = random_proxy_from_file()
			self.session.proxies.update({'http': f'{proxy_type}://{random_proxy_str}', 'https': f'{proxy_type}://{random_proxy_str}'})

		while True:
			try:
				r = self.session.get('https://twitter.com/home', verify = False)

				if not r.ok:
					raise Wrong_Response(r)

				url_to_get_query_ids = BeautifulSoup(r.text, 'lxml').find_all('link', {'rel': 'preload', 'as': 'script', 'crossorigin': 'anonymous'})[-1].get('href')
				r = self.session.get(url_to_get_query_ids, verify = False)
				self.queryIdforSubscribe = r.text.split('",operationName:"TweetResultByRestId')[0].split('"')[-1]
				self.queryIdforRetweet = r.text.split('",operationName:"CreateRetweet')[0].split('"')[-1]
				self.queryIdforLike = r.text.split('",operationName:"FavoriteTweet')[0].split('"')[-1]
				self.queryIdforComment = r.text.split('",operationName:"CreateTweet"')[0].split('"')[-1]
				self.queryIdforFollowers = r.text.split('",operationName:"Followers')[0].split('"')[-1]
				self.queryIdforUserByScreenName = r.text.split('",operationName:"UserByScreenName')[0].split('"')[-1]
				self.queryIdforCreateTweet = r.text.split('",operationName:"CreateTweet"')[0].split('"')[-1]
				bearer_token = 'Bearer ' + r.text.split('r="ACTION_FLUSH"')[-1].split(',s="')[1].split('"')[0]

				self.session.headers.update({'authorization': bearer_token, 'cookie': self.cookies_str, 'x-csrf-token': csrf_token})

			except Exception as error:
				logger.error(f'Ошибка при получении начальных параметров: {str(error)}')
				continue

			except Wrong_Response as error:
				self.session.headers.update({'user-agent': random_useragent()})
				continue

			else:
				break

	def get_username(self):
		for _ in range(3):
			r = self.session.get('https://mobile.twitter.com/i/api/1.1/account/settings.json?include_mention_filter=true&include_nsfw_user_flag=true&include_nsfw_admin_flag=true&include_ranked_timeline=true&include_alt_text_compose=true&ext=ssoConnections&include_country_code=true&include_ext_dm_nsfw_media_filter=true&include_ext_sharing_audiospaces_listening_data_with_followers=true', verify=False)

			try:
				if not loads(r.text).get('errors'):
					self.username = str(loads(r.text)['screen_name'])
				
				else:
					raise Wrong_Response(r)

			except Exception as error:
				response = r.text.replace('\n', '').replace('\r', '')
				logger.error(f'Ошибка при получении @username: {str(error)}, ответ: {response}, строка: {self.cookies_str}')

			except Wrong_Response as error:
				logger.error(f'Ошибка при получении @username: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}, строка: {self.cookies_str}')

			else:
				return(True, self.username)

		return(False, None)

	def mass_follow(self, current_username_to_subscribe):
		if self.username != current_username_to_subscribe:
			for _ in range(3):
				try:
					r = self.session.get(f'https://mobile.twitter.com/i/api/graphql/{self.queryIdforUserByScreenName}' + '/UserByScreenName?variables={"screen_name":"' + current_username_to_subscribe + '","withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}', headers = {'content-type': 'application/x-www-form-urlencoded'}, verify = False)

					if not r.ok:
						raise Wrong_Response(r)

					rest_id = str(loads(r.text)['data']['user']['result']['rest_id'])
					
					r = self.session.post('https://mobile.twitter.com/i/api/1.1/friendships/create.json', data='include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&user_id=' + rest_id, headers = {'content-type': 'application/x-www-form-urlencoded'}, verify=False)

					if not r.ok:
						raise Wrong_Response(r)
					
				except Exception as error:
					logger.error(f'{self.username} | Ошибка при массовой подписке: {str(error)}')
				
				except Wrong_Response as error:
					logger.error(f'{self.username} | Ошибка при массовой подписке: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

				else:
					logger.success(f'{self.username} | Аккаунт успешно подписался на {current_username_to_subscribe}')

					return

	def mass_retweets(self):
		for _ in range(3):
			try:
				r = self.session.post(f'https://twitter.com/i/api/graphql/{self.queryIdforRetweet}/CreateRetweet', headers={'content-type': 'application/json'}, json= {"variables":"{\"tweet_id\":\"" + tweet_id + "\",\"dark_request\":false}","queryId":"" + self.queryIdforRetweet + ""}, verify = False)

				if not r.ok != 200:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовом ретвите: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовом ретвите: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно ретвитнул пост {tweet_url}')

				return

	def mass_likes(self):
		for _ in range(3):
			try:
				r = self.session.post(f'https://mobile.twitter.com/i/api/graphql/{self.queryIdforLike}/FavoriteTweet', headers = {'content-type': 'application/json'}, json = {"variables":"{\"tweet_id\":\"" + tweet_id+"\",\"dark_request\":false}","queryId":"" + self.queryIdforRetweet + ""}, verify = False)

				if not r.ok:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовом лайкинге: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовом лайкинге: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно лайкнул пост {tweet_url}')

				return

	def mass_comments(self, address):
		for _ in range(3):
			try:
				fullmesage = ''

				if tag_users == 'y':
					users_to_tag = []

					for _ in range(how_much_users_tag):
						first3 = "".join([choice("abcdefghijklmnopqrstuvwxyz013456789") for _ in range(3)])
						r = self.session.get('https://twitter.com/i/api/1.1/search/typeahead.json?q=' + str(first3) + '&src=compose&result_type=users&context_text=' + str(first3))
						users_to_tag.append('@' + loads(r.text)['users'][0]['screen_name'])

					fullmesage += '\\n'.join(users_to_tag)

				if need_phrase_for_comment == 'y':
					fullmesage += '\\n' + phrase_for_comment

				if address:
					fullmesage += '\\n' + address

				r = self.session.post(f'https://twitter.com/i/api/graphql/{self.queryIdforComment}/CreateTweet', headers = {'content-type': 'application/json'}, json = {"variables":"{\"tweet_text\":\"" + fullmesage + "\",\"reply\":{\"in_reply_to_tweet_id\":\"" + tweet_id + "\",\"exclude_reply_user_ids\":[]},\"media\":{\"media_entities\":[],\"possibly_sensitive\":false},\"withDownvotePerspective\":false,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true,\"withSuperFollowsUserFields\":true,\"semantic_annotation_ids\":[],\"dark_request\":false,\"withUserResults\":true,\"withBirdwatchPivots\":false}","queryId":"" + self.queryIdforComment + ""}, verify = False)

				if not r.ok:
					raise Wrong_Response(r)
		
			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовых комментариях: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовых комментариях: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно отправил комментарий для {tweet_url}')

				return
	
	def mass_tweets(self, text_to_tweet):
		for _ in range(3):
			try:
				r = self.session.post(f'https://twitter.com/i/api/graphql/{self.queryIdforCreateTweet}/CreateTweet', json = {"variables":"{\"tweet_text\":\"" + text_to_tweet + "\",\"media\":{\"media_entities\":[],\"possibly_sensitive\":false},\"withDownvotePerspective\":false,\"withReactionsMetadata\":false,\"withReactionsPerspective\":false,\"withSuperFollowsTweetFields\":true,\"withSuperFollowsUserFields\":true,\"semantic_annotation_ids\":[],\"dark_request\":false,\"__fs_dont_mention_me_view_api_enabled\":true,\"__fs_interactive_text_enabled\":true,\"__fs_responsive_web_uc_gql_enabled\":false}","queryId":"" + self.queryIdforCreateTweet + ""}, verify = False)

				if not r.ok:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовых твитах: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовых твитах: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно отправил твит')

				return

	def mass_unfollow(self, current_username_to_subscribe):
		for _ in range(3):
			try:
				r = self.session.get(f'https://mobile.twitter.com/i/api/graphql/{self.queryIdforUserByScreenName}' + '/UserByScreenName?variables={"screen_name":"'+ current_username_to_subscribe + '","withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}', headers = {'content-type': 'application/x-www-form-urlencoded'}, verify = False)

				if not r.ok:
					raise Wrong_Response(r)

				rest_id = str(loads(r.text)['data']['user']['result']['rest_id'])

				r = self.session.post('https://twitter.com/i/api/1.1/friendships/destroy.json', headers = {'content-type': 'application/x-www-form-urlencoded'}, data = f'include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&user_id={rest_id}')

				if not r.ok:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при массовом анфолловинге: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при массовом анфолловинге: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно отписался от {current_username_to_subscribe}')

				return

	def get_random_username(self):
		while True:
			try:
				r = get('https://randomuser.me/api/')

				if not r.ok:
					raise Wrong_Response(r)

				random_username = loads(r.text)['results'][0]['login']['username']

			except Exception as error:
				logger.error(f'{self.username} | Не удалось получить случайный @username, ошибка: {str(error)}, пробую еще раз')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Не удалось получить случайный @username, ошибка: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}, пробую еще раз')

			else:
				logger.success(f'{self.username} | Успешно получено случайный @username: {random_username}')

				return(random_username)

	def change_username(self):
		for _ in range(3):
			try:
				random_username = self.get_random_username()
				r = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers = {'content-type': 'application/x-www-form-urlencoded'}, data = f'include_mention_filter=true&include_nsfw_user_flag=true&include_nsfw_admin_flag=true&include_ranked_timeline=true&include_alt_text_compose=true&screen_name={random_username}')

				if not r.ok:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при смене @username: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при смене @username: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт сменил @username на {random_username}')

				return

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

	def change_avatar(self, avatar_data):
		for _ in range(3):
			try:
				r = self.session.post("https://twitter.com/i/api/1.1/account/update_profile_image.json", data = {"image": avatar_data}, headers = {'content-type': 'application/x-www-form-urlencoded'})

				if r.status_code != 200:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при смене аватарки: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при смене аватарки: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно сменил аватарку')

				return

	def change_banner(self, banner_data):
		for _ in range(3):
			try:
				r = self.session.post("https://twitter.com/i/api/1.1/account/update_profile_banner.json", data = {"banner": banner_data}, headers = {'content-type': 'application/x-www-form-urlencoded'})

				if r.status_code != 201:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при смене баннера: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при смене баннера: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно сменил баннер')

				return

	def change_profile(self, current_bio):
		for _ in range(3):
			try:
				r = self.session.get('https://twitter.com/i/api/graphql/Bhlf1dYJ3bYCKmLfeEQ31A/UserByScreenName?variables={"screen_name":"'+ self.username +'","withSafetyModeUserFields":true,"withSuperFollowsUserFields":true}')

				if not r.ok:
					raise Wrong_Response(r)

				old_desc = loads(r.text)['data']['user']['result']['legacy']['description']
				old_name = loads(r.text)['data']['user']['result']['legacy']['name']

				if not current_bio:
					r = self.session.post('https://twitter.com/i/api/1.1/account/update_profile.json', headers = {'content-type': 'application/x-www-form-urlencoded'}, data = f'displayNameMaxLength=50&name={get_full_name()}&description={old_desc}&location='.encode('utf-8'))

				else:
					r = self.session.post('https://twitter.com/i/api/1.1/account/update_profile.json', headers = {'content-type': 'application/x-www-form-urlencoded'}, data = f'displayNameMaxLength=50&name={old_name}&description={current_bio}&location='.encode('utf-8'))

				if r.status_code != 200:
					raise Wrong_Response(r)

			except Exception as error:
				logger.error(f'{self.username} | Ошибка при обновлении профиля: {str(error)}')

			except Wrong_Response as error:
				logger.error(f'{self.username} | Ошибка при обновлении профиля: {str(error)}, код ответа: {str(r.status_code)}, ответ: {str(r.text)}')

			else:
				logger.success(f'{self.username} | Аккаунт успешно сменил описание/имя')

				return
			

if __name__ == '__main__':
	clear()
	
	if user_action == 6:
		all_usernames = []

		for current_cookies_str in accounts_cookies:
			csrf_token = current_cookies_str.split('ct0=')[-1].split(';')[0]
			get_username_status, current_username = MainWork(current_cookies_str, csrf_token).get_username()
			if get_username_status: all_usernames.append(current_username)

	for current_cookies_str in accounts_cookies:
		if wallets_addresses or len(wallets_addresses) > 0:
			csrf_token = current_cookies_str.split('ct0=')[-1].split(';')[0]
			main_worker_obj = MainWork(current_cookies_str, csrf_token)
			get_username_status, current_username = main_worker_obj.get_username()

			if get_username_status:
				if user_action == 1:
					for username_to_subscribe in username_to_subscribe_list:
						main_worker_obj.mass_follow(username_to_subscribe)

				elif user_action == 2:
					for username_to_subscribe in username_to_subscribe_list:
						main_worker_obj.mass_unfollow(username_to_subscribe)

				elif user_action == 3:
					main_worker_obj.mass_retweets()

				elif user_action == 4:
					main_worker_obj.mass_likes()

				elif user_action == 5:
					if need_send_wallet == 'y':
						main_worker_obj.mass_comments(wallets_addresses.pop(0))

					else:
						main_worker_obj.mass_comments(None)

				elif user_action == 6:
					if len(all_usernames) > 1:
						for username_to_subscribe in all_usernames:
							main_worker_obj.mass_follow(username_to_subscribe)

				elif user_action == 7:
					if text_to_tweet_source == 2:
						if text_to_tweet_type == 1:
							current_text_to_tweet = text_to_tweet_list.pop(0)
						elif text_to_tweet_type == 2:
							current_text_to_tweet = text_to_tweet_list.pop(randint(0, len(text_to_tweet_list)-1))
						else:
							current_text_to_tweet = choice(text_to_tweet_list)

					main_worker_obj.mass_tweets(current_text_to_tweet)

				elif user_action == 8:
					main_worker_obj.change_username()

				elif user_action == 9:
					if avatars_source == 2:
						avatar_data = main_worker_obj.get_random_avatar_from_web()

					else:
						avatar_data = main_worker_obj.get_random_image_from_list(images_folder)

					main_worker_obj.change_avatar(avatar_data)

				elif user_action == 10:
					banner_data = main_worker_obj.get_random_image_from_list(images_folder)

					main_worker_obj.change_banner(banner_data)

				elif user_action == 11:
					random_bio_str = get_random_bio_from_file()
					main_worker_obj.change_profile(random_bio_str)

				elif user_action == 12:
					main_worker_obj.change_profile(None)

		else:
			break

		if user_sleep_option == 'y':
			sleep(user_time_to_sleep)


	logger.success('Работа успешно завершена')
	print('\nPress Any Key To Exit..')
	getch()
	exit()
