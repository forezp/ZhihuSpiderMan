import requests
import json
import time
new_url_tokens = set()
old_url_tokens = set()
saved_users_set = set()

URL_TEMPLATE = "https://www.zhihu.com/api/v4/members/{0}/followees";
QUERY_PARAMS = "?include=data%5B*%5D.url_token&offset=0&per_page=30&limit=30";


def download(url):
    if url is None:
        return None
    try:
        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
            'authorization': 'your authorization '
        })
        print (response.content)
        if (response.status_code == 200):
            return response.content
        return None
    except:
        return None


def parse(response):
    try:
        print (response)
        json_body = json.loads(response);
        json_data = json_body['data']
        for item in json_data:
            if (not old_url_tokens.__contains__(item['url_token'])):
                if(new_url_tokens.__len__()<2000):
                   new_url_tokens.add(item['url_token'])
            if (not saved_users_set.__contains__(item['url_token'])):
                jj=json.dumps(item)
                save(item['url_token'],jj )
                saved_users_set.add(item['url_token'])

        if (not json_body['paging']['is_end']):
            next_url = json_body['paging']['next']
            response2 = download(next_url)
            parse(response2)

    except:
        print ('parse fail')


def save(url_token, strs):
    f = file("\\Users\\forezp\\Downloads\\zhihu\\user_" + url_token + ".txt", "w+")
    f.writelines(strs)
    f.close()


def get_new_url():
    url_token = new_url_tokens.pop()
    old_url_tokens.add(url_token)
    url = URL_TEMPLATE.format(url_token) + QUERY_PARAMS.replace('url_token', url_token)
    print (url)
    return url


def main():
    new_url_tokens.add('zhen-shi-gu-shi-ji-hua')
    while (new_url_tokens.__len__() > 0):
        time.sleep(0.1)
        url = get_new_url()
        response = download(url)
        parse(response)


if __name__ == '__main__':
    main()
