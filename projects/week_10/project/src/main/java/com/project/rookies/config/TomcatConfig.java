package com.project.rookies.config;

import org.apache.catalina.Context;
import org.apache.catalina.Wrapper;
import org.apache.catalina.startup.Tomcat;
import org.springframework.boot.web.embedded.tomcat.TomcatServletWebServerFactory;
import org.springframework.boot.web.embedded.tomcat.TomcatWebServer;
import org.springframework.boot.web.server.WebServerFactoryCustomizer;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.io.File;

@Configuration
public class TomcatConfig {

    /**
     * [Tomcat 취약점 구현]
     * 특정 URL(/uploads)로 접근 시, 파일 목록(Directory Listing)을 강제로 보여줌.
     * AppConfig를 통해 OS(Windows/Linux)에 맞는 경로를 자동으로 가져옴.
     */
    @Bean
    public TomcatServletWebServerFactory servletContainer(AppConfig appConfig) {
        return new TomcatServletWebServerFactory() {
            @Override
            protected TomcatWebServer getTomcatWebServer(Tomcat tomcat) {

                // 1. OS별 업로드 경로 가져오기
                String docBase = appConfig.getUploadPath();
                if (docBase.endsWith("/") || docBase.endsWith("\\")) {
                    docBase = docBase.substring(0, docBase.length() - 1);
                }
                new File(docBase).mkdirs();

                // 2. 톰캣에 '/uploads' 라는 별도 컨텍스트(Context) 추가
                // 메인 앱(/)과는 별개로 동작하는 구역을 만드는 것입니다.
                Context context = tomcat.addContext("/dirs", docBase);

                // 3. 해당 컨텍스트에 DefaultServlet (파일 목록 보여주는 서블릿) 등록
                Wrapper defaultServlet = context.createWrapper();
                defaultServlet.setName("default");
                defaultServlet.setServletClass("org.apache.catalina.servlets.DefaultServlet");

                // [핵심] listings = true (디렉터리 리스팅 활성화)
                defaultServlet.addInitParameter("listings", "true");
                defaultServlet.addInitParameter("debug", "0");
                defaultServlet.setLoadOnStartup(1);

                // 4. 서블릿 매핑
                context.addChild(defaultServlet);
                context.addServletMappingDecoded("/", "default");

                return super.getTomcatWebServer(tomcat);
            }
        };
    }
}