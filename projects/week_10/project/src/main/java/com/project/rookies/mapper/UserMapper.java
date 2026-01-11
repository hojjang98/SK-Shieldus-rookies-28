package com.project.rookies.mapper;

import com.project.rookies.dto.UserDto;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface UserMapper {
    UserDto login(@Param("username") String username, @Param("password") String password);
    void save(UserDto userDto);
    UserDto findByUsername(@Param("username") String username);
    UserDto findByUsernameAndEmail(@Param("username") String username, @Param("email") String email);
    void update(UserDto userDto);
    void delete(Long id);
    List<UserDto> findAllUsers();
}
