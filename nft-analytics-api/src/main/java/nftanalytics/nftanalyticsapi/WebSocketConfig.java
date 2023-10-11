package nftanalytics.nftanalyticsapi;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

import nftanalytics.nftanalyticsapi.tradesActivityHandler.TradesActivityHandler;
import nftanalytics.nftanalyticsapi.volumeHandler.VolumeHandler;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {
	public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
		registry.addHandler(new TradesActivityHandler(), "/trades").setAllowedOrigins("*");
		registry.addHandler(new VolumeHandler(), "/volume").setAllowedOrigins("*");
		// registry.addHandler(new AppTextWebSocketHandler(), "/ws").setAllowedOrigins("*");
	}
}
