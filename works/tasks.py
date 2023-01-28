import time
from typing import Callable

from celery import shared_task

from works.models import Work


@shared_task
def calculate_task(function: Callable, n: int, tick: int):
    """n값을 대상으로 function(n)을 연산하고 결과를 DB에 저장함

    Arguments:
    - function (Callable): n값을 이용해서 값을 연산할 함수. 결과를 저장하는 Work model이 int만 받기 때문에 int를 받아서 int를 반환해야 함
    - n (int): function(n)에 전달할 parameter
    - tick (int): 실행 시간을 저장하기 위한 시작 기준 시간. unix timestamp (unit=second). time.time()으로 생성된 값을 사용하면 됨

    Note:
    피보나치 연산을 위한 함수 f 외에도 다른 연산에 대응하기 위해서 내부에서 f()를 호출하지 않고 외부의 function을 받아서 실행하도록 함.
    """
    Work(
        n=n,
        result=function(n),
        elapsed_time=str(time.time() - tick),
    ).save()
