package nftanalytics.nftanalyticsapi.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;

public class PostgresSQL {

    private final String url = "jdbc:sqlite:../analytics/test.db"; 
    private Connection conn;

    public PostgresSQL() {
        conn = connect();
    }

    private Connection connect() {
        try {
            conn = DriverManager.getConnection(url);
        } catch (SQLException e) {
            System.out.println("got here");
            System.out.println(e.getMessage());
        }
        return conn;
    }

    public Connection getConnection() {
        return conn;
    }

    public ArrayList<ArrayList<String>> selectStatement(String sqlQuery) {
        ArrayList<ArrayList<String>> result = new ArrayList<>();
        
        try {
            ResultSet rs = conn.createStatement().executeQuery(sqlQuery); 
            int columnCount = rs.getMetaData().getColumnCount(); 
            while (rs.next()) {
                ArrayList<String> row = new ArrayList<>();
                for (int i = 1; i <= columnCount; i++) {
                    row.add(rs.getString(i));
                }
                result.add(row); 
            }
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
        return result;
    }

    public static void main(String[] args) {
        PostgresSQL psql = new PostgresSQL();
        psql.selectStatement("SELECT * FROM trades");
        
    }
}
