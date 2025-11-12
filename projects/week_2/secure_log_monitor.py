import json
import logging
import os
import random
import time

# ===== [신규] system.log 자동 생성 =====
if not os.path.exists("system.log"):
    with open("system.log", "w", encoding="utf-8") as f:
        f.write("INFO Server started\n")
        f.write("ERROR Connection timeout\n")
        f.write("ERROR Database connection lost\n")
        f.write("INFO System recovered\n")
        f.write("ERROR Unauthorized access attempt\n")
    print("[INFO] system.log 파일이 새로 생성되었습니다.")

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
    # 사용자 풀 구성
    users = [
        User("admin", authenticated=True),
        User("carol", authenticated=False),
        User("guest", authenticated=random.choice([True, False])),
        User("root", authenticated=True),
        User("analyst", authenticated=random.choice([True, False])),
        User("intern", authenticated=False),
    ]

    # system.log 업데이트 (다양한 에러 메시지 포함)
    error_templates = [
        "ERROR Connection timeout",
        "ERROR Unauthorized access attempt",
        "ERROR Disk quota exceeded",
        "ERROR Invalid token",
        "ERROR Database connection lost",
        "ERROR Firewall rule conflict",
        "ERROR Suspicious packet detected",
        "ERROR Privilege escalation attempt",
        "ERROR Memory leak in module",
        "ERROR Service unavailable",
    ]
    with open("system.log", "w", encoding="utf-8") as f:
        f.write("INFO Secure Log Simulation Started\n")
        for _ in range(30):
            f.write(random.choice(error_templates) + "\n")
        f.write("INFO Simulation Completed\n")
    print("[INFO] system.log 에 다양한 에러 패턴이 생성되었습니다.\n")

    # ===== 랜덤 로그 100개 생성 =====
    for i in range(100):
        u = random.choice(users)
        read_secure_log(u)
        time.sleep(0.03)  # 속도 조절 (0.03초 간격 → 약 3초 내 100개 생성)

    print("\n✅ 100개의 랜덤 접근 로그가 access.log에 기록 완료되었습니다.")
