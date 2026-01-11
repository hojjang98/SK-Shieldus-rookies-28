package com.project.rookies.dto;

import lombok.Data;

@Data
public class DnaResultDto {
    private Long id;
    private Long boardId;
    private String category;
    private String filename;
    private String filepath;
    private String uploadedAt;
}
