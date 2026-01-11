package com.project.rookies.config;

import jakarta.annotation.PostConstruct;
import org.springframework.stereotype.Component;

import java.io.File;

@Component
public class AppConfig {

    private String uploadPath;

    @PostConstruct
    public void init() {
        String os = System.getProperty("os.name").toLowerCase();

        if (os.contains("win")) {
            this.uploadPath = "C:/rookies/upload/";
        } else {
            this.uploadPath = "/var/www/rookies/upload/";
        }

        // 디렉토리 자동 생성
        File folder = new File(this.uploadPath);
        if (!folder.exists()) {
            boolean created = folder.mkdirs();
            if (created) {
                System.out.println("[AppConfig] 기본 디렉토리 생성 완료: " + this.uploadPath);
            } else {
                // 리눅스에서 권한이 없으면 실패할 수 있음
                System.err.println("[AppConfig] 디렉토리 생성 실패 (권한 확인 필요): " + this.uploadPath);
                System.err.println("'sudo mkdir -p /var/www/rookies && sudo chown -R $USER:$USER /var/www/rookies' 명령어를 실행해보세요.");
            }
        } else {
            System.out.println("[AppConfig] 기본 디렉토리 감지됨: " + this.uploadPath);
        }
    }

    public String getUploadPath() {
        return this.uploadPath;
    }
}