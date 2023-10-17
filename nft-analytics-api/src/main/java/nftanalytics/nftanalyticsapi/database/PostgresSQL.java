package nftanalytics.nftanalyticsapi.database;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class PostgresSQL {

    private final String url = "jdbc:postgresql://127.0.0.1:5432/nftanalytics";
    private final String user = "postgres";
    private final String password = "x";

    private Connection conn = null;

    public PostgresSQL() {
        conn = connect();
    }

    private Connection connect() {
        Connection conn = null;
        try {
            conn = DriverManager.getConnection(url, user, password);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        return conn;
    }

    public Connection getConnection() {
        return conn;
    }
}
