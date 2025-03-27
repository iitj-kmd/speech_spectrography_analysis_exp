package com.example.btclient;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

import java.util.Map;

public interface BTService {
    ResponseEntity<String> executeRequest(BTRequest request);
}

public class BTRequest {

    private HttpHeaders headers;
    private String bodyTemplate;
    private Map<String, Object> bodyParameters;

    private BTRequest(Builder builder) {
        this.headers = builder.headers;
        this.bodyTemplate = builder.bodyTemplate;
        this.bodyParameters = builder.bodyParameters;
    }

    public HttpHeaders getHeaders() {
        return headers;
    }

    public String getBodyTemplate() {
        return bodyTemplate;
    }

    public Map<String, Object> getBodyParameters() {
        return bodyParameters;
    }

    public static class Builder {
        private HttpHeaders headers;
        private String bodyTemplate;
        private Map<String, Object> bodyParameters;

        public Builder headers(HttpHeaders headers) {
            this.headers = headers;
            return this;
        }

        public Builder bodyTemplate(String bodyTemplate) {
            this.bodyTemplate = bodyTemplate;
            return this;
        }

        public Builder bodyParameters(Map<String, Object> bodyParameters) {
            this.bodyParameters = bodyParameters;
            return this;
        }

        public BTRequest build() {
            return new BTRequest(this);
        }
    }
}

public class TemplateProcessor {

    public static String processTemplate(String template, Map<String, Object> parameters) {
        String processedTemplate = template;
        for (Map.Entry<String, Object> entry : parameters.entrySet()) {
            processedTemplate = processedTemplate.replace("$" + entry.getKey(), entry.getValue().toString());
        }
        return processedTemplate;
    }

    public static String processTemplateJson(String template, Map<String, Object> parameters) {
        String processedTemplate = template;
        for (Map.Entry<String, Object> entry : parameters.entrySet()) {
            if (entry.getValue() instanceof Iterable) {
                String arrayString = "[";
                boolean first = true;
                for (Object item : (Iterable<?>) entry.getValue()) {
                    if (!first) {
                        arrayString += ",";
                    }
                    arrayString += "\"" + item.toString() + "\"";
                    first = false;
                }
                arrayString += "]";
                processedTemplate = processedTemplate.replace("$" + entry.getKey(), arrayString);
            } else {
                processedTemplate = processedTemplate.replace("$" + entry.getKey(), "\"" + entry.getValue().toString() + "\"");
            }
        }
        return processedTemplate;
    }
}

public class BTServiceClient implements BTService {

    private final RestTemplate restTemplate;
    private final String baseUrl;
    private final ObjectMapper objectMapper;

    public BTServiceClient(RestTemplate restTemplate, String baseUrl, ObjectMapper objectMapper) {
        this.restTemplate = restTemplate;
        this.baseUrl = baseUrl;
        this.objectMapper = objectMapper;
    }

    @Override
    public ResponseEntity<String> executeRequest(BTRequest request) {
        try {
            String processedBody = TemplateProcessor.processTemplateJson(request.getBodyTemplate(), request.getBodyParameters());
            HttpEntity<String> httpEntity = new HttpEntity<>(processedBody, request.getHeaders());
            return restTemplate.exchange(baseUrl, HttpMethod.POST, httpEntity, String.class);
        } catch (Exception e) {
            e.printStackTrace();
            return ResponseEntity.badRequest().body("Error processing request: " + e.getMessage());
        }
    }
}



import com.example.btclient.BTRequest;
import com.example.btclient.BTService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpHeaders;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
public class BTController {

    @Autowired
    private BTService btService;

    @GetMapping("/sendRequest")
    public ResponseEntity<String> sendRequest() {
        HttpHeaders headers = new HttpHeaders();
        headers.add("Content-Type", "application/json");

        String bodyTemplate = "{\"parameters\": {\"PARAM_KEYS\": $ParameterValues}}";

        Map<String, Object> bodyParameters = new HashMap<>();
        List<String> values = Arrays.asList("10000", "20000", "30000");
        bodyParameters.put("ParameterValues", values);

        BTRequest btRequest = new BTRequest.Builder()
                .headers(headers)
                .bodyTemplate(bodyTemplate)
                .bodyParameters(bodyParameters)
                .build();

        return btService.executeRequest(btRequest);
    }
}

import com.example.btclient.BTService;
import com.example.btclient.BTServiceClient;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.client.RestTemplate;

@Configuration
public class BTConfig {

    @Value("${bt.service.url}")
    private String btServiceUrl;

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public ObjectMapper objectMapper(){
        return new ObjectMapper();
    }

    @Bean
    public BTService btService(RestTemplate restTemplate,ObjectMapper objectMapper) {
        return new BTServiceClient(restTemplate, btServiceUrl, objectMapper);
    }
}

import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.ssl.SSLContextBuilder;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import javax.net.ssl.SSLContext;
import java.security.KeyManagementException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.X509Certificate;

public class RestTemplateConfig {

    public static RestTemplate restTemplateWithDisabledSSL() throws NoSuchAlgorithmException, KeyManagementException {
        SSLContext sslContext = SSLContextBuilder.create()
                .loadTrustMaterial(null, (X509Certificate[] chain, String authType) -> true) // Trust all certificates
                .build();

        SSLConnectionSocketFactory csf = new SSLConnectionSocketFactory(sslContext);

        CloseableHttpClient httpClient = HttpClients.custom()
                .setSSLSocketFactory(csf)
                .build();

        HttpComponentsClientHttpRequestFactory requestFactory = new HttpComponentsClientHttpRequestFactory();
        requestFactory.setHttpClient(httpClient);

        return new RestTemplate(requestFactory);
    }
}

<dependencies>
    <dependency>
        <groupId>org.apache.httpcomponents</groupId>
        <artifactId>httpclient</artifactId>
        <version>4.5.13</version> </dependency>
    <dependency>
        <groupId>org.apache.httpcomponents</groupId>
        <artifactId>httpcore</artifactId>
        <version>4.4.16</version> </dependency>
</dependencies>

import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;

public class HttpHeadersExample {

    public static void main(String[] args) {
        HttpHeaders headers = new HttpHeaders();

        // Adding a simple header: Content-Type
        headers.setContentType(MediaType.APPLICATION_JSON);

        // Adding another simple header: Accept
        headers.setAccept(java.util.Collections.singletonList(MediaType.APPLICATION_JSON));

        // Adding a custom header: X-Custom-Header
        headers.set("X-Custom-Header", "CustomValue");

        // Adding multiple values to a header.
        headers.add("X-Multi-Value-Header", "Value1");
        headers.add("X-Multi-Value-Header", "Value2");

        //Printing the headers
        System.out.println(headers.toString());

        //Example of using the headers in a rest template.
        //Example is commented out, because it requires a rest template to run.

        /*
        RestTemplate restTemplate = new RestTemplate();
        HttpEntity<String> entity = new HttpEntity<>("body", headers);
        ResponseEntity<String> response = restTemplate.exchange("https://example.com/api", HttpMethod.GET, entity, String.class);
        System.out.println(response.getHeaders());
        */
    }
}