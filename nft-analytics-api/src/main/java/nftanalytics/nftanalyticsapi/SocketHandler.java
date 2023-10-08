package nftanalytics.nftanalyticsapi;

import java.util.ArrayList;


import java.io.IOException;
import java.math.BigInteger;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;

import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import com.fasterxml.jackson.databind.ObjectMapper;

import nftanalytics.nftanalyticsapi.database.PostgresSQL;

@Component
public class SocketHandler extends TextWebSocketHandler {

	@Override
	public void handleTextMessage(WebSocketSession session, TextMessage message) throws InterruptedException, IOException {
        ObjectMapper mapper = new ObjectMapper();
        TradesInput input = null;
        try {
            input = mapper.readValue(message.getPayload(), TradesInput.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
        Connection conn = new PostgresSQL().getConnection();
        // new BigInteger("100");
        while (true) {
            try {
                Statement st = conn.createStatement();
                ResultSet rs = st.executeQuery(String.format("select * from trades where address='%s' order by time_updated desc", input.address));

                ArrayList<Trade> trades = new ArrayList<>();

                while (rs.next()) {            
                    Trade trade = new Trade(rs.getString("src"), rs.getString("dst"), rs.getInt("token_id"), new BigInteger(rs.getString("price"))); 
                    trades.add(trade);
                }


                session.sendMessage(new TextMessage(mapper.writeValueAsString(trades)));

                // session.sendMessage(input);
            } catch (Exception e) { 
                e.printStackTrace();
            }

            Thread.sleep(10000);
        }
	}

    @Override
	public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        System.out.println("closed");
    }

	@Override
	public void afterConnectionEstablished(WebSocketSession session) throws Exception {
		// //the messages will be broadcasted to all users.
		// // sessions.add(session);
        System.out.println("got a connection");
	}
}
