package com.project.rookies.mapper;

import com.project.rookies.dto.FamilyRelationDto;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface FamilyRelationMapper {
    List<FamilyRelationDto> findByUserId(@Param("userId") Long userId);
    List<FamilyRelationDto> searchByUserIdAndName(@Param("userId") Long userId, @Param("keyword") String keyword);
    void add(FamilyRelationDto dto);
    void delete(@Param("id") Long id, @Param("userId") Long userId);
    void deleteByUserId(@Param("userId") Long userId);
}
