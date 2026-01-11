package com.project.rookies.mapper;

import com.project.rookies.dto.TicketDto;
import org.apache.ibatis.annotations.Mapper;
import java.util.List;

@Mapper
public interface TicketMapper {
    void save(TicketDto ticketDto);
    List<TicketDto> findAll();
}
