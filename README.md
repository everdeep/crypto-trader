## Autotrader Microservice 
This application is designed to scan the database for currency pairs that have been flagged for autotrading and then uses their respective trade strategies and parameters to conduct automated buying and selling.

### Project setup
If setting up on a fresh machine, there is some basic software that is required to be installed to ensure the application can run. This includes:

Required:
- **Homebrew** (for easy installing on mac)
- **Mysql**
- **Redis** (message broker)
- **Python 3.9+**

Optional:
- **iterm2**
- **Oh-my-zsh**
- **pyenv** (python virtual environment) - for convenient python version mangement


### Setup (Mac):
<details>
<summary><b>Info</b></summary>

1. Install homebrew  
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Install [Iterm2](https://iterm2.com/downloads.html)

3. Install Oh-my-zsh (Optional)
```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

4. Install other required software using brew
```bash
brew install mysql
brew install pyenv
brew install nvm
brew install redis
```
5. Ensure redis and mysql services are running on brew with
```
brew services
```
6. Start them if necessary
```
brew services start mysql;
brew services start redis;
```

7. Install python 3.9.6
```bash
pyenv install 3.9.6
```

8. Clone the repository
```bash
git clone https://github.com/everdeep/cryptobot.git

# Store credentials
git config credential.helper store
```

8. Install missing pip packages
```bash
pip install -r requirements.txt
pip install marshmallow_enum
pip install -U "celery[redis]"
```

9. Create the *.env* file

10. Setup celery Daemon service
```bash
# In crytobot/trader/celery
sudo cp default/celeryd /etc/default/celeryd
sudo cp default/celerybeat /etc/default/celerybeat

sudo cp init.d/celeryd /etc/init.d/celeryd
sudo cp init.d/celerybeat /etc/init.d/celerybeat
```

11. Check celery works
```bash
celery -A monitor worker -l INFO
```

</details>

### Setup (Ubuntu):
<details>
<summary><b>Info</b></summary>

1. Update packages
```bash
sudo apt update && sudo apt upgrade

# Install pip
sudo apt install python3-pip
```
2. Install mysql ([Debugging](https://bobcares.com/blog/oserror-mysql_config-not-found/))
```bash
sudo apt install mysql-server
sudo apt install libmysqlclient-dev
sudo apt install build-essential
```
3. [Setup mysql](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04)
OR connect to RDS mysql

4. Navigate to the sql folder and create the database:
```bash
mysql -u root -p < database.sql
# other scripts if necessary

or 

mysql -u admin -p -h [endpoint] < database.sql
```

5. Install Redis
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt-get update
sudo apt-get install redis

pip install -U "celery[redis]"

# Check it is running
service --status-all

# Start if not
service redis-server start
```
Further documentation [here](https://redis.io/docs/getting-started/installation/install-redis-on-linux/).

6. Clone repo
```bash
git clone https://github.com/everdeep/cryptobot.git

# Store credentials
git config credential.helper store
```

7. Update PATH to include pip packages (if necessary)
```bash
export PATH=$PATH:/home/ubuntu/.local/bin
```

8. Install missing pip packages
```bash
pip3 install -r requirements.txt
pip3 install marshmallow_enum
```

9. Create the *.env* file

10. Setup celery Daemon service
```bash
# In crytobot/trader/celery
sudo cp default/celeryd /etc/default/celeryd
sudo cp default/celerybeat /etc/default/celerybeat

sudo cp init.d/celeryd /etc/init.d/celeryd
sudo cp init.d/celerybeat /etc/init.d/celerybeat
```

11. Check celery works
```bash
celery -A monitor worker -l INFO
```
</details>

***

### Testing
1. Navigate to the `src` directory.

2. Run the celery beat scheduler with
```bash
celery -A monitor beat -l INFO
```

3. Run the celery worker
```bash
celery -A monitor worker -l INFO
```

4. Observe if tasks are being scheduled and executed.

***

### Monitoring
Logs can be found in `/var/log/celery/` and `/var/log/celerybeat/` for the worker and scheduler respectively. Depending on the number of workers, the logs will be split into different files.

### Debugging
1. If you are having issues with connecting to mysql, you need to first alter the root user
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'your_new_password';
```