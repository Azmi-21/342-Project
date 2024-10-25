package java_code;
import java.util.List;

public class Instructor {
    private String name;
    private String phoneNumber;
    private String specialization;
    private List<String> availableCities;

    public Instructor(String name, String phoneNumber, String specialization, List<String> availableCities) {
        this.name = name;
        this.phoneNumber = phoneNumber;
        this.specialization = specialization;
        this.availableCities = availableCities;
    }


    //Print method that ovverides the Object class method
    public String toString() {
        return name + " (Specialized at: " + specialization + ")";
    }
}
