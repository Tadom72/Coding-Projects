package LibraryApp;

public abstract class LibraryItem {

    // Static counter shared by ALL library items
    private static int nextId = 1;

    private int id;
    protected String title;

    public LibraryItem(String title) {
        this.id = nextId++;   // assign current ID, then increment for next item
        this.title = title;
    }

    public int getId() {
        return id;
    }

    public String getTitle() {
        return title;
    }

    // Each subclass (e.g., Book) provides its own data format for saving
    public abstract String toDataString();


}