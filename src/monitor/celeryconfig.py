broker_url = "redis://localhost:6379/0"
result_backend = "rpc://"

# task_default_queue = 'celery'
task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]
timezone = "Europe/Berlin"
enable_utc = True

# List of modules to import when the Celery worker starts.
imports = ("monitor.tasks",)

# List of functions to call when the Celery worker starts.
task_time_limit = 55
task_soft_time_limit = 45
worker_max_tasks_per_child = 10
# worker_concurrency = 1
worker_prefetch_multiplier = 1


# Add schedule tasks
beat_schedule = {
    "autotrade": {"task": "monitor.tasks.do_scheduled_autotrade", "schedule": 60.0, "args": ()},
    "update_balance": {"task": "monitor.tasks.do_scheduled_update_balance", "schedule": 60.0, "args": ()},
}

# Custom annotation class
class Annotation:
    def annotate(self, task):
        pass


task_annotations = (Annotation(), {})


# Custom task failure handler
def on_failure(self, exc, task_id, args, kwargs, einfo):
    print("Task failed: {0!r}".format(exc))


task_failure = on_failure

# call afer celery shutdown signal
def on_worker_shutdown():
    print("Worker shutdown")


worker_shutdown = on_worker_shutdown