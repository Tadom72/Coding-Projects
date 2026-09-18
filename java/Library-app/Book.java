package LibraryApp;

public class Book extends LibraryItem implements Borrowable {

    private String author;
    private boolean borrowed = false;
    private String borrowerName = "";

    public Book(String title, String author) {
        super(title);
        this.author = author;
    }

    public String getAuthor() {
        return author;
    }

    @Override
    public void borrow(String borrower) {
        if (!borrowed) {
            borrowed = true;
            borrowerName = borrower;
            System.out.println("\"" + getTitle() + "\" borrowed by " + borrowerName);
        } else {
            System.out.println("\"" + getTitle() + "\" is already borrowed by " + borrowerName);
        }
    }

    @Override
    public void giveBack() {
        if (borrowed) {
            System.out.println("\"" + getTitle() + "\" returned by " + borrowerName);
            borrowed = false;
            borrowerName = "";
        } else {
            System.out.println("\"" + getTitle() + "\" is not currently borrowed.");
        }
    }

    @Override
    public boolean isBorrowed() {
        return borrowed;
    }

    @Override
    public String toString() {
        String status = borrowed ? "Borrowed by " + borrowerName : "Available";
        return "Book[" + getId() + "] " + getTitle() + " by " + author + " (" + status + ")";
    }

    @Override
    public String toDataString() {
        return String.format("%-40s; %s", getTitle(), author);
    }
}