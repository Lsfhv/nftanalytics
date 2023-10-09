package nftanalytics.nftanalyticsapi.volumeHandler;

import java.math.BigInteger;

public class VolumeOutput {
    public long timePeriod; 
    public BigInteger volume;

    public VolumeOutput(BigInteger volume, long timePeriod) {
        this.volume = volume;
        this.timePeriod = timePeriod;
    }
}
