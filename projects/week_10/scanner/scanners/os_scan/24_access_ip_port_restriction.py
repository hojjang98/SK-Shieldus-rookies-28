import sys
import os
try:
    from .utils import get_session_with_admin_auth, detect_os, execute_command
except ImportError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from scanners.os_scan.utils import get_session_with_admin_auth, detect_os, execute_command

def _has_hosts_deny_all(content):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        normalized = line.replace(" ", "")
        if normalized.upper().startswith("ALL:ALL"):
            return True
    return False

def _has_hosts_allow(content):
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        return True
    return False

def _iptables_has_non_docker_rules(content):
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("Chain "):
            continue
        lower = line.lower()
        if lower.startswith("target"):
            continue
        if "docker" in lower:
            continue
        if lower.startswith("policy"):
            continue
        return True
    return False

def scan(target_url, login_info=None):
    result = {
        'name': 'OS: 접속 IP 및 포트 제한',
        'vulnerable': False,
        'details': [],
        'recommendations': []
    }

    try:
        session = get_session_with_admin_auth(target_url, login_info)
        os_type = detect_os(target_url, session)

        if os_type == "Windows":
            result['details'].append("[OS] Windows는 지원하지 않습니다")
            result['recommendation'] = 'Windows는 지원하지 않습니다'
            return result

        if os_type == "Linux":
            hosts_deny = execute_command(target_url, session, "cat /etc/hosts.deny 2>&1")
            hosts_allow = execute_command(target_url, session, "cat /etc/hosts.allow 2>&1")

            deny_all = _has_hosts_deny_all(hosts_deny)
            allow_configured = _has_hosts_allow(hosts_allow)

            ufw_status = execute_command(target_url, session, "ufw status 2>&1")
            firewalld_status = execute_command(target_url, session, "firewall-cmd --state 2>&1")
            iptables_status = execute_command(target_url, session, "iptables -L -n 2>&1")
            nft_status = execute_command(target_url, session, "nft list ruleset 2>&1")

            firewall_active = False
            if "active" in ufw_status.lower():
                firewall_active = True
            if "running" in firewalld_status.lower():
                firewall_active = True
            if "Chain" in iptables_status and "command not found" not in iptables_status:
                if _iptables_has_non_docker_rules(iptables_status):
                    firewall_active = True
            if "table" in nft_status.lower() and "command not found" not in nft_status.lower():
                firewall_active = True

            tools_missing = all(
                "command not found" in status.lower() or "not found" in status.lower()
                for status in [ufw_status, firewalld_status, iptables_status, nft_status]
            )

            if (deny_all and allow_configured) or firewall_active or tools_missing:
                result['details'].append("[OS] 접속 IP/포트 제한 설정: 양호")
            else:
                result['vulnerable'] = True
                result['details'].append("[OS] 접속 IP/포트 제한 설정 미흡")
                result['recommendations'].append("hosts.deny/allow 설정 또는 방화벽 활성화 필요")

        if not result['recommendations']:
            result['recommendation'] = '안전 - 접속 IP 및 포트 제한이 설정됨'
        else:
            result['recommendation'] = ' | '.join(list(set(result['recommendations'])))

    except Exception as e:
        result['details'].append(f"오류: {str(e)}")
        result['recommendation'] = '검사 실패'

    return result
