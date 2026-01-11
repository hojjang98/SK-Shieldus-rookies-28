package com.project.rookies.mapper;

import com.project.rookies.dto.DnaResultDto;
import com.project.rookies.dto.DnaStatusDto;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import java.util.List;

@Mapper
public interface DnaMapper {
    DnaStatusDto findStatus(@Param("boardId") Long boardId);
    void ensureStatus(@Param("boardId") Long boardId);
    void updateStatus(@Param("boardId") Long boardId, @Param("status") String status);

    List<DnaResultDto> findResultsByBoardId(@Param("boardId") Long boardId);
    List<DnaResultDto> findResultsForUser(@Param("writer") String writer);
    DnaResultDto findResultById(@Param("id") Long id);
    void saveResult(DnaResultDto dto);

    void deleteResultsByBoardId(@Param("boardId") Long boardId);
    void deleteResultsByUserWriter(@Param("writer") String writer);
    void deleteStatusByBoardId(@Param("boardId") Long boardId);
}
