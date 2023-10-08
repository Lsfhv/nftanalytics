package nftanalytics.nftanalyticsapi;

import java.math.BigInteger;

public class Trade {
    public String src;
    public String dst;
    public int token_id;
    public BigInteger value;

    public Trade(String src, String dst, int token_id, BigInteger value) {
        this.src = src;
        this.dst = dst;
        this.token_id = token_id;
        this.value = value;
    }

    public Trade() {}
}
