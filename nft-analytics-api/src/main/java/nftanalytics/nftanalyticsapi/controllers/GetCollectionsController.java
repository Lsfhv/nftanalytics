package nftanalytics.nftanalyticsapi.controllers;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import nftanalytics.nftanalyticsapi.database.PostgresSQL;

import java.util.ArrayList;
import java.util.HashMap;

@CrossOrigin
@RestController
public class GetCollectionsController extends Controller {
    
    @RequestMapping("/getcollections") 
    public HashMap<String, String> getCollections() throws JsonProcessingException {
        PostgresSQL psql = new PostgresSQL();
        ObjectMapper mapper = new ObjectMapper();
        ArrayList<CollectionModel> collections = new ArrayList<>();
        HashMap<String, String> map = new HashMap<>();
        psql.selectStatement("select name, address, openseaSlug from slug").forEach(row -> {
            collections.add(new CollectionModel(row.get(0), row.get(1), row.get(2))); 
        });
        map.put(RESULT, mapper.writeValueAsString(collections));
        return map;
    }
}
