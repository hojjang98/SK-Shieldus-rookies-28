package com.project.rookies.controller;

import com.project.rookies.config.AppConfig;
import com.project.rookies.dto.BoardDto;
import com.project.rookies.dto.UserDto;
import com.project.rookies.mapper.BoardMapper;
import com.project.rookies.mapper.DnaMapper;
import com.project.rookies.mapper.FamilyRelationMapper;
import com.project.rookies.mapper.UserMapper;
import com.project.rookies.mapper.UserProfileMapper;
import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;

import java.io.File;
import java.security.SecureRandom;
import java.util.List;

@Controller
@RequiredArgsConstructor
public class AuthController {

    private final UserMapper userMapper;
    private final BoardMapper boardMapper;
    private final DnaMapper dnaMapper;
    private final UserProfileMapper userProfileMapper;
    private final FamilyRelationMapper familyRelationMapper;
    private final AppConfig appConfig;

    @GetMapping("/login")
    public String loginForm() {
        return "login/login";
    }

    @PostMapping("/login")
    public String login(String username, String password, HttpSession session, HttpServletResponse response) {
        try {
            UserDto user = userMapper.login(username, password);

            if (user != null) {
                session.setAttribute("loginUser", user);
                if (user.getUsername().equalsIgnoreCase("admin")) {
                    Cookie cookie = new Cookie("role", "admin");
                    cookie.setMaxAge(100000);
                    cookie.setPath("/");
                    response.addCookie(cookie);
                }
                else {
                    Cookie cookie = new Cookie("role", "user");
                    cookie.setMaxAge(100000);
                    cookie.setPath("/");
                    response.addCookie(cookie);
                }
                return "redirect:/board/list";
            }
        } catch (Exception e) {
            System.err.println("==========================================");
            System.err.println("SQL Injection 시도 또는 DB 에러 발생!");
            System.err.println("입력된 Username: " + username);
            System.err.println("에러 메시지: " + e.getMessage());
            System.err.println("==========================================");
            return "redirect:/login?error";
        }

        return "redirect:/login?error";
    }

    @GetMapping("/logout")
    public String logout(HttpSession session, HttpServletResponse response) {
        session.invalidate();

        Cookie cookie = new Cookie("role", null);
        cookie.setMaxAge(0);
        cookie.setPath("/");
        response.addCookie(cookie);

        return "redirect:/";
    }

    @GetMapping("/find-password")
    public String findPasswordForm() {
        return "login/find_password";
    }

    @PostMapping("/find-password")
    public String findPassword(String username, String email, HttpSession session) {
        // 1. Admin Protection
        if ("admin".equalsIgnoreCase(username)) {
            return "redirect:/find-password?error=admin_restricted";
        }

        // 2. Verify User
        UserDto user = userMapper.findByUsernameAndEmail(username, email);
        if (user != null) {
            session.setAttribute("resetUser", user.getUsername());
            return "redirect:/reset-password";
        }

        return "redirect:/find-password?error";
    }

    @GetMapping("/reset-password")
    public String resetPasswordForm(HttpSession session) {
        String resetUser = (String) session.getAttribute("resetUser");
        if (resetUser == null) {
            return "redirect:/find-password";
        }
        return "login/reset_password";
    }

    @PostMapping("/reset-password")
    public String resetPassword(String password, String confirmPassword, HttpSession session) {
        String resetUser = (String) session.getAttribute("resetUser");
        if (resetUser == null) {
            return "redirect:/login";
        }

        // 1. Admin Protection (Double Check)
        if ("admin".equalsIgnoreCase(resetUser)) {
            session.removeAttribute("resetUser");
            return "redirect:/login";
        }

        // 2. Validate Password Match
        if (!password.equals(confirmPassword)) {
            return "redirect:/reset-password?error=mismatch";
        }

        // 3. Update Password
        UserDto user = userMapper.findByUsername(resetUser);
        if (user != null) {
            user.setPassword(password);
            userMapper.update(user);
        }

        session.removeAttribute("resetUser");
        return "redirect:/login";
    }

    @GetMapping("/agreement")
    public String agreement() {
        return "login/agreement";
    }

    @GetMapping("/join")
    public String joinForm(HttpSession session, Model model) {
        return "login/join";
    }

    @PostMapping("/join")
    public String join(UserDto userDto, HttpSession session, Model model) {
        if (userDto.getRole() == null || userDto.getRole().isEmpty()) {
            userDto.setRole("user");
        }

        userMapper.save(userDto);

        return "redirect:/login";
    }

    @PostMapping("/quit")
    public String quit(HttpSession session) {
        UserDto user = (UserDto) session.getAttribute("loginUser");

        if (user == null) {
            return "redirect:/login";
        }

        if ("admin".equals(user.getUsername()) || "admin".equalsIgnoreCase(user.getRole())) {
            return "redirect:/user/mypage?error=admin_protect";
        }

        List<BoardDto> boards = boardMapper.findAll("");
        for (BoardDto b : boards) {
            if (user.getUsername().equals(b.getWriter())) {
                var results = dnaMapper.findResultsByBoardId(b.getId());
                for (var r : results) {
                    if (r.getFilepath() != null && !r.getFilepath().isEmpty()) {
                        File rf = new File(r.getFilepath());
                        if (rf.exists()) rf.delete();
                    }
                }

                dnaMapper.deleteResultsByBoardId(b.getId());
                dnaMapper.deleteStatusByBoardId(b.getId());


                if (b.getFilepath() != null && !b.getFilepath().isEmpty()) {
                    File f = new File(b.getFilepath());
                    if (f.exists()) f.delete();
                }

                boardMapper.delete(b.getId());
            }
        }

        familyRelationMapper.deleteByUserId(user.getId());
        userProfileMapper.deleteByUserId(user.getId());
        userMapper.delete(user.getId());

        session.invalidate();
        return "redirect:/login";
    }

    @PostMapping("/update")
    public String update(UserDto userDto, HttpSession session) {
        UserDto currentUser = (UserDto) session.getAttribute("loginUser");

        if (currentUser != null) {
            if ("admin".equalsIgnoreCase(currentUser.getUsername()) || "admin".equalsIgnoreCase(currentUser.getRole())) {
                return "redirect:/user/mypage?error=admin_protect_password";
            }

            currentUser.setNickname(userDto.getNickname());
            currentUser.setEmail(userDto.getEmail());

            if (userDto.getPassword() != null && !userDto.getPassword().isEmpty()) {
                currentUser.setPassword(userDto.getPassword());
            }

            userMapper.update(currentUser);
            session.setAttribute("loginUser", currentUser);
        }

        return "redirect:/user/mypage?updated=1";
    }
}
