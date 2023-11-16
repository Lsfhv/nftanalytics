package nftanalytics.nftanalyticsapi.controllers;

import java.util.HashMap;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import nftanalytics.nftanalyticsapi.database.PostgresSQL;
import java.util.ArrayList; 
@CrossOrigin
@RestController
public class GetAddressController extends Controller {

    @RequestMapping("/getaddress")
    public HashMap<String, String> getAddress(@RequestParam String slug) {
        PostgresSQL psql = new PostgresSQL(); 
        String sqlQuery = String.format("select address from slug where openseaSlug='%s'", slug);
        ArrayList<ArrayList<String>> result = psql.selectStatement(sqlQuery);   
        HashMap<String, String> map = new HashMap<>(); 
        if (result.size() == 0) {
            map.put(RESULT, NOT_FOUND);
        } else {
            map.put(RESULT, result.get(0).get(0));
        }
        return map;
    }
}
