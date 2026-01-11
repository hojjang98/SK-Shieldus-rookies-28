package com.project.rookies.mapper;

import com.project.rookies.dto.UserProfileDto;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

@Mapper
public interface UserProfileMapper {
    UserProfileDto findByUserId(@Param("userId") Long userId);
    void upsert(UserProfileDto dto);
    void deleteByUserId(@Param("userId") Long userId);
}
