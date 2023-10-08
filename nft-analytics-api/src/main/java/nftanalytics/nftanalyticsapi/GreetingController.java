package nftanalytics.nftanalyticsapi;

import org.springframework.messaging.handler.annotation.MessageMapping;
import org.springframework.messaging.handler.annotation.SendTo;
import org.springframework.stereotype.Controller;
import org.springframework.web.util.HtmlUtils;

@Controller
public class GreetingController {


    @MessageMapping("/hello")
    @SendTo("/topic/greetings")
    public Greeting greeting(HelloMessage message) throws Exception {

      System.out.println("got here");

      Thread.sleep(1000); // simulated delay
      return new Greeting("Hello, " + HtmlUtils.htmlEscape(message.getName()) + "!");
    }

    @MessageMapping("/trades")
    @SendTo("/topic/greetings")
    public Greeting trades(HelloMessage message) throws Exception {

      System.out.println("got here bope");

      // Thread.sleep(1000); // simulated delay
      return new Greeting("Baka, " + HtmlUtils.htmlEscape(message.getName()) + "!");
    }

}