package com.project.rookies.controller;

import com.project.rookies.dto.DnaResultDto;
import com.project.rookies.dto.FamilyRelationDto;
import com.project.rookies.dto.UserDto;
import com.project.rookies.mapper.DnaMapper;
import com.project.rookies.mapper.FamilyRelationMapper;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.io.File;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Controller
@RequestMapping("/employee")
@RequiredArgsConstructor
public class EmployeeController {

    private final FamilyRelationMapper familyRelationMapper;
    private final DnaMapper dnaMapper;

    @GetMapping("/search")
    public String searchForm(Long targetUserId, Model model) {
        model.addAttribute("targetUserId", targetUserId);
        return "employee/search";
    }

    @PostMapping("/search")
    public String search(Long targetUserId, String name, HttpSession session, Model model) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";

        Long resolvedUserId = targetUserId != null ? targetUserId : user.getId();

        List<FamilyRelationDto> matches = new ArrayList<>();
        if (name != null && !name.trim().isEmpty()) {
            matches = familyRelationMapper.searchByUserIdAndName(resolvedUserId, name.trim());
        }

        model.addAttribute("keyword", name);
        model.addAttribute("targetUserId", targetUserId);
        model.addAttribute("resolvedUserId", resolvedUserId);
        model.addAttribute("matches", matches);
        return "employee/search";
    }

    @GetMapping("/results")
    public String results(String writer, Model model) {
        List<DnaResultDto> reports = new ArrayList<>();
        if (writer != null && !writer.trim().isEmpty()) {
            reports = dnaMapper.findResultsForUser(writer.trim());
        }
        model.addAttribute("writer", writer);
        model.addAttribute("reports", reports);
        return "employee/results";
    }

    @GetMapping("/report/download")
    public ResponseEntity<Resource> download(Long id) throws Exception {
        DnaResultDto r = dnaMapper.findResultById(id);
        if (r == null) return ResponseEntity.notFound().build();

        File f = new File(r.getFilepath());
        if (!f.exists()) return ResponseEntity.notFound().build();

        String encoded = URLEncoder.encode(r.getFilename(), StandardCharsets.UTF_8).replaceAll("\\+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_PDF)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename*=UTF-8''" + encoded)
                .body(new FileSystemResource(f));
    }
}
