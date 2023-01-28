import time

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

    만약 f(n) 연산에 실패한다고 해도 DB에 저장해서 유저가 처리 종료를 확인할 수 있도록 함.
    다만, result=None, success=False, note=에러메시지로 설정됨.
    해당 부분의 설계 의도는 works.models.Work docstring을 참고
    """

    try:
        function_result = f(n)
        success = True
        note = ''
    except Exception as e:
        function_result = None
        success = False
        note = str(e)

    Work(
        n=n,
        result=function_result,
        elapsed_time=str(time.time() - tick),
        success=success,
        note=note,
    ).save()
