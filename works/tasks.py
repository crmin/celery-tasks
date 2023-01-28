import time
from typing import Callable

from celery import shared_task

from works.models import Work


def f(n: int) -> int:
    return 1 if n <= 1 else f(n - 1) + f(n - 2)


@shared_task
def calculate_task(n: int, tick: int):
    """n값을 대상으로 f(n)을 연산하고 결과를 DB에 저장함

    Arguments:
    - n (int): f(n)에 전달할 parameter
    - tick (int): 실행 시간을 저장하기 위한 시작 기준 시간. unix timestamp (unit=second). time.time()으로 생성된 값을 사용하면 됨
    """
    Work(
        n=n,
        result=f(n),
        elapsed_time=str(time.time() - tick),
    ).save()
