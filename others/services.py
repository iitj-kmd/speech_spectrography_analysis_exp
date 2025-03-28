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

import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.stereotype.Component;

@SpringBootApplication
public class CommandLineApp {

    public static void main(String[] args) {
        SpringApplication.run(CommandLineApp.class, args);
    }

    @Component
    public static class MyCommandLineRunner implements CommandLineRunner {

        @Override
        public void run(String... args) throws Exception {
            System.out.println("Hello from Spring Boot Command Line App!");

            if (args.length > 0) {
                System.out.println("Arguments passed:");
                for (String arg : args) {
                    System.out.println("- " + arg);
                }
            } else {
                System.out.println("No arguments passed.");
            }

            // Optionally, you can add more logic here.
            // For example, reading files, processing data, etc.
        }
    }
}

import java.util.HashMap;
import java.util.Map;

public class EnumExample {

    public enum StringEnum {
        VALUE_ONE("This is value one"),
        VALUE_TWO("Another value here"),
        SPECIAL_VALUE("A very special string"),
        DEFAULT_VALUE("Default string");

        private final String value;

        StringEnum(String value) {
            this.value = value;
        }

        public String getValue() {
            return value;
        }

        //Optional: A method to retrieve an enum by its name (string)
        private static final Map<String, StringEnum> stringToEnum = new HashMap<>();

        static {
            for (StringEnum enumValue : values()) {
                stringToEnum.put(enumValue.name(), enumValue);
            }
        }

        public static StringEnum fromString(String name) {
            return stringToEnum.get(name);
        }
    }

    public static void main(String[] args) {
        // Accessing enum values
        System.out.println(StringEnum.VALUE_ONE.getValue()); // Output: This is value one
        System.out.println(StringEnum.SPECIAL_VALUE.getValue()); // Output: A very special string

        //Retrieving an enum instance from a String.
        String enumName = "VALUE_TWO";
        StringEnum retrievedEnum = StringEnum.fromString(enumName);

        if(retrievedEnum != null){
            System.out.println(retrievedEnum.getValue()); // Output: Another value here
        } else {
            System.out.println("Enum not found for: " + enumName);
        }

        //Retrieving an enum instance from a String that does not exist.
        String enumName2 = "VALUE_THREE";
        StringEnum retrievedEnum2 = StringEnum.fromString(enumName2);

        if(retrievedEnum2 != null){
            System.out.println(retrievedEnum2.getValue());
        } else {
            System.out.println("Enum not found for: " + enumName2); // Output: Enum not found for: VALUE_THREE
        }
    }
}

////////////////////////////////////////////////////////////////
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;

@Service
public class ExternalApiService {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public ExternalApiService(RestTemplate restTemplate, ObjectMapper objectMapper) {
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
    }

    public YourDataObject fetchDataFromExternalService(String externalServiceUrl, Object requestBody) throws IOException {

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<Object> entity = new HttpEntity<>(requestBody, headers);

        ResponseEntity<String> response = restTemplate.exchange(
                externalServiceUrl,
                HttpMethod.POST, // Or GET, PUT, DELETE as needed
                entity,
                String.class);

        if (response.getStatusCode() == HttpStatus.OK) {
            String responseBody = response.getBody();
            return processResponse(responseBody);
        } else {
            // Handle non-OK status codes (e.g., 4xx, 5xx)
            throw new RuntimeException("External service returned status code: " + response.getStatusCode());
        }
    }

    private YourDataObject processResponse(String responseBody) throws IOException {
        JsonNode rootNode = objectMapper.readTree(responseBody);

        JsonNode statusNode = rootNode.get("status");
        if (statusNode != null && "failure".equalsIgnoreCase(statusNode.asText())) {
            // Handle failure case
            JsonNode errorMessageNode = rootNode.get("errorMessage"); //or whatever error field is called
            String errorMessage = errorMessageNode != null ? errorMessageNode.asText() : "Unknown failure";
            throw new RuntimeException("External service returned failure: " + errorMessage);
        }

        // Handle success case (parse the data into YourDataObject)
        // Example: Assume the success data is under a "data" node
        JsonNode dataNode = rootNode.get("data");

        if (dataNode == null){
            throw new RuntimeException("External service returned success, but data node is missing.");
        }

        // Example: Convert dataNode to YourDataObject
        // Adjust the conversion logic based on the actual structure of YourDataObject
        try {
            return objectMapper.treeToValue(dataNode, YourDataObject.class);
        } catch (IOException e){
            throw new RuntimeException("Error mapping JSON to YourDataObject", e);
        }

    }

    // Example YourDataObject class (replace with your actual data class)
    public static class YourDataObject {
        private String field1;
        private int field2;

        // Constructors, getters, setters, etc.
        public String getField1() {
            return field1;
        }

        public void setField1(String field1) {
            this.field1 = field1;
        }

        public int getField2() {
            return field2;
        }

        public void setField2(int field2) {
            this.field2 = field2;
        }
    }
}



////////////////////////////////////
////////////////////////////////////////////////////////////


import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.HttpStatus;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;

@Component
public class ExternalApiClientRestTemplate {

    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public ExternalApiClientRestTemplate(RestTemplate restTemplate, ObjectMapper objectMapper) {
        this.restTemplate = restTemplate;
        this.objectMapper = objectMapper;
    }

    public YourDataObject fetchData(String externalServiceUrl, Object requestBody) throws IOException {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        HttpEntity<Object> entity = new HttpEntity<>(requestBody, headers);

        ResponseEntity<String> response = restTemplate.exchange(
                externalServiceUrl,
                HttpMethod.POST,
                entity,
                String.class);

        if (response.getStatusCode() == HttpStatus.OK) {
            return processResponse(response.getBody());
        } else {
            throw new RuntimeException("External API call failed with status: " + response.getStatusCode());
        }
    }

    private YourDataObject processResponse(String responseBody) throws IOException {
        JsonNode rootNode = objectMapper.readTree(responseBody);

        JsonNode statusNode = rootNode.get("status");
        if (statusNode != null && "failure".equalsIgnoreCase(statusNode.asText())) {
            String errorMessage = rootNode.path("errorMessage").asText("Unknown failure");
            throw new RuntimeException("External API returned failure: " + errorMessage);
        }

        JsonNode dataNode = rootNode.get("data");
        if (dataNode == null) {
            throw new RuntimeException("External API response missing 'data' node");
        }
        return objectMapper.treeToValue(dataNode, YourDataObject.class);
    }

    // YourDataObject class (replace with your actual data class)
    public static class YourDataObject {
        private String field1;
        private int field2;
        // ... getters, setters, constructors ...
    }
}



