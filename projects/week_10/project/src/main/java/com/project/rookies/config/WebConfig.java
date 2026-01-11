package com.project.rookies.config;

import lombok.RequiredArgsConstructor;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new LoginCheckInterceptor())
                .addPathPatterns("/**")
                .excludePathPatterns(
                        "/",
                        "/login",
                        "/join",
                        "/join/send",
                        "/error",
                        "/css/**",
                        "/js/**",
                        "/uploads/**",
                        "/files/**",
                        "/about",
                        "/services",
                        "/agreement",
                        "/find-password",
                        "/reset-password"
                );
    }

}
