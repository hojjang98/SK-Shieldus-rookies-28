package com.project.rookies.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @GetMapping("/")
    public String home() {
        return "home/home";
    }

    @GetMapping("/about")
    public String about() {
        return "home/about";
    }

    @GetMapping("/services")
    public String services() {
        return "home/services";
    }
}
