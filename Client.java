public class Client {
    private String name;
    private boolean isUnderage;
    private Client guardian;

    public Client(String name, boolean isUnderage, Client guardian) {
        this.name = name;
        this.isUnderage = isUnderage;
        this.guardian = guardian;
    }

    public boolean hasGuardian() {
        return isUnderage && guardian != null;
    }

    public String getName() {
        return name;
    }

    public boolean isUnderage() {
        return isUnderage;
    }

    public String toString() {
        return name + (isUnderage ? " (Underage, Guardian: " + guardian.getName() + ")" : "");
    }
}
