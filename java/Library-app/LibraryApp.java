package LibraryApp;

import java.util.Scanner;

public class LibraryApp {

    private static final String FILE_NAME = "books.txt"; //loads booklist from this file saves to the file_nameOUT
    private static final String FILE_NAMEOUT = "books1.txt"; //to change so it edidts the original file change name to books.txt

    public static void main(String[] args) {

        Library library = new Library();
        Scanner input = new Scanner(System.in);

        int choice;

        do {
            printMenu();
            System.out.print("Enter choice: ");

            // Basic guard against non-int input
            while (!input.hasNextInt()) {
                System.out.println("Please enter a number from the menu.");
                input.nextLine();
            }
            choice = input.nextInt();
            input.nextLine(); // clear newline

            switch (choice) {
                case 1:
                    library.loadFromFile(FILE_NAME);
                    break;

                case 2:
                    library.listAllItems();
                    break;
                case 3:
                	String title;
                	String author;
                	System.out.println("Please enter the new book information");
                	
                	System.out.println("Title:");
                	title = input.nextLine();
                	
                	System.out.println("Author:");
                	author = input.nextLine();
                	
                	Book item = new Book(title, author);
                	library.addItem(item);
                	break;

                case 4:
                    library.saveToFile(FILE_NAMEOUT);
                    break;

                case 5:
                    System.out.println("Exiting LibraryApp. Goodbye!");
                    break;

                default:
                    System.out.println("Invalid option. Please choose 1-5.");
            }

            System.out.println();

        } while (choice != 5);

        input.close();
    }

    private static void printMenu() {
    	
        System.out.println("===== Library Menu =====");
        System.out.println("1. Load books from file");
        System.out.println("2. List all books");
        System.out.println("3. Add a new Book");
        System.out.println("4. Save books to file book1.txt");
        System.out.println("5. Exit");
        System.out.println("========================");
    }

    
}