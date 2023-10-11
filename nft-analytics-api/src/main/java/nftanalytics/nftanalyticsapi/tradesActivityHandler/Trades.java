package nftanalytics.nftanalyticsapi.tradesActivityHandler;

import java.util.ArrayList;

public class Trades {
    public ArrayList<Trade> trades;

    public Trades() {
        
    }
    
    public String toString() {
        return "[" + trades.size() + "]";
    }
}
