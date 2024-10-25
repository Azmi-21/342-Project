package java_code;
import java.time.LocalDate;
import java.time.LocalTime;

public class Booking {
    private Client client;
    private Offering offering;
    private LocalDate bookingDate;
    private LocalTime startTime;
    private LocalTime endTime;

    public Booking(Client client, Offering offering, LocalDate bookingDate, LocalTime startTime, LocalTime endTime) {
        this.client = client;
        this.offering = offering;
        this.bookingDate = bookingDate;
        this.startTime = startTime;
        this.endTime = endTime;
    }

    public String toString() {
        return "Booking: " + client + " for " + offering + " on " + bookingDate;
    }
}

