Скрипт **python3** для скачивания Ваших репозиториев с **github** и **gitlab** серверов по токену доступа.  
Тестировал на **python 3.7.5**, под **Linux Mint 19.3**.   

Работает на python3 >= **3.7**.

### Как использовать:

```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
&& sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
&& echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
&& sudo apt update \
&& sudo apt install gh libomp-dev -y

pip3 install -r requirements.txt

```

Скачиваем все доступные репозитории:
```bash
./src/main.py -s github.com -t ghp_TOKEN
```

В папке запуска сгенерируется архив с Вашими проектами.
