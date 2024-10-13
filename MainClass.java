import java.time.LocalDate;
import java.time.LocalTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class MainClass {
    public static void main(String[] args) {
      
        Location evBuilding = new Location("EV-Building", "Montreal", "1515 Saint-Catherine St W #1428");
        Location aquaticCenter = new Location("Aquatic Center", "Laval", "2205 Ave Terry-Fox.");

        // To see the object
        System.out.println("===============Locations================\n");
        System.out.println(evBuilding);
        System.out.println(aquaticCenter);

       
        Instructor alimurat = new Instructor("Alimurat", "514-123-4567", "Ping-Pong", Arrays.asList("Montreal", "Brossard"));
        Instructor azmi = new Instructor("Azmi", "438-123-4567", "Football", Arrays.asList("Montreal","Laval"));

        System.out.println("================Intructors================\n");
        System.out.println(alimurat);
        System.out.println(azmi);
 

        Offering pingpongOffering = new Offering("Private", aquaticCenter, LocalDate.of(2024, 10, 13), LocalDate.of(2024, 12, 15), LocalTime.of(14, 0), LocalTime.of(16, 0), alimurat);
        Offering soccerOffering = new Offering("Group", evBuilding, LocalDate.of(2024, 10, 13), LocalDate.of(2024, 12, 15), LocalTime.of(14, 0), LocalTime.of(16, 0),azmi);

        System.out.println("================Offerings================\n");
        System.out.println(alimurat);
        System.out.println(azmi);

        
        Client ronaldo = new Client("Cristiano Ronaldo", false, null);
        Client messi = new Client("Lionel Messi", true, ronaldo);

        System.out.println("================Clients================\n");
        System.out.println(ronaldo);
        System.out.println(messi);
        
        System.out.println("================Bookings================\n");
        //TODO

    }
}
