package java_code;
import java.time.LocalDate;
import java.time.LocalTime;

public class Offering {
    private String type; 
    private Location location;
    private LocalDate startDate; //to be used in implementations
    private LocalDate endDate;   //to be used in implementations
    private LocalTime startTime;
    private LocalTime endTime;
    private Instructor instructor;

    public Offering(String type, Location location, LocalDate startDate, LocalDate endDate, LocalTime startTime, LocalTime endTime, Instructor instructor) {
        this.type = type;
        this.location = location;
        this.startDate = startDate;
        this.endDate = endDate;
        this.startTime = startTime;
        this.endTime = endTime;
        this.instructor = instructor;
    }

    public String toString() {
        return type + " class at " + location + " from " + startTime + " to " + endTime + ", Instructor: " + instructor;
    }
}
