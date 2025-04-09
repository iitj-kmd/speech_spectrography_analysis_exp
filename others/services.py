import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.core.io.Resource;
import org.springframework.http.client.ClientHttpRequestFactory;
import org.springframework.http.client.HttpComponentsClientHttpRequestFactory;
import org.springframework.web.client.RestTemplate;

import javax.net.ssl.SSLContext;
import java.io.IOException;
import java.security.KeyManagementException;
import java.security.KeyStore;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;

@Configuration
public class RestTemplateConfig {

    @Value("${truststore.path}")
    private Resource truststorePath;

    @Value("${truststore.password}")
    private String truststorePassword;

    @Bean
    public RestTemplate restTemplate(ClientHttpRequestFactory clientHttpRequestFactory) {
        return new RestTemplate(clientHttpRequestFactory);
    }

    @Bean
    public ClientHttpRequestFactory clientHttpRequestFactory() {
        try {
            KeyStore trustStore = KeyStore.getInstance("JKS");
            trustStore.load(truststorePath.getInputStream(), truststorePassword.toCharArray());

            SSLContext sslContext = org.apache.http.ssl.SSLContexts.custom()
                    .loadTrustMaterial(trustStore, null) // No key manager needed for client-side trust
                    .build();

            SSLConnectionSocketFactory socketFactory = new SSLConnectionSocketFactory(sslContext);
            CloseableHttpClient httpClient = HttpClients.custom()
                    .setSSLSocketFactory(socketFactory)
                    .build();

            HttpComponentsClientHttpRequestFactory clientHttpRequestFactory =
                    new HttpComponentsClientHttpRequestFactory(httpClient);
            return clientHttpRequestFactory;

        } catch (KeyStoreException | IOException | NoSuchAlgorithmException | CertificateException | KeyManagementException e) {
            throw new IllegalStateException("Failed to initialize client request factory with truststore", e);
        }
    }
}
