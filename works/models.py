from django.db import models


class Work(models.Model):
    """Celery task의 결과값을 저장함

    Celery task 처리는 비동기적으로 이루어지므로 slack webhook, email 등의 외부 알림 방법을 설정해두지 않은 이상 처리에 실패한 경우
    외부에서는 처리에 실패했는지, 아직 처리중인지 알 수 있는 방법이 없음.
    따라서 처리에 실패한 경우도 DB에 결과를 업데이트 해야함.

    처리에 실패한 경우
    result -> None
    success -> False
    note -> 에러 내용
    으로 설정함.

    * result is None으로 성공/실패 여부를 확인할 수 있지 않을까?
    -> 실행하는 함수가 지금은 None을 반환할 수 없지만 추후 변경이 있다면 그 때도 None을 반환하지 않을지는 알 수 없음
    -> result는 실행 결과 값을 저장하는 field이지, 성공 여부를 저장하는 field가 아니므로 의미적으로 맞지 않음
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    n = models.IntegerField()
    result = models.IntegerField(null=True)  # 실패한 경우 null
    elapsed_time = models.CharField(max_length=50)
    success = models.BooleanField(default=True)
    note = models.TextField(blank=True, default='')  # null=True가 아닌 이유는 README 참고
