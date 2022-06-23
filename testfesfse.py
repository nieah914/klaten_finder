headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.57 Whale/3.14.133.23 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': 'https://www.klaytnfinder.io',
    'Referer': 'https://www.klaytnfinder.io',
    'X-Requested-With': 'XMLHttpRequest'
}
import requests
session = requests.Session()
session.headers.update(headers)

error_count = 1

pre_result = []
cur_result = []



res = session.get('https://www.klaytnfinder.io/account/0xc6a2ad8cc6e4a7e08fc37cc5954be07d499e7654?tabId=tokenTransfer',headers=headers)
print(res.text)
res = session.get('https://cypress-api.klaytnfinder.io/api/v1/accounts/0xc6a2ad8cc6e4a7e08fc37cc5954be07d499e7654?_t=1655908468662',headers=headers)

print(res.text)
res = session.get(
    f'https://cypress-api.klaytnfinder.io/api/v1/accounts/0xc6a2ad8cc6e4a7e08fc37cc5954be07d499e7654/token-transfer-filters?_t=1655907973851',
    headers=headers)
print(res.text)
