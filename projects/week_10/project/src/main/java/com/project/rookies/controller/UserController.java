package com.project.rookies.controller;

import com.project.rookies.dto.FamilyRelationDto;
import com.project.rookies.dto.UserDto;
import com.project.rookies.dto.UserProfileDto;
import com.project.rookies.mapper.FamilyRelationMapper;
import com.project.rookies.mapper.UserProfileMapper;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;

@Controller
@RequestMapping("/user")
@RequiredArgsConstructor
public class UserController {

    private final UserProfileMapper userProfileMapper;
    private final FamilyRelationMapper familyRelationMapper;

    @GetMapping("/mypage")
    public String mypage(HttpSession session, Model model) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";

        UserProfileDto profile = userProfileMapper.findByUserId(user.getId());
        List<FamilyRelationDto> family = familyRelationMapper.findByUserId(user.getId());

        model.addAttribute("user", user);
        model.addAttribute("profile", profile);
        model.addAttribute("family", family);

        return "user/mypage";
    }

    @PostMapping("/profile")
    public String updateProfile(UserProfileDto profileDto, HttpSession session) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";

        profileDto.setUserId(user.getId());
        userProfileMapper.upsert(profileDto);
        return "redirect:/user/mypage?profileUpdated=1";
    }

    @PostMapping("/family/add")
    public String addFamily(FamilyRelationDto familyDto, HttpSession session) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";

        familyDto.setUserId(user.getId());
        familyRelationMapper.add(familyDto);
        return "redirect:/user/mypage?familyAdded=1";
    }

    @PostMapping("/family/delete")
    public String deleteFamily(Long id, HttpSession session) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";

        familyRelationMapper.delete(id, user.getId());
        return "redirect:/user/mypage?familyDeleted=1";
    }
}
