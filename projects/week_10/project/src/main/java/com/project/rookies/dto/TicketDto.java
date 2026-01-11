package com.project.rookies.dto;

import lombok.Data;

@Data
public class TicketDto {
    private Long id;
    private String subject;
    private String resultLog;
    private String createdAt;
}