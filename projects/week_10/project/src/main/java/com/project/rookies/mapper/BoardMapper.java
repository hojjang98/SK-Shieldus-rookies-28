package com.project.rookies.mapper;

import com.project.rookies.dto.BoardDto;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import java.util.List;

@Mapper
public interface BoardMapper {
    // 1. 목록 조회 (검색 포함)
    List<BoardDto> findAll(@Param("keyword") String keyword);
    List<BoardDto> findByWriter(@Param("writer") String writer, @Param("keyword") String keyword);
    List<BoardDto> findByWriterOrAdmin(@Param("writer") String writer, @Param("keyword") String keyword);

    // 2. 상세 조회
    BoardDto findById(Long id);

    // 3. 글 저장
    void save(BoardDto boardDto);

    // 4. 글 수정
    void update(BoardDto boardDto);

    // 5. 글 삭제
    void delete(Long id);
    long count();
}