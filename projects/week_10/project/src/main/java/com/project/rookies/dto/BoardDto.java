package com.project.rookies.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class BoardDto {
    private Long id;
    private String title;
    private String content;
    private String writer;
    private String filename;
    private String filepath;
    private int readCount;
    private String createdAt;
}
