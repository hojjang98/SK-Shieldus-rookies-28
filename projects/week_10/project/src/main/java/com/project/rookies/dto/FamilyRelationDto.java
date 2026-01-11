package com.project.rookies.dto;

import lombok.Data;

@Data
public class FamilyRelationDto {
    private Long id;
    private Long userId;
    private String relationType;
    private String name;
    private String birthDate;
    private String createdAt;
}
