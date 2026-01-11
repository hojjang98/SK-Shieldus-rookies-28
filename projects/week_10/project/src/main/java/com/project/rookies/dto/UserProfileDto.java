package com.project.rookies.dto;

import lombok.Data;

@Data
public class UserProfileDto {
    private Long userId;
    private String birthDate;
    private String phone;
    private String address;
    private String updatedAt;
}
