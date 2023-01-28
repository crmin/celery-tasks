import random
import time

from django.http import HttpResponse

from works.tasks import calculate_task


def process_work(request):
    tick = time.time()
    n = random.randrange(35, 42)

    calculate_task.delay(n, tick)

    return HttpResponse('done')
