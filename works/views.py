import random
import time

from django.http import HttpResponse

from works.tasks import calculate_task


def f(n: int) -> int:
    return 1 if n <= 1 else f(n - 1) + f(n - 2)


def process_work(request):
    tick = time.time()
    n = random.randrange(35, 42)

    calculate_task.delay(f, n, tick)

    return HttpResponse('done')
