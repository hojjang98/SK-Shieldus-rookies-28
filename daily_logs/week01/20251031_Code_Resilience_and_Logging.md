## 📄 2025.10.31 (Day 5) [예외 처리, 로깅, 파일 입출력]

## 1. 🧠 핵심 개념 정리 (Concepts)

* [cite_start]핵심1 — **예외 처리 (`try-except-else-finally`)**: 시스템의 비정상적인 종료를 방지하고, 코드를 **견고하게 구축**하여 예상치 못한 상황(예: 잘못된 입력값, 리소스 접근 실패)에 대처한다[cite: 1].
* [cite_start]핵심2 — **로깅 (Logging)**: **`try-except` 구문과 결합**하여 예외 발생 시 **상황 정보를 기록**(`warning`, `error` 레벨 사용)하여 디버깅 및 보안 관제(접근 실패, 탐지 상황 기록)에 활용한다.
* 핵심3 — **데코레이터 (Decorator)**: 함수 로직 변경 없이 **권한 체크, 로깅, 실행시간 측정** 등 **공통 보안 로직**을 간결하게 추가하여 보안 통제 일관성을 확보하는 고급 기법이다.
* [cite_start]핵심4 — **파일 입출력 (`with open() as file`)**: 데이터 분석을 위한 **로그/데이터 파일(csv, json, txt)**을 처리하며, `with` 구문을 통해 **파일을 자동으로 `close()`**하여 리소스 누수(leak)와 예외를 방지한다.

---

## 2. 💻 실습 코드 & 응용 (Practice & Code)

```python
# 예시: 로깅을 이용한 오류 처리 및 마스킹 (보안적 측면 강화)
import logging
import json

# 사용자 이름을 두 글자만 남기고 마스킹
def mask_username(username):
    if not isinstance(username, str) or len(username) < 2: return "Unknown"
    masked_part = '*' * (len(username) - 2)
    return username[:2] + masked_part

def access_logger(func): # 데코레이터 정의
    def wrapper(user):
        username = user.get('name', 'N/A')
        masked_name = mask_username(username)
        try:
            result = func(user)
            # 성공 로그를 파일로 기록 (json.dump)
            log_data = {"level": "INFO", "masked_user": masked_name, "status": "SUCCESS", "message": "프로파일 접근 성공"}
            with open('userAccess.log', 'a', encoding='utf-8') as f:
                 json.dump(log_data, f, ensure_ascii=False); f.write('\n')
            return result
        except Exception as e:
            # 실패 시 경고 레벨로 오류 기록
            logging.warning(f"접근 오류 발생: 사용자 '{masked_name}' - {type(e).__name__}")
            # 실패 로그를 파일로 기록 (json.dump)
            log_data = {"level": "ERROR", "masked_user": masked_name, "status": "FAIL", "error_type": type(e).__name__,"message": "인증 실패 및 접근 거부"}
            with open('userAccess.log', 'a', encoding='utf-8') as f:
                json.dump(log_data, f, ensure_ascii=False); f.write('\n')
            raise # 예외를 재발생시켜 호출자에게 알림
    return wrapper

@access_logger # 데코레이터 적용
def getProfile(user):
    is_authenticated = False
    for key, value in user.items():
        if key == 'authenticated' and value is True:
            is_authenticated = True
            break
    if not is_authenticated:
        raise PermissionError("인증되지 않은 사용자 접근 시도")
    return {"name": user.get('name'), "status" : '프로파일_접근'}
```

- 사용 맥락: 관리자가 사용자 정보를 확인할 때, **접근 기록(시간, 사용자, 상태)**을 파일에 남기며, **민감 정보(사용자 이름)**는 마스킹 처리하여 보안성을 강화하는 로깅 로직 구현에 사용한다.
- 확장 아이디어: 실행시간 측정 데코레이터 (`timer`)를 활용하여 **성능 저하**를 모니터링하고, 특정 시간 초과 시 **경고 로그**를 발생시키는 로직을 추가할 수 있다.

---

## 3. 🛡️ 보안 관점 분석 (Security Insight)

* 관점1 — **공통 보안 로직의 적용 (데코레이터)**:
    * **적용방식**: 인증/인가가 필요한 API 함수나 민감 정보 처리 함수에 **데코레이터**를 적용하여 **권한 체크** 또는 **데이터 마스킹 로깅**과 같은 **공통 보안 기능**을 일괄적으로 적용하여 보안 통제 일관성을 확보한다.

* 관점2 — **시스템 비정상 종료 방지 및 정보 은폐 (예외 처리)**:
    * **적용방식**: `try-except` 구문을 통해 예외 발생 시 시스템이 비정상 종료되는 것을 막고 정상적인 흐름으로 종료시키며, **`except` 블록에서 구체적인 예외 정보**를 외부에 노출하지 않고 **내부 로깅**만 수행하여 공격자에게 시스템 정보를 유출하는 것을 방지한다.

* 관점3 — **보안 감사 및 침해 탐지 (로깅 및 파일 입출력)**:
    * **적용방식**: 중요한 이벤트(로그인 성공/실패, 민감 데이터 접근 등) 발생 시 **로깅 레벨(WARNING, ERROR)**을 사용하여 **시간 정보와 함께 기록**하고, 이를 **별도의 로그 파일**로 저장하여 **보안 감사(Audit)** 증거로 활용하거나, 침해 사고 발생 시 **탐지 및 분석**을 위한 기초 데이터로 활용한다.

---

## 4. 🧩 요약 (Summary)

1.  예외처리는 **코드의 견고성**을 위한 필수 요소로, `try-except-finally`를 통해 **시스템의 비정상 종료를 막고** 예상치 못한 상황에 대처한다.
2.  **로깅**은 예외 상황에서 **마스킹된 사용자 정보** 등 **필요한 정보만 기록**하여 보안 감사 증거로 활용하고 **정보 유출 위험**을 줄인다.
3.  **데코레이터**를 활용하여 **권한 체크 및 로깅** 등 **공통 보안 로직**을 함수 전후에 간결하게 적용하는 것이 **보안 통제 일관성** 확보에 효과적이다.