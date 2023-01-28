# Beringlab 과제

## 목표
동기적으로 동작하는 view의 루틴을 비동기적으로 동작하도록 수정

## 환경
- postgresql 15
  - celery worker와 django api간의 DB 공유를 volume으로 하는 것 보다 DBMS에서 처리하는 것이 더 좋은 구조라고 생각했음.
  - celery worker와 api에서 동시에 db 요청이 오는 경우 psql같은 DBMS는 요청을 적절히 처리해줄 것이라는 기대가 있음.
- redis
  - in-memory에서 처리하기 때문에 rabbit mq를 broker로 사용하는 것 보다 더 빠르고 가벼울 것이라고 생각됨.
  - 어떠한 이유로 docker container가 내려갔을 때 정보 손실이 있을 수는 있지만
    view에서 하는 작업이 간단하고 속도가 중요한 작업이라고 생각해서 redis를 선택함.
  - 만약 view에서 처리하는 작업이 유실되지 않고 반드시 실행되어야하는 작업이라면 rabbitmq를 사용하면 될 것 같음.
## 설계 의도
- `.env`가 `.gitignore`에 처리되지 않고 github에 올라가는 이유
  - 환경변수값에 psql 정보가 담겨있는데, 해당 프로젝트가 제품을 위한 프로젝트가 아니고 테스트를 위함이므로 보안적인 문제는 없다고 생각됨.
  - .env 파일로 환경 변수를 관리함으로 여러 container에서 같은 값을 쉽게 참조할 수 있고, 추후 값의 변경도 쉬움.
- `Work.note` 필드가 `null=True`가 아닌 `blank=True`인 이유
  - null value는 aggregate할 때 예상하지 못한 결과를 가져오기도 함.
  - int와 같은 type에서는 "blank"를 의미하는 값은 null 밖에 없음. (0 != null).
    하지만 str에서는 ""와 null 모두 "blank"를 의미할 수 있으므로 개발자에게 혼돈을 줄 수 있음.
  - 따라서 str이 저장되는 필드 (CharField, TextField)는 null=False, blank=True로 설정해야함
