# Celery Tasks

## 목표
동기적으로 동작하는 view의 루틴을 비동기적으로 동작하도록 수정

## 실행
프로젝트는 dockerize 되었고, brocker, database 등과 함께 동작하므로 docker compose를 이용해서 실행함

```shell
docker compose up --build
```
* django project는 http://localhost:8888 를 통해 접근 가능.
  * django admin을 통해서도 데이터를 확인 가능.
    * http://localhost:8888/admin
    * username=admin
    * password=admin
* database는 host=localhost, port=5432, database=beringlab으로 접근 가능. 계정 정보는 .env 파일에서 확인 가능. 


### 실행에 문제가 발생한 경우
#### `docker: 'compose' is not a docker command`
이전 버전의 docker compose를 사용해서 발생한 문제. 아래 명령어로 실행
```shell
docker-compose up --build
```

#### ~~`SCRAM authentication requires libpq version 10 or above`~~

> `psycopg2-binary` 대신 `psycopg2` 패키지를 사용해서 해결되었음.

M1과 같은 Apple silicon을 포함한 ARM processor에서는 잘못된 버전의 libpq에 대해 빌드하는 버그로 인해서
psycopg2-binary package가 실행되지 않으므로 아래 환경변수를 설정하고 rosetta를 통해 실행해야함
```shell
export DOCKER_DEFAULT_PLATFORM=linux/amd64
```


## 환경
- postgresql 15
  - celery worker와 django api간의 DB 공유를 volume으로 하는 것 보다 DBMS에서 처리하는 것이 더 좋은 구조라고 생각했음.
  - celery worker와 api에서 동시에 db 요청이 오는 경우 psql같은 DBMS는 요청을 적절히 처리해줄 것이라는 기대가 있음.
- celery 13.7
  - redis가 in-memory에서 동작하기 때문에 성능은 더 좋겠지만 어떠한 이유로 container가 내려가게 된다면 정보 손실이 발생함.
  - 해당 프로젝트 특성상 많은 트래픽이 발생하지 않는 반면, HA가 고려되지 않았기 때문에 정보 손실이 발생하지 않는것이 더 중요하다고 판단됨.
  - 정보가 손실되어도 유저가 재시도를 하면 되는 등 큰 무리가 없는 작업이라면 redis를 고려해볼 수 있을 것 같음.

## 설계 의도
- `.env`가 `.gitignore`에 처리되지 않고 github에 올라가는 이유
  - 환경변수값에 psql 정보가 담겨있는데, 해당 프로젝트가 제품을 위한 프로젝트가 아니고 테스트를 위함이므로 보안적인 문제는 없다고 생각됨.
  - .env 파일로 환경 변수를 관리함으로 여러 container에서 같은 값을 쉽게 참조할 수 있고, 추후 값의 변경도 쉬움.
- `Work.note` 필드가 `null=True`가 아닌 `blank=True`인 이유
  - null value는 aggregate할 때 예상하지 못한 결과를 가져오기도 함.
  - int와 같은 type에서는 "blank"를 의미하는 값은 null 밖에 없음. (0 != null).
    하지만 str에서는 ""와 null 모두 "blank"를 의미할 수 있으므로 개발자에게 혼돈을 줄 수 있음.
  - 따라서 str이 저장되는 필드 (CharField, TextField)는 null=False, blank=True로 설정해야함
