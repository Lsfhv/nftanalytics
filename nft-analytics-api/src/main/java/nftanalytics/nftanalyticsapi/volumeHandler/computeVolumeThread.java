package nftanalytics.nftanalyticsapi.volumeHandler;

import java.sql.Statement;
import java.math.BigInteger;
import java.sql.Connection;
import java.sql.ResultSet;
import java.time.Instant;

import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import com.fasterxml.jackson.databind.ObjectMapper;

import nftanalytics.nftanalyticsapi.database.PostgresSQL;

public class computeVolumeThread extends Thread {

    WebSocketSession session ; 
    String address; 
    long timePeriod;
    Connection conn; 

    public computeVolumeThread(WebSocketSession session, String address, long timePeriod)  {
        this.session = session;
        this.address = address; 
        this.timePeriod = timePeriod;

        conn = new PostgresSQL().getConnection();
    }

    public long getEpochTime() {
        return (Instant.now().toEpochMilli() / 1000);
    }

    public void run() {
        ObjectMapper mapper = new ObjectMapper();
        while (true) {
            long currentTime = getEpochTime() ;
            // long volume = 0;
            
            BigInteger volume = new BigInteger("0");
            try {
                
                Statement st = conn.createStatement();

                                
                ResultSet rs = st.executeQuery(String.format("select * from trades where address='%s' and cast(extract(epoch from time_updated) as bigint) >= %d", address, currentTime - timePeriod));
                while (rs.next()) {
                    volume = volume.add(new BigInteger(rs.getString("price")));
                }

                VolumeOutput vo = new VolumeOutput(volume, timePeriod);
                session.sendMessage(new TextMessage(mapper.writeValueAsString(vo)));

            } catch (Exception e) {
                e.printStackTrace();
            }

            try {
                Thread.sleep(timePeriod * 1000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }

        }
    }
}
