package nftanalytics.nftanalyticsapi.tradesActivityHandler;

import java.math.BigInteger;
import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.ArrayList;

import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import com.fasterxml.jackson.databind.ObjectMapper;

import nftanalytics.nftanalyticsapi.database.PostgresSQL;

public class TradesThread  extends Thread {

    private WebSocketSession session; 
    private String address; 

    public TradesThread(WebSocketSession session, String address) {
        this.session = session;
        this.address = address;
    }

    public void run() {
        ObjectMapper mapper = new ObjectMapper();
        Connection conn = new PostgresSQL().getConnection();
        while (true) {
            try {
                Statement st = conn.createStatement();
                ResultSet rs = st.executeQuery(String.format("select * from trades where address='%s' order by time_updated desc", address));

                ArrayList<Trade> trades = new ArrayList<>();

                while (rs.next()) {            
                    Trade trade = new Trade(rs.getString("tx_hash"),rs.getString("src"), rs.getString("dst"), rs.getInt("token_id"), new BigInteger(rs.getString("price"))); 
                    trades.add(trade);
                }

                if (!session.isOpen()) {
                    break;
                }

                session.sendMessage(new TextMessage(mapper.writeValueAsString(trades)));
            } catch (Exception e) { 
                e.printStackTrace();
            }
            try {
                Thread.sleep(1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
    
}
