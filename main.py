# -*- coding: utf-8 -*-
import time
from telegram.ext import Updater, MessageHandler, Filters
import datetime
import telegram
import chromedriver_autoinstaller
from selenium import webdriver
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self):
        self.bot = TelegramBot()
        self.__url = '0xc6a2ad8cc6e4a7e08fc37cc5954be07d499e7654'
        self.target_infos = []
        chromedriver_autoinstaller.install()
        self.options = webdriver.ChromeOptions()
        # self.options.add_argument('headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=self.options)

    def set_target_contract_url(self,_token_name, _term , _contract_url, _amount):
        info = {'token_name':_token_name,'url':_contract_url, 'amount':_amount, 'term':_term}
        self.target_infos.append(info)


    def run(self):
        self.bot.send('Klaytn finder 감시프로그램을 시작합니다.')
        lastet_block_num = '93995973'

        while True:
            try:
                error_count = 0
                block_num_list = []
                self.driver.get(f'https://www.klaytnfinder.io/account/{self.__url}?tabId=tokenTransfer')
                time.sleep(1)
                soup = BeautifulSoup(self.driver.page_source, 'html5lib')
                rows = soup.select('div.sc-bczRLJ.sc-gsnTZi.sc-jTYCaT.jJsXzF.fkYrgn.kbuOWw')
                for row in rows:
                    cols = row.select('div.sc-bczRLJ.sc-gsnTZi.sc-GVOUr.geVLEb.eQndoC.cruIwm')
                    block_info = {}
                    block_num = row.select('div')[3].text.replace('#','')
                    amount = row.select('div')[-1].text
                    block_info['from'] = 'Klayswap' if cols[0].text == 'Klayswap' else cols[0].contents[1].contents[0].attrs['href'].split('/')[-1]
                    block_info['to'] = 'Klayswap' if cols[1].text == 'Klayswap' else cols[1].contents[1].contents[0].attrs['href'].split('/')[-1]
                    block_info['block_num'] = float(block_num)
                    block_info['amount'] = float(amount.replace(',',''))
                    # print(block_info)
                    block_num_list.append(block_info)

                for block_info in block_num_list:
                    # 현재 블록이 마지막 블록보다 큰지 즉, 최신항목인지
                    if block_info['block_num'] >= float(lastet_block_num):
                        # 비교할 항목들
                        for target_info in self.target_infos:
                            # 현재 블록 의 양이 목표치 양보다 큰지, 그리고 우리가 원하는 url 인지
                            # if block_info['amount'] > target_info['amount'] and target_info['url'] in block_info['from']:
                            if block_info['amount'] > target_info['amount'] :
                                cur_time = datetime.datetime.now()
                                ampm = cur_time.strftime('%p')
                                ampm_kr = '오전' if ampm == 'AM' else '오후'
                                self.bot.send(f'''
{block_info['amount']} {target_info['token_name']} {target_info['term']} {'입금'if block_info['from'] == 'Klayswap' else '출금'} 되었습니다.
<b>{ampm_kr} {cur_time.strftime("%I:%M:%S")}</b>
    ''', html_mode=True)
                lastet_block_num = str(int(block_num_list[0]['block_num']) + 1)
            except Exception as e:
                lastet_block_num = '93995973'
                error_count += 1
                print(e)
                self.bot.send(f'Klaytn finder 데이터 요청에 문제가 {error_count}번 발생했습니다.')
                if error_count == 3:
                    error_count = 0
                    self.bot.send(f'Klaytn finder 데이터 요청에 문제가 있어서 5초 대기합니다.')
                    time.sleep(5)

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

cr = Crawler()
# 대상 url 지정
cr.set_target_contract_url(_token_name ='SIX',_term='가', _contract_url='0xbfb4528b7096d983f1c3c693274c4c14887aee41',_amount=100)

cr.run()