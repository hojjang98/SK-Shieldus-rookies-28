package com.project.rookies.controller;

import com.project.rookies.dto.BoardDto;
import com.project.rookies.dto.DnaResultDto;
import com.project.rookies.dto.DnaStatusDto;
import com.project.rookies.dto.UserDto;
import com.project.rookies.mapper.BoardMapper;
import com.project.rookies.mapper.DnaMapper;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/board")
@RequiredArgsConstructor
public class BoardController {

    private final BoardMapper boardMapper;
    private final DnaMapper dnaMapper;

    @Value("${file.upload-dir}")
    private String uploadDir;

    @GetMapping("/list")
    public String list(@RequestParam(defaultValue = "") String keyword, Model model, HttpSession session) {
        UserDto user = (UserDto) session.getAttribute("loginUser");

        if (user == null) {
            return "redirect:/login";
        }

        List<BoardDto> boards;
        if ("admin".equalsIgnoreCase(user.getUsername()) || "admin".equalsIgnoreCase(user.getRole())) {
            boards = boardMapper.findAll(keyword);
        } else {
            boards = boardMapper.findByWriterOrAdmin(user.getUsername(), keyword);
        }

        Map<Long, DnaStatusDto> statusMap = new HashMap<>();
        for (BoardDto b : boards) {
            dnaMapper.ensureStatus(b.getId());
            statusMap.put(b.getId(), dnaMapper.findStatus(b.getId()));
        }

        model.addAttribute("boardList", boards);
        model.addAttribute("statusMap", statusMap);
        return "board/list";
    }

    @GetMapping("/write")
    public String writeForm() {
        return "board/write";
    }

    @PostMapping("/write")
    public String write(BoardDto dto, @RequestParam MultipartFile file, HttpSession session) throws IOException {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        dto.setWriter(user.getUsername());

        if (!file.isEmpty()) {
            String originalFilename = file.getOriginalFilename();
            File dest = new File(uploadDir + originalFilename);
            file.transferTo(dest);

            dto.setFilename(originalFilename);
            dto.setFilepath(dest.getAbsolutePath());
        }

        boardMapper.save(dto);
        dnaMapper.ensureStatus(dto.getId());

        return "redirect:/board/list";
    }

    @GetMapping("/view")
    public String view(@RequestParam("id") Long id, Model model) {
        BoardDto board = boardMapper.findById(id);

        if (board != null) {
            dnaMapper.ensureStatus(id);
            DnaStatusDto status = dnaMapper.findStatus(id);
            List<DnaResultDto> results = dnaMapper.findResultsByBoardId(id);

            boolean fileExists = false;
            if (board.getFilepath() != null && !board.getFilepath().isEmpty()) {
                File f = new File(board.getFilepath());
                fileExists = f.exists();
            }

            model.addAttribute("board", board);
            model.addAttribute("status", status);
            model.addAttribute("results", results);
            model.addAttribute("fileExists", fileExists);

            return "board/view";
        }

        return "redirect:/board/list";
    }

    @GetMapping("/download")
    public void download(@RequestParam String filename, HttpServletResponse response) throws IOException {
        Path path = Paths.get(uploadDir + filename);
        if (Files.exists(path)) {
            response.setHeader("Content-Disposition", "attachment; filename=" + URLEncoder.encode(filename, StandardCharsets.UTF_8));
            Files.copy(path, response.getOutputStream());
        }
    }

    @GetMapping("/edit")
    public String editForm(@RequestParam("id") Long id, HttpSession session, Model model) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        BoardDto board = boardMapper.findById(id);

        if (user != null && board != null && (user.getUsername().equalsIgnoreCase(board.getWriter()) || user.getUsername().equalsIgnoreCase("admin"))) {
            model.addAttribute("board", board);
            return "board/edit";
        }

        return "redirect:/board/list";
    }

    @PostMapping("/edit")
    public String edit(BoardDto boardDto) {
        boardMapper.update(boardDto);
        return "redirect:/board/view?id=" + boardDto.getId();
    }

    @GetMapping("/delete")
    public String delete(@RequestParam("id") Long id, HttpSession session) {
        UserDto user = (UserDto) session.getAttribute("loginUser");

        if (user != null && (user.getId().equals(id) || user.getUsername().equalsIgnoreCase("admin"))) {
            dnaMapper.deleteResultsByBoardId(id);
            dnaMapper.deleteStatusByBoardId(id);
            boardMapper.delete(id);
        }

        return "redirect:/board/list";
    }
}
