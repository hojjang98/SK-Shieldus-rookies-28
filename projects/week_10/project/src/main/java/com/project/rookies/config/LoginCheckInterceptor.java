package com.project.rookies.config;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import org.springframework.web.servlet.HandlerInterceptor;

public class LoginCheckInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler) throws Exception {
        HttpSession session = request.getSession(false);

        // 세션에 'loginUser'가 없으면 로그인 페이지로 리다이렉트
        if (session == null || session.getAttribute("loginUser") == null) {
            response.sendRedirect("/login");
            return false;
        }
        return true;
    }
}
