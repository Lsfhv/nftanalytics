package nftanalytics.nftanalyticsapi.controllers;

public class CollectionModel {
    public String collectionName; 
    public String collectionAddress; 
    public String collectionSlug;
    
    public CollectionModel(String collectionName, String collectionAddress, String collectionSlug) {
        this.collectionName = collectionName;
        this.collectionAddress = collectionAddress;
        this.collectionSlug = collectionSlug;
    }
}
