package nftanalytics.nftanalyticsapi;

import java.util.HashMap;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import nftanalytics.nftanalyticsapi.database.PostgresSQL;

@CrossOrigin
@RestController
public class GetAddressController {
    
    @RequestMapping("/getaddress")
    public HashMap<String, String> getAddress(@RequestParam String slug) {

        Connection conn = new PostgresSQL().getConnection();

        HashMap<String, String> map = new HashMap<>();

        String sqlQuery = String.format("select * from slug where opensea='%s'", slug);
        String result = "";

        try {
            Statement st = conn.createStatement();
            ResultSet rs = st.executeQuery(sqlQuery);
            while (rs.next()) {
                result = rs.getString("address");
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        map.put("address", result);

        return map;
    }

}
