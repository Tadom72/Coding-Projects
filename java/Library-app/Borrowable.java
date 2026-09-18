package LibraryApp;

public interface Borrowable {
    void borrow(String borrower);
    void giveBack();
    boolean isBorrowed();
}