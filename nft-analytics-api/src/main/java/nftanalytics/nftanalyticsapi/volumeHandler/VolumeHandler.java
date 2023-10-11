package nftanalytics.nftanalyticsapi.volumeHandler;

import java.io.IOException;

import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class VolumeHandler extends TextWebSocketHandler {
    @Override
    public void handleTextMessage(WebSocketSession session, TextMessage message) throws InterruptedException, IOException {
        ObjectMapper mapper = new ObjectMapper();
        VolumeInput input = null;
        try {
            input = mapper.readValue(message.getPayload(), VolumeInput.class);
        } catch (Exception e) {
            e.printStackTrace();
        }
        
        for (long timePeriod: input.timePeriods) {
            computeVolumeThread thread = new computeVolumeThread(session, input.address, timePeriod);
            thread.start();
        }

    }

    @Override
	public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        session.close();
    }

	@Override
	public void afterConnectionEstablished(WebSocketSession session) throws Exception {

    }
}
