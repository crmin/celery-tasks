import random
import time

from django.http import HttpResponse
from kombu.exceptions import OperationalError
from loguru import logger

from works.tasks import calculate_task


# Note: f() definition은 works.tasks로 이동했습니다

def process_work(request):
    tick = time.time()
    n = random.randrange(35, 42)

    try:
        calculate_task.delay(n, tick)
    except OperationalError:  # task 실행 시점에 이미 broker와 연결이 끊겨있음
        # -> 유저가 실행을 요청할 때 이미 문제가 파악되므로 DB에 등록하지 않고 response로 실패를 보여줄 수 있음
        logger.error('Cannot connect to broker')
        return HttpResponse('Cannot connect to broker')

    return HttpResponse('done')
