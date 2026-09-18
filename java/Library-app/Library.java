package LibraryApp;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.Scanner;

import week10.Student;

public class Library {

    private ArrayList<LibraryItem> items = new ArrayList<>();

    public void addItem(LibraryItem item) {
        items.add(item);
    }

    public void listAllItems() {
        if (items.isEmpty()) {
            System.out.println("No items in the library.");
            return;
        }
        for (LibraryItem item : items) {
            System.out.println(item);
        }
    }

    public ArrayList<LibraryItem> getItems() {
        return items;
    }

    public void loadFromFile(String fileName) {
    	int counter = 0;
        File file = new File(fileName);

        try (Scanner sc = new Scanner(file)) {

            while (sc.hasNextLine()) {
                String line = sc.nextLine().trim();    // e.g. ",21,Computer Science"
                if (line.isEmpty()) {
                    continue; // skip blank lines
                }

                String[] parts = line.split(";");

                // simple defensive check
                if (parts.length == 2) {
                    String title   = parts[0].trim();
                    String author = parts[1].trim();

                    items.add(new Book(title, author));
                } else {
                    System.out.println("Skipping malformed line: " + line);
                }
            }

        } catch (FileNotFoundException e) {
            System.out.println("Could not find file: " + fileName + " (" + e.getMessage() + ")");
        }
        
        for(LibraryItem item: items) {
        	counter++;
        }
        System.out.println("Succesfully loaded " + counter + " Items");

    }
    
    public void saveToFile(String fileName) {
        try (PrintWriter out = new PrintWriter(new FileWriter(fileName))) {

            for (LibraryItem b : items) {
                out.println(b.toDataString());
            }

            System.out.println("File overwritten successfully.");

        } catch (IOException e) {
            System.out.println("Error writing file: " + e.getMessage());
        }
    }
    
}

