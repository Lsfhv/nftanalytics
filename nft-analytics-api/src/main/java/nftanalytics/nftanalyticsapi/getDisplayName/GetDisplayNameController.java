package nftanalytics.nftanalyticsapi.getDisplayName;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;

import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import nftanalytics.nftanalyticsapi.database.PostgresSQL;

@CrossOrigin
@RestController
public class GetDisplayNameController {
    @RequestMapping("/getdisplayname")
    public HashMap<String, String> getDisplayName(@RequestParam String slug) {
        HashMap<String, String> map = new HashMap<>();
        Connection conn = new PostgresSQL().getConnection();

        String sqlQuery = String.format("select * from slug where opensea='%s'", slug);
        String result = "error";

        try {
            Statement st = conn.createStatement();
            ResultSet rs = st.executeQuery(sqlQuery);
            while (rs.next()) {
                result = rs.getString("display_name");
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        map.put("display_name", result);

        return map;
    }
}
