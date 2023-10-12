package nftanalytics.nftanalyticsapi.getCollections;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;

import nftanalytics.nftanalyticsapi.database.PostgresSQL;
import java.util.ArrayList;

@CrossOrigin
@RestController
public class GetCollectionsController {
    
    @RequestMapping("/getcollections") 
    public String getCollections() throws JsonProcessingException {
        Connection conn = new PostgresSQL().getConnection();
        ObjectMapper mapper = new ObjectMapper();

        ArrayList<CollectionModel> collections = new ArrayList<>();

        try {
            Statement st = conn.createStatement();
            ResultSet rs = st.executeQuery("select * from slug");
            while (rs.next()) {
                collections.add(new CollectionModel(rs.getString("display_name"), rs.getString("address"), rs.getString("opensea"))); 
            }
        } catch (Exception e) {
            e.printStackTrace();
        }

        return mapper.writeValueAsString(collections);
    }
}
