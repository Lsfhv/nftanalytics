package nftanalytics.nftanalyticsapi.tradesActivityHandler;



import java.io.IOException;


import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class TradesActivityHandler extends TextWebSocketHandler {

	@Override
	public void handleTextMessage(WebSocketSession session, TextMessage message) throws InterruptedException, IOException {
        ObjectMapper mapper = new ObjectMapper();
        TradesInput input = null;
    
        try {
            input = mapper.readValue(message.getPayload(), TradesInput.class);
        } catch (Exception e) {
            e.printStackTrace();
        }

        TradesThread t = new TradesThread(session, input.address);
        t.start();
	}

    @Override
	public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        session.close();
    }

	@Override
	public void afterConnectionEstablished(WebSocketSession session) throws Exception {

	}
}
