# -*- coding: utf-8 -*-
import datetime
import requests
import time
import json
import random

from telegram.ext import Updater, MessageHandler, Filters
import telegram


class TelegramBot:
    def __init__(self, parent=None):
        self.parent = parent

        # 이곳은 텔레그램 토큰과 챗아이디를 설정하는 부분입니다.
        self.telegram_token = '2123437403:AAF7PZJMxZZsF9RluiEc5n8yOK_RsaAOG1w'
        self.chat_id = '1200909738'
        try:
            self.bot = telegram.Bot(token=self.telegram_token)
        except:
            raise NameError

        self.updater = Updater(self.telegram_token, use_context=True)
        self.updater.start_polling(timeout=5)

    def send(self, msg, html_mode=False):
        try:
            if html_mode:
                self.bot.sendMessage(chat_id=self.chat_id, text=msg, parse_mode=telegram.ParseMode.HTML)
            else:
                self.bot.sendMessage(chat_id=self.chat_id, text=msg)
        except:
            pass


class Application:
    def __init__(self):
        self.driver = None
        self.bot = TelegramBot()

        # 감시하고자 하는 contract 주소를 지정합니다.
        self.my_contract = '0xc6a2ad8cc6e4a7e08fc37cc5954be07d499e7654'

        '''
        여기가 감시하고자 하는 토큰을 등록하는 곳입니다.
        형태는 보시면 아시겠지만,

        (1): {'number': (2), 'term': (3), 'address': (4)}

        위와 같으며,
          (1) - 코인 이름을 뜻하며 문자열로 해야 하기 때문에 'SIX', 'PIB' 와 같이 하시면 됩니다.
          (2) - 감시하고자 하는 임계물량을 숫자로 적으시면 됩니다.
          (3) - 텔레그램으로 메세지를 전송할 때에, '5,000 SIX가 입금되었습니다' 처럼 코인명 다음에 조사 '이'나 '가'를 
                써줘야 하는데 코인마다 '이', '가'를 구분하기 위해서 지정하는 부분입니다.
          (4) - 코인의 고유 contract 주소를 적으시면 됩니다. 역시 문자열이기 때문에 꼭 따옴표로 둘러싸야 합니다.
        '''
        self.monitoring_tokens = {
            'SIX': {'number': 2000, 'term': '가', 'address': '0x64b4ee8a878d785c9c06a18966d51a33345e5610'},
            'CLBK': {'number': 50000, 'term': '가', 'address': '0x55a5dcc23a7a697052ab5d881530849ca0efad34'},
            'MNR': {'number': 150000, 'term': '이', 'address': '0xe641811d4a0c80d1260d4036df54d90559b9ab54'},
            'PIB': {'number': 500000, 'term': '가', 'address': '0x2ecdf3088488a8e91c332b9ee86bb87d4e9cce82'},
            'REDI': {'number': 300000, 'term': '가', 'address': '0x5e9bc710d817affa64e0fd93f3f7602e9f4dd396'},
            'TRCL': {'number': 100000, 'term': '이', 'address': '0x8e4e386950f6c03b25d0f9aa8bd89c1b159e8aee'},
            'BORA': {'number': 5000, 'term': '가', 'address': '0xbbca9b2d17987ace3e98e376931c540270ce71bb'},
            'WEMIX': {'number': 1000, 'term': '가', 'address': '0x917eed7ae9e7d3b0d875dd393af93fff3fc301f8'},
            'HINT': {'number': 50000, 'term': '가', 'address': '0x194896a1fbd33a13d71e0a2053d4f8129f435e31'},
            'HIBS': {'number': 200000, 'term': '가', 'address': '0x6bf915f013dc12274adf57e3c68fe8464ddc8b10'},
            'WIKEN': {'number': 30000, 'term': '가', 'address': '0x6119b1540aa3bea20518f5e239f64d98ebe9aaff'},
            'SSX': {'number': 20000, 'term': '이', 'address': '0x01d71c376425b4feccb7b8719a760110091b3eb9'},
            'MBX': {'number': 100, 'term': '가', 'address': '0xbfb4528b7096d983f1c3c693274c4c14887aee41'},
            'ISR': {'number': 50000, 'term': '가', 'address': '0x869440673a24e3c3f18c173d8a964b2f2621245b'},
            'AGOV': {'number': 50000, 'term': '가', 'address': '0x5c6795e72c47d7fa2b0c7a6446d671aa2e381d1e'},

        }

        self.run()

    def run(self):
        self.bot.send('KlaySwapProtocol 감시프로그램을 시작합니다.')

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://scope.klaytn.com',
            'Referer': 'https:/scope.klaytn.com/',
            'X-Requested-With': 'XMLHttpRequest'
        }

        session = requests.Session()
        session.headers.update(headers)

        error_count = 1

        pre_result = []
        cur_result = []

        while True:
            rand = random.random()
            res = session.get(
                f'https://api-cypress-v2.scope.klaytn.com/v2/accounts/0xc6a2ad8cc6e4a7e08fc37cc5954be07d499e7654/ftTransfers?r={rand}',
                headers=headers)
            try:
                result = json.loads(res.text)
                pre_result = cur_result.copy()

                tokens = result['tokens']
                cur_result = result['result']

                new_data = [v for v in cur_result if v not in pre_result]
                if len(new_data) == 25:
                    time.sleep(1 + random.random())
                    rand = random.random()
                    res = session.get(
                        f'https://api-cypress-v2.scope.klaytn.com/v2/accounts/0xc6a2ad8cc6e4a7e08fc37cc5954be07d499e7654/ftTransfers?page=2&version=v3&r={rand}',
                        headers=headers)
                    more_result = json.loads(res.text)

                    tokens.update(more_result['tokens'])
                    cur_result = cur_result + more_result['result']

                    # new_data = [v for v in cur_result if v not in pre_result and (v['fromAddress'] == self.my_contract or v['toAddress'] == self.my_contract)]
                    new_data = [v for v in cur_result if v not in pre_result]

                text = ''
                for d in new_data:
                    token_symbol = tokens[d['tokenAddress']]['symbol'].upper()
                    amount = int(d['amount'], 16)
                    decimals = int(d['decimals'])
                    number = int(amount / pow(10, decimals))
                    if token_symbol in self.monitoring_tokens.keys() and number >= self.monitoring_tokens[token_symbol][
                        'number']:
                        if d['fromAddress'] == self.my_contract and d['toAddress'] == \
                                self.monitoring_tokens[token_symbol]['address']:
                            text = f'{number:,} {token_symbol}{self.monitoring_tokens[token_symbol]["term"]} 입금되었습니다.\n'
                        elif d['toAddress'] == self.my_contract and d['fromAddress'] == \
                                self.monitoring_tokens[token_symbol]['address']:
                            text = f'{number:,} {token_symbol}{self.monitoring_tokens[token_symbol]["term"]} 출금되었습니다.\n'

                if text:
                    cur_time = datetime.datetime.now()
                    ampm = cur_time.strftime('%p')
                    ampm_kr = '오전' if ampm == 'AM' else '오후'

                    text += f'<b>{ampm_kr} {cur_time.strftime("%I:%M:%S")}</b>\n'

                    print(text)
                    self.bot.send(text, html_mode=True)
                else:
                    # print('no new data..')
                    pass
            except Exception as e:
                error_count += 1
                print(e)
                self.bot.send(f'Klaytn 데이터 요청에 문제가 {error_count}번 발생했습니다.')
                if error_count == 3:
                    error_count = 0
                    self.bot.send(f'Klaytn 데이터 요청에 문제가 있어서 5초 대기합니다.')
                    time.sleep(5)

            time.sleep(1 + random.random() * 2)

        self.bot.updater.stop()


app = Application()
