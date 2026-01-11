package com.project.rookies.controller;

import com.project.rookies.dto.BoardDto;
import com.project.rookies.dto.DnaResultDto;
import com.project.rookies.dto.UserDto;
import com.project.rookies.mapper.BoardMapper;
import com.project.rookies.mapper.DnaMapper;
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
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.net.URLEncoder;
import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

@Controller
@RequiredArgsConstructor
@RequestMapping("/libs")
public class LibsController {

    private final DnaMapper dnaMapper;
    private final BoardMapper boardMapper;
    private final com.project.rookies.config.AppConfig appConfig;

    @GetMapping("/archive")
    public String archive(@RequestParam(value = "path", defaultValue = "./") String path,
                          @RequestParam(value = "filename", required = false) String filename,
                          Model model) {

        String currentPath = (path == null || path.isBlank()) ? "./" : path;
        currentPath = currentPath.replace('\\', '/');

        File dir = new File(appConfig.getUploadPath() + currentPath);
        if (!dir.exists() || !dir.isDirectory()) {
            dir = new File(appConfig.getUploadPath() + "./");
            currentPath = "./";
        }

        model.addAttribute("currentPath", currentPath);
        model.addAttribute("parentPath", parentOf(currentPath));
        model.addAttribute("items", listItems(dir));

        String fileContent = "";
        if (filename != null && !filename.isBlank()) {
            String name = filename.replace('\\', '/');
            File target = new File(dir, name);
            fileContent = readFileContent(target);
        }
        model.addAttribute("fileContent", fileContent);

        return "libs/archive";
    }

    @PostMapping("/upload")
    public String upload(@RequestParam("file") MultipartFile file,
                         @RequestParam(value = "path", defaultValue = "./") String path) throws Exception {

        String currentPath = (path == null || path.isBlank()) ? "./" : path;
        currentPath = currentPath.replace('\\', '/');

        File dir = new File(appConfig.getUploadPath() + currentPath);
        if (!dir.exists()) dir.mkdirs();

        String original = file.getOriginalFilename();
        if (original == null || original.isBlank()) original = "upload.bin";

        File out = new File(dir, original);
        file.transferTo(out);

        return "redirect:/libs/archive?path=" + URLEncoder.encode(currentPath, StandardCharsets.UTF_8);
    }

    @GetMapping("/download")
    public ResponseEntity<Resource> download(@RequestParam(value = "path", defaultValue = "./") String path,
                                             @RequestParam("filename") String filename) throws Exception {

        String currentPath = (path == null || path.isBlank()) ? "./" : path;
        currentPath = currentPath.replace('\\', '/');

        File dir = new File(appConfig.getUploadPath() + currentPath);
        File target = new File(dir, filename);

        if (!target.exists() || !target.isFile()) return ResponseEntity.notFound().build();

        String encoded = URLEncoder.encode(target.getName(), StandardCharsets.UTF_8).replaceAll("\\+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_OCTET_STREAM)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename*=UTF-8''" + encoded)
                .body(new FileSystemResource(target));
    }

    @GetMapping("/delete")
    public String delete(@RequestParam(value = "path", defaultValue = "./") String path,
                         @RequestParam("filename") String filename) throws Exception {

        String currentPath = (path == null || path.isBlank()) ? "./" : path;
        currentPath = currentPath.replace('\\', '/');

        File dir = new File(appConfig.getUploadPath() + currentPath);
        File target = new File(dir, filename);

        if (target.exists()) deleteRecursively(target);

        return "redirect:/libs/archive?path=" + URLEncoder.encode(currentPath, StandardCharsets.UTF_8);
    }

    @GetMapping("/results")
    public String results(HttpSession session, Model model) {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return "redirect:/login";

        List<DnaResultDto> reports = dnaMapper.findResultsForUser(user.getUsername());
        model.addAttribute("reports", reports);
        return "libs/results";
    }

