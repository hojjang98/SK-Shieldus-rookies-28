package com.project.rookies.controller;

import com.project.rookies.dto.TicketDto;
import com.project.rookies.mapper.TicketMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.Date;
import java.util.List;

@Controller
@RequiredArgsConstructor
public class SupportController {

    private final TicketMapper ticketMapper;

    @GetMapping("/support/ticket")
    public String ticketForm(Model model) {
        List<TicketDto> logs = ticketMapper.findAll();
        model.addAttribute("logs", logs);
        return "support/ticket";
    }

    @PostMapping("/support/ticket")
    public String createTicket(@RequestParam("subject") String subject, Model model) {

        String responseMsg = "";

        // [시나리오] 개발자의 실수:
        String serverSecret = "SK-SHIELDUS-ADMIN-KEY-2025";

        try {
            responseMsg = String.format("Ticket Created: " + subject + " (Date: %s)", new Date(), serverSecret);

        } catch (Exception e) {
            responseMsg = "System Error: " + e.getMessage();
        }

        // [DB 저장] DTO 생성 후 Mapper 호출
        TicketDto ticket = new TicketDto();
        ticket.setSubject(subject);
        ticket.setResultLog(responseMsg);

        ticketMapper.save(ticket); // DB에 영구 저장!

        // 화면 갱신을 위해 목록 다시 조회
        model.addAttribute("result", responseMsg);
        model.addAttribute("logs", ticketMapper.findAll());

        return "support/ticket";
    }
}