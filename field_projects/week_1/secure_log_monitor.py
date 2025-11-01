import json
import logging


# ===== 로깅 설정 =====
logging.basicConfig(
    filename="access.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)


# ===== 사용자 클래스 =====
class User:
    def __init__(self, name: str, authenticated: bool = False):
        self.name = name
        self.authenticated = authenticated


# ===== 공통 로깅 데코레이터 =====
def access_logger(func):
    def wrapper(user: User):
        masked = user.name[:2] + "*" * (len(user.name) - 2)
        try:
            result = func(user)
            log_entry = {
                "user": masked,
                "result": "SUCCESS",
                "message": "로그 접근 성공"
            }
            with open("access.log", "a", encoding="utf-8") as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write("\n")
            logging.info(f"{masked} 접근 성공")
            print(f"[INFO] 접근 성공: {masked}")
            return result
        except Exception as e:
            log_entry = {
                "user": masked,
                "result": "FAIL",
                "error": type(e).__name__,
                "message": str(e)
            }
            with open("access.log", "a", encoding="utf-8") as f:
                json.dump(log_entry, f, ensure_ascii=False)
                f.write("\n")
            logging.warning(f"{masked} 접근 실패 ({type(e).__name__})")
            print(f"[WARNING] 접근 실패: {masked} ({type(e).__name__})")
    return wrapper


# ===== 보안 로그 접근 함수 =====
@access_logger
def read_secure_log(user: User):
    if not user.authenticated:
        raise PermissionError("인증되지 않은 사용자입니다.")
    with open("system.log", "r", encoding="utf-8") as f:
        logs = f.readlines()
    filtered = [line.strip() for line in logs if "ERROR" in line][-5:]
    return filtered


# ===== 실행부 =====
if __name__ == "__main__":
    users = [
        User("admin", authenticated=True),
        User("carol", authenticated=False)
    ]

    for u in users:
        read_secure_log(u)