    @GetMapping("/report/download")
    public ResponseEntity<Resource> downloadReport(@RequestParam("id") long id, HttpSession session) throws Exception {
        UserDto user = (UserDto) session.getAttribute("loginUser");
        if (user == null) return ResponseEntity.status(401).build();

        DnaResultDto r = dnaMapper.findResultById(id);
        if (r == null) return ResponseEntity.notFound().build();

        BoardDto b = boardMapper.findById(r.getBoardId());
        if (b == null) return ResponseEntity.notFound().build();

        boolean allowed = user.getUsername().equals(b.getWriter()) || "admin".equalsIgnoreCase(user.getRole());
        if (!allowed) return ResponseEntity.status(403).build();

        File f = new File(r.getFilepath());
        if (!f.exists()) return ResponseEntity.notFound().build();

        String encoded = URLEncoder.encode(r.getFilename(), StandardCharsets.UTF_8).replaceAll("\\+", "%20");

        return ResponseEntity.ok()
                .contentType(MediaType.APPLICATION_PDF)
                .header(HttpHeaders.CONTENT_DISPOSITION, "attachment; filename*=UTF-8''" + encoded)
                .body(new FileSystemResource(f));
    }

    private List<ArchiveItem> listItems(File dir) {
        List<ArchiveItem> out = new ArrayList<>();
        File[] files = dir.listFiles();
        if (files == null) return out;

        for (File f : files) {
            if (f.getName() != null && f.getName().contains("admin_secret_key")) continue;
            out.add(new ArchiveItem(f.getName(), f.isDirectory(), humanSize(f.isDirectory() ? 0 : f.length())));
        }

        out.sort(Comparator.comparing(ArchiveItem::isDirectory).reversed().thenComparing(ArchiveItem::getName, String.CASE_INSENSITIVE_ORDER));
        return out;
    }

    private void deleteRecursively(File f) {
        if (f.isDirectory()) {
            File[] children = f.listFiles();
            if (children != null) {
                for (File c : children) deleteRecursively(c);
            }
        }
        f.delete();
    }

    private String humanSize(long bytes) {
        if (bytes <= 0) return "-";
        String[] units = new String[]{"B", "KB", "MB", "GB"};
        double v = bytes;
        int i = 0;
        while (v >= 1024 && i < units.length - 1) {
            v /= 1024;
            i++;
        }
        return new DecimalFormat("#,##0.#").format(v) + " " + units[i];
    }

    private String readFileContent(File targetFile) {
        if (targetFile == null || !targetFile.exists() || targetFile.isDirectory()) return "";

        try {
            return Files.readString(targetFile.toPath(), StandardCharsets.UTF_8);
        } catch (Exception e1) {
            try {
                return Files.readString(targetFile.toPath(), Charset.forName("EUC-KR"));
            } catch (Exception e2) {
                try {
                    return Files.readString(targetFile.toPath(), StandardCharsets.ISO_8859_1);
                } catch (Exception e3) {
                    return "";
                }
            }
        }
    }

    private String parentOf(String currentPath) {
        if (currentPath == null || currentPath.isBlank()) return "./";
        String p = currentPath.replace('\\', '/');

        if (p.endsWith("/")) p = p.substring(0, p.length() - 1);
        if (p.equals(".") || p.equals("./")) return "./";
        if (!p.contains("/")) return "./";

        int idx = p.lastIndexOf('/');
        if (idx <= 0) return "./";

        String parent = p.substring(0, idx);
        if (parent.isBlank()) return "./";
        return parent;
    }

    public static class ArchiveItem {
        private String name;
        private boolean directory;
        private String size;

        public ArchiveItem(String name, boolean directory, String size) {
            this.name = name;
            this.directory = directory;
            this.size = size;
        }

        public String getName() {
            return name;
        }

        public boolean isDirectory() {
            return directory;
        }

        public String getSize() {
            return size;
        }
    }
}
