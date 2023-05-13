
1.  Run the beat scheduler to queue tasks
```bash
celery -A proj beat -l INFO
```

2. Run the worker to process the messages in the RabbitMQ queue
1.  Run the beat scheduler to queue tasks
```bash
celery -A proj worker -l INFO
```

***

For starting a celery instance in the background
```bash
celery multi start w1 -A proj -l INFO --pidfile=/var/run/celery/%n.pid \
                                      --logfile=/var/log/celery/%n%I.log
```

For stopping the instance
```bash
celery multi stop w1 -A proj -l INFO
```

For stopping the instance whilst waiting for tasks to finish
```bash
celery multi stopwait w1 -A proj -l INFO
```

Runninig celery as a daemon:
https://docs.celeryq.dev/en/3.1/tutorials/daemonizing.html
