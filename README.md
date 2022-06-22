### 설치방법
```bash
pip install -r requirements.txt
```
### 실행방법
```bash
python main.py
```

### url 및 amount 세팅 방법
```python
cr = Crawler()
# 대상 url 지정
cr.set_target_contract_url(주소)
# amount 지정
cr.set_target_amount(값)
cr.run()
```