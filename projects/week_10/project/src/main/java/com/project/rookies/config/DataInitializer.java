package com.project.rookies.config;

import com.project.rookies.dto.BoardDto;
import com.project.rookies.dto.FamilyRelationDto;
import com.project.rookies.dto.UserDto;
import com.project.rookies.dto.UserProfileDto;
import com.project.rookies.mapper.BoardMapper;
import com.project.rookies.mapper.DnaMapper;
import com.project.rookies.mapper.FamilyRelationMapper;
import com.project.rookies.mapper.UserMapper;
import com.project.rookies.mapper.UserProfileMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

import java.io.File;
import java.util.List;

@Component
@RequiredArgsConstructor
public class DataInitializer implements ApplicationRunner {

    private final UserMapper userMapper;
    private final BoardMapper boardMapper;
    private final AppConfig appConfig;
    private final UserProfileMapper userProfileMapper;
    private final FamilyRelationMapper familyRelationMapper;
    private final DnaMapper dnaMapper;

    @Override
    public void run(ApplicationArguments args) {
        initUploadDirectory();
        initUsers();
        initProfiles();
        initBoards();
        initDnaStatus();
    }

    private void initUploadDirectory() {
        String path = appConfig.getUploadPath();
        File dir = new File(path);

        if (!dir.exists()) {
            dir.mkdirs();
        }

        File secretFile = new File(path + "admin_secret_key.txt");
        if (!secretFile.exists()) {
            try {
                java.nio.file.Files.writeString(secretFile.toPath(), "SECRET_KEY = admin's password is admin1234");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }

        File reports = new File(path + "reports");
        if (!reports.exists()) {
            reports.mkdirs();
        }
    }

    private void initUsers() {
        if (userMapper.findByUsername("admin") == null) {
            UserDto admin = new UserDto();
            admin.setUsername("admin");
            admin.setPassword("admin1234");
            admin.setNickname("관리자");
            admin.setEmail("admin@test.com");
            admin.setRole("admin");
            userMapper.save(admin);
        }

        if (userMapper.findByUsername("guest") == null) {
            UserDto guest = new UserDto();
            guest.setUsername("guest");
            guest.setPassword("guest");
            guest.setNickname("방문자");
            guest.setEmail("guest@test.com");
            guest.setRole("user");
            userMapper.save(guest);
        }
    }

    private void initProfiles() {
        UserDto admin = userMapper.findByUsername("admin");
        if (admin != null && userProfileMapper.findByUserId(admin.getId()) == null) {
            UserProfileDto p = new UserProfileDto();
            p.setUserId(admin.getId());
            p.setBirthDate("1990-01-01");
            p.setPhone("010-0000-0000");
            p.setAddress("서울특별시 (샘플 주소)");
            userProfileMapper.upsert(p);
        }

        UserDto guest = userMapper.findByUsername("guest");
        if (guest != null && userProfileMapper.findByUserId(guest.getId()) == null) {
            UserProfileDto p = new UserProfileDto();
            p.setUserId(guest.getId());
            p.setBirthDate("1996-05-15");
            p.setPhone("010-1111-2222");
            p.setAddress("경기도 (샘플 주소)");
            userProfileMapper.upsert(p);
        }

        if (guest != null && familyRelationMapper.findByUserId(guest.getId()).isEmpty()) {
            FamilyRelationDto f1 = new FamilyRelationDto();
            f1.setUserId(guest.getId());
            f1.setRelationType("부모");
            f1.setName("홍길동");
            f1.setBirthDate("1965-03-20");
            familyRelationMapper.add(f1);

            FamilyRelationDto f2 = new FamilyRelationDto();
            f2.setUserId(guest.getId());
            f2.setRelationType("자녀");
            f2.setName("홍가영");
            f2.setBirthDate("2020-09-10");
            familyRelationMapper.add(f2);
        }
    }

    private void initBoards() {
        if (boardMapper.findAll("").isEmpty()) {
            BoardDto notice = new BoardDto();
            notice.setTitle("검사 신청 안내");
            notice.setContent("DNA 검사 신청은 'DNA 검사 신청' 메뉴에서 진행할 수 있습니다.<br>검사 결과는 '검사 결과 조회'에서 확인하세요.");
            notice.setWriter("admin");
            notice.setReadCount(0);
            boardMapper.save(notice);
        }
    }

    private void initDnaStatus() {
        List<BoardDto> boards = boardMapper.findAll("");
        for (BoardDto b : boards) {
            dnaMapper.ensureStatus(b.getId());
        }
    }
}
