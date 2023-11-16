package nftanalytics.nftanalyticsapi.controllers;

import java.util.HashMap;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import nftanalytics.nftanalyticsapi.database.PostgresSQL;

@CrossOrigin
@RestController
public class GetDisplayNameController extends Controller {
    @RequestMapping("/getdisplayname")
    public HashMap<String, String> getDisplayName(@RequestParam String slug) {
        HashMap<String, String> map = new HashMap<>();
        PostgresSQL psql = new PostgresSQL();
        String sqlQuery = String.format("select name from slug where openseaSlug='%s'", slug);
        String result = psql.selectStatement(sqlQuery).get(0).get(0);
        map.put(RESULT, result);
        return map;
    }
}
