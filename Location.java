public class Location {
    private String name;
    private String city;
    private String address;

    public Location(String name, String city, String address) {
        this.name = name;
        this.city = city;
        this.address = address;
    }
    //Print method that overides the Object class method

    public String toString() {
        return name + " in " + city;
    }
}
