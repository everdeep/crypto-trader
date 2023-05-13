from celery import Celery

app = Celery("monitor")

app.config_from_object("monitor.celeryconfig")

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == "__main__":
    app.start()
