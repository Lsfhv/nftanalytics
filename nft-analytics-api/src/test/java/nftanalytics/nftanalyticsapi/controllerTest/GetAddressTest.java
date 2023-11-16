package nftanalytics.nftanalyticsapi.controllerTest;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import nftanalytics.nftanalyticsapi.controllers.GetAddressController;
import nftanalytics.nftanalyticsapi.database.PostgresSQL;

import static org.assertj.core.api.Assertions.assertThat;

import java.util.HashMap;
import java.util.ArrayList;
import java.util.concurrent.ThreadLocalRandom;

@SpringBootTest
public class GetAddressTest {

    @Autowired
	private GetAddressController controller;

    @Test
    void contextLoads() {
        assertThat(controller).isNotNull();
    }

    @Test
    void getAddressTest() {
        HashMap<String, String> result; 
        result = controller.getAddress("cool-cats-nft");
        assertThat(result.get("result")).isEqualTo("0x1A92f7381B9F03921564a437210bB9396471050C");

        result = controller.getAddress("fake sldfjsalfafd");
        assertThat(result.get("result")).isEqualTo("Not found");
    }

    @Test
    void getAddressTestRandom() {
        HashMap<String, String> result; 
        PostgresSQL psql = new PostgresSQL(); 
        ArrayList<ArrayList<String>> slugs = psql.selectStatement("select openseaSlug, address from slug");
        int randomNum = ThreadLocalRandom.current().nextInt(0, slugs.size());
        String slug = slugs.get(randomNum).get(0);
        String address = slugs.get(randomNum).get(1);

        result = controller.getAddress(slug);
        assertThat(result.get("result")).isEqualTo(address);
    }
}
