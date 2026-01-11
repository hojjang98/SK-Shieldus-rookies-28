package com.project.rookies.controller;

import com.project.rookies.dto.UserDto;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@Controller
@RequestMapping("/admin")
public class AdminController {

    /**
     * [시나리오] 서버 상태 점검 페이지
     * - 관리자만 들어올 수 있어야 하는데, 쿠키값(role=admin)만 확인하는 취약한 구조
     * - 핑 테스트 기능에 Command Injection 존재
     */
    @GetMapping("/system")
    public String systemCheck(HttpServletRequest request, HttpServletResponse response, HttpSession session, Model model) {
        // [취약점] 불충분한 인가 & 쿠키 변조
        // 세션 검증 없이 오직 'role' 쿠키가 'admin'인지만 확인

        boolean isAdmin = false;
        boolean hasCookie = false;
        if (request.getCookies() != null) {
            for (Cookie c : request.getCookies()) {
                if ("role".equals(c.getName())) {
                    hasCookie = true;
                    if ("admin".equals(c.getValue())) {
                        isAdmin = true;
                    }
                    break;
                }
            }
        }

        if (!hasCookie) {
            String initialRole = "user";

            UserDto loginUser = (UserDto) session.getAttribute("loginUser");

            if (loginUser != null && "admin".equals(loginUser.getUsername())) {
                initialRole = "admin";
                isAdmin = true;
            }

            Cookie roleCookie = new Cookie("role", initialRole);
            roleCookie.setPath("/");
            roleCookie.setHttpOnly(false);
            roleCookie.setSecure(false);
            response.addCookie(roleCookie);
        }

        if (!isAdmin) {
            UserDto loginUser = (UserDto) session.getAttribute("loginUser");

            if (loginUser != null) {
                if ("admin".equals(loginUser.getUsername()) || "admin".equalsIgnoreCase(loginUser.getRole())) {
                    isAdmin = true;
                }
            }
        }

        if (!isAdmin) {
            model.addAttribute("msg", "접근 거부: 관리자 권한이 필요합니다.");
            return "admin/access_denied";
        }

        return "admin/system"; // 관리자 대시보드
    }

    @PostMapping("/system/ping")
    public String pingTest(@RequestParam("target") String target, Model model) {
        // [취약점] OS Command Injection
        StringBuilder output = new StringBuilder();
        try {
            String os = System.getProperty("os.name").toLowerCase();
            Process p;
            if (os.contains("win")) {
                p = Runtime.getRuntime().exec("cmd.exe /c ping -n 3 " + target);
            } else {
                // Linux/Mac: /bin/bash -c "ping -c 3 <target>"
                String[] outputHelper = new String[] { "/bin/bash", "-c", "ping -c 3 " + target };
                p = Runtime.getRuntime().exec(outputHelper);
            }

            String charset = os.contains("win") ? "EUC-KR" : "UTF-8";

            BufferedReader reader = new BufferedReader(new InputStreamReader(p.getInputStream(), charset));
            String line;
            while ((line = reader.readLine()) != null) output.append(line).append("\n");
        } catch (Exception e) {
            output.append("Error: ").append(e.getMessage());
        }

        model.addAttribute("result", output.toString());
        model.addAttribute("lastTarget", target);
        return "admin/system";
    }
}