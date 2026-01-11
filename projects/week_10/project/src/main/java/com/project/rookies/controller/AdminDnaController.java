package com.project.rookies.controller;

import com.project.rookies.config.AppConfig;
import com.project.rookies.dto.BoardDto;
import com.project.rookies.dto.DnaResultDto;
import com.project.rookies.dto.DnaStatusDto;
import com.project.rookies.dto.UserDto;
import com.project.rookies.mapper.BoardMapper;
import com.project.rookies.mapper.DnaMapper;
import com.project.rookies.mapper.UserMapper;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.nio.file.Files;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/admin/dna")
@RequiredArgsConstructor
public class AdminDnaController {

    private final BoardMapper boardMapper;
    private final DnaMapper dnaMapper;
    private final UserMapper userMapper;
    private final AppConfig appConfig;

    @GetMapping("/applications")
    public String applications(HttpSession session, Model model) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";
        if (!"admin".equalsIgnoreCase(user.getRole())) return "redirect:/board/list";

        List<BoardDto> applications = boardMapper.findAll("");
        Map<Long, DnaStatusDto> statusMap = new HashMap<>();
        for (BoardDto b : applications) {
            dnaMapper.ensureStatus(b.getId());
            statusMap.put(b.getId(), dnaMapper.findStatus(b.getId()));
        }

        model.addAttribute("applications", applications);
        model.addAttribute("statusMap", statusMap);
        model.addAttribute("users", userMapper.findAllUsers());
        return "admin/dna_applications";
    }

    @PostMapping("/status")
    public String updateStatus(Long boardId, String status, HttpSession session) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";
        if (!"admin".equalsIgnoreCase(user.getRole())) return "redirect:/board/list";

        dnaMapper.ensureStatus(boardId);
        dnaMapper.updateStatus(boardId, status);
        return "redirect:/admin/dna/applications?statusUpdated=1";
    }

    @PostMapping("/result/upload")
    public String uploadResult(Long boardId, String category, MultipartFile file, HttpSession session) throws Exception {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";
        if (!"admin".equalsIgnoreCase(user.getRole())) return "redirect:/board/list";

        if (file == null || file.isEmpty()) return "redirect:/admin/dna/applications?uploadError=empty";

        String original = file.getOriginalFilename() == null ? "report.pdf" : file.getOriginalFilename();
        String safeName = original.replaceAll("[\\\\/]+", "_");
        if (!safeName.toLowerCase().endsWith(".pdf")) return "redirect:/admin/dna/applications?uploadError=type";

        String baseDir = appConfig.getUploadPath();
        File dir = new File(baseDir + "reports/" + boardId + "/");
        if (!dir.exists()) dir.mkdirs();

        File out = new File(dir, System.currentTimeMillis() + "_" + safeName);
        Files.write(out.toPath(), file.getBytes());

        DnaResultDto dto = new DnaResultDto();
        dto.setBoardId(boardId);
        dto.setCategory(category);
        dto.setFilename(safeName);
        dto.setFilepath(out.getAbsolutePath());
        dnaMapper.saveResult(dto);

        dnaMapper.ensureStatus(boardId);
        dnaMapper.updateStatus(boardId, "결과 업로드");

        return "redirect:/admin/dna/applications?uploaded=1";
    }
}
