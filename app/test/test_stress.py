''' Contributed by Lin Junhong et al. 2023-06.'''

import requests
import multiprocessing
import time

def stress(username):
    try:
        data = {
            'username': username,
            'password': '123123'
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36 Edg/114.0.1823.51'
        }
        session = requests.session()
        response = session.post(url='http://127.0.0.1:5000/signup', data=data, headers=headers)
        print('Sign up ', response.status_code)
        time.sleep(0.5)
        response = session.post(url='http://127.0.0.1:5000/login', data=data, headers=headers)
        print('Sign in ', response.status_code)
        time.sleep(0.5)
        response = session.get(url=f'http://127.0.0.1:5000/{username}/userpage', headers=headers)
        print('User page', response.status_code)
        time.sleep(0.5)
        print(session.cookies)
        for i in range(5):
            response = session.get(url=f'http://127.0.0.1:5000/get_next_article/{username}', headers=headers, cookies=session.cookies)
            time.sleep(0.5)
            print(f'Next page ({i}) [{username}]')
            print(response.status_code)
            print(response.json()['today_article']['article_title'])
    except Exception as e:
        print(e)


if __name__ == '__main__':
    username = 'Learner'
    pool = multiprocessing.Pool(processes=10)
    for i in range(10):
        pool.apply_async(stress, (f'{username}{i}',))
    pool.close()
    pool.join()
