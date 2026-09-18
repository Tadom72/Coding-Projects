import java.io.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.LinkedList;

enum C {White, Grey, Black};


public class BfDfPrim 
{
    // V = number of vertices
    // E = number of edges

    //test
    // adj[ ][ ] is the adjacency matrix

    private List<List<Integer>> adj;
    private int[][] weights;
    private int V, E;
    //private int[][] adj;

    // used for traversing graph to mark vertices already visited
    private C[] colour;
    private int time;
    
    // for storing the traversal tree and ditance from starting vertex
    private int[] parent, d, f ;
    

    // adjacency list constructor
    public BfDfPrim(String graphFile) throws IOException {
        int u, v;
        int e;
        int w;

        FileReader fr = new FileReader(graphFile);
		BufferedReader reader = new BufferedReader(fr);	
    
        String splits = " +";  // multiple whitespace as delimiter
		String line = reader.readLine();        
        String[] parts = line.split(splits);
        System.out.println( "Vertices: " + parts[0] + " Edges: " + parts[1]);
		    
		V = Integer.parseInt(parts[0]);
        E = Integer.parseInt(parts[1]);

        // create adjacency List, initialised to 0's
        this.adj = new ArrayList<>();
        for(int i = 0; i <= V; i++) {
            this.adj.add(new ArrayList<Integer>());
        }
        this.weights = new int[V+1][V+1];
        colour = new C[V+1];
        parent = new int[V+1];
        d = new int[V+1];
        f = new int[V+1];

        // read the edges
        System.out.println("Reading edges from text file");
        for(e = 1; e <= E; ++e)
        {
            line = reader.readLine();
            parts = line.split(splits);
            u = Integer.parseInt(parts[0]);
            v = Integer.parseInt(parts[1]); 
            w = Integer.parseInt(parts[2]);
            
            System.out.println("Edge " + toChar(u) + "->" + toChar(v) + " with weight " + w);
            
            this.adj.get(u).add(v);
            //weight arrary to store the weight of edges so it can easily be displayed
            this.weights[u][v] = w;
            //Line needed as graph is undirected so edge can be traversed both ways
            this.adj.get(v).add(u);
            this.weights[v][u] = w;

            
            
        }
        reader.close();

    }

	// convert vertex into char for pretty printing
    private char toChar(int u)
    {  
		//Changed to 84 to display from U
        return (char)(u + 64);
    }
	
    // method to display the graph representation
    public void display() {
       for (int i = 1; i < adj.size(); i++) {
            System.out.print("\n" + i + ": ");

            for (int j : adj.get(i)) {
                System.out.print(j + "(" + weights[i][j] + ") ");
            }
        }
    }

    public void charDisplay() {
       for (int i = 1; i < adj.size(); i++) {
            System.out.print("\n" + toChar(i) + ": ");

            for (int j : adj.get(i)) {
                System.out.print(toChar(j) + "(" + weights[i][j] + ") ");
            }
        }
    }


    // method to initialise Depth First Traversal of Graph
    // Assuming graph is connected
    public void DF( int s) 
    {     
        int v;
        for(v=1; v<=V; ++v) {
            colour[v] = C.White;
            parent[v] = 0;        
        }
        
        System.out.print("\nDepth First Graph Traversal\n");
        System.out.println("Starting with Vertex " + toChar(s));
        
        time = 0;
        dfVisit(s);

		//Check for any verices still undiscorved after the intial depth search
		//Added this as w and z where never being discovered 
		for(v=1; v<=V; ++v) {
			if(colour[v] == C.White){
				dfVisit(v);
			}
		}
        
        System.out.print("\n\n");
    }


    // Recursive Depth First Traversal for adjacency matrix
    private void dfVisit( int v)
    {
        int u;
        ++time;
        d[v] = time;
        colour[v] = C.Grey;
        
        System.out.print("\n  DF just visited vertex " + toChar(v) + " along edge " + 
            toChar(parent[v]) + "--" + toChar(v) );
        
        // process all the vertices u connected to vertex v
       // lots of missing code
	   for(u = 1 ; u <= V; u++){
		   //Added check that the adj of the coloumn isnt 0
		   //So that the edges are seen as directional they cant go from 2->1 for example
		   //If chosing to display graph by row instead of coloum (line 58) switch the adj[v][u] to adj[u][v] 
		   if ( adj.get(v).contains(u) && colour[u] == C.White){
			   parent[u] = v;
			   dfVisit(u);
		   }
	   }
	   //for asigning when a verices is finished i.e all branches are discovered
	   colour[v] = C.Black;
	   ++time;
	   f[v] = time;
    }
    
    public void BF(int s) {
        //lots of missing code
        Queue<Integer> q = new LinkedList<>();
        int time = 0;
        int v = 1;
        for( v = 1; v <= V; v++) {
            colour[v] = C.White;
            parent[v] = 0;
        }

        q.offer(s);
        while (!q.isEmpty()) {
            v = q.poll();
            if(colour[v] == C.White){
                colour[v] = C.Grey;
                time++;
                d[v] = time;
                System.out.print("\n  BF just visited vertex " + toChar(v) + " along edge " + 
                    toChar(parent[v]) + "--" + toChar(v) );
                for (int u : adj.get(v)) {
                    if (colour[u] == C.White) {
                        parent[u] = v;
                        q.offer(u);
                    }
                }
                colour[v] = C.Black;
                time++;
                f[v] = time;
            }
        }
        System.out.println("\n");
    }
	
	//Function for displaying when a verices was discovered and finshed 
	public void finished() {
		int v;
		for(v = 1; v <= V; v++){
			System.out.print("\n" + toChar(v) + " Was Discovered at: " + d[v] + " And was finished at: " + f[v]);
		}
        System.out.println("\n");
	}

    public static void main(String[] args) throws IOException
    {
        //gets sting name of graph file from user input
        String fname;
        System.out.print("Enter the name of the graph file: ");
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        fname = br.readLine();
        if (fname.contains(".txt") == false) {
            fname = fname + ".txt";
        }

        //gets the starting vertex for the traversal from user input
        int s;
        System.out.print("Enter the starting vertex (as a number): ");
        s = Integer.parseInt(br.readLine());


        //GraphMatrixDir g = new GraphMatrixDir(fname);
        BfDfPrim g = new BfDfPrim(fname);
       
        //regular display using vertices numbers
        //g.display();

        //Adjencency list display using the vertices letters rather than numbers
		g.charDisplay();

		//user selects which traversal they want to see
        System.out.print("Enter '1' for Depth First Traversal or '2' for Breadth First Traversal: ");
        int choice = Integer.parseInt(br.readLine());
        if (choice == 1) {
            g.DF(s);
            g.finished();
        } else if (choice == 2) {
            g.BF(s);
            g.finished();
        } else {
            System.out.println("Invalid choice. Please enter '1' or '2'.");
            return;
        }
		//g.DF(s);
		
		//Personally made function feel free to remove if unnecassary 
		//g.finished();
        

        g.BF(s);

        g.finished();
        
    }

}

