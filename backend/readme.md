### 1. Launch server 
step1: install python 3 ( 3.8 or 3.9)

step2: install requirements, enter the following command in your terminal：
```python
pip install -r requirements.txt

or

pip3 install -r requirements.txt
```

step3: create ***.env*** file under ***app*** folder


step4: enter the below command to run the server
```python
python3 app/main.py
```
<br/>

### 2. export requirements.txt
```python
pipreqs . --encoding=utf8 --force
```
<br/>

### 3. execute the pytest
```shell
cd ~/backend/app

pytest
```
<br>

Inorder to test the api, we have to use locust
```shell
pip install locust
```
Then we have to run the test_api_*.py via following
```shell

```
<br/>