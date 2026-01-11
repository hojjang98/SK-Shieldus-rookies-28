import json
import logging
import os

# 로그 설정
logging.basicConfig(
    filename="access.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

# system.log 초기 생성 (없을 경우만)
if not os.path.exists("system.log"):
    with open("system.log", "w", encoding="utf-8") as f:
        f.write("2025-11-12 09:00 [INFO] System boot completed\n")
        f.write("2025-11-12 09:15 [ERROR] Connection timeout\n")
        f.write("2025-11-12 09:27 [ERROR] Unauthorized access attempt\n")
        f.write("2025-11-12 09:41 [INFO] Service recovered\n")
    print("[INFO] system.log created")

class User:
    def __init__(self, name: str, authenticated: bool = False):
        self.name = name
        self.authenticated = authenticated

# 접근 로깅 데코레이터
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

@access_logger
def read_secure_log(user: User):
    if not user.authenticated:
        raise PermissionError("인증되지 않은 사용자입니다.")
    with open("system.log", "r", encoding="utf-8") as f:
        logs = f.readlines()
    filtered = [line.strip() for line in logs if "ERROR" in line]
    return filtered[-5:]

if __name__ == "__main__":
    print("=== Mini Security Log Monitor ===\n")

    users = [
        User("admin", authenticated=True),
        User("carol", authenticated=False)
    ]

    for u in users:
        result = read_secure_log(u)
        if result:
            print(f"{u.name} → 최근 오류 로그 {len(result)}건 탐지됨.")
            for line in result:
                print("   ", line)
        print("-" * 50)
