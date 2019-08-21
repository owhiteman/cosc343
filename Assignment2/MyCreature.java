import cosc343.assig2.Creature;
import java.util.Random;

/**
 * The MyCreate extends the cosc343 assignment 2 Creature.  Here you implement
 * creatures chromosome and the agent function that maps creature percepts to
 * actions.  
 *
 * @author  
 * @version 1.0
 * @since   2017-04-05 
 */
public class MyCreature extends Creature {

    // Random number generator
    Random rand = new Random();

    private float chromosome[] = new float[30];
    

    public int fitness = 0;

    


    /* Empty constructor - might be a good idea here to put the code that 
       initialises the chromosome to some random state   
  
       Input: numPercept - number of percepts that creature will be receiving
       numAction - number of action output vector that creature will need
       to produce on every turn
    */
    public MyCreature(int numPercepts, int numActions) {

	for(int i = 0; i < chromosome.length; i++){
	    chromosome[i] = rand.nextFloat();
	}
    }

    public MyCreature(){

    }
    
    public MyCreature(MyCreature mum, MyCreature dad){

	boolean monsters = rand.nextBoolean();
	boolean creatures = rand.nextBoolean();
	boolean food = rand.nextBoolean();

	//k-point crossover
	
	//Actions regarding monsters
	for(int i = 0; i < 9; i++){
	    if(monsters == true){
	        chromosome[i] = mum.getChromosome()[i];
	    }else{
		chromosome[i] = dad.getChromosome()[i];
	    }
	}

	//Actions regarding other creatures
	for(int j = 9; j < 18; j++){
	    if(creatures == true){
	        chromosome[j] = mum.getChromosome()[j];
	    }else{
		chromosome[j] = dad.getChromosome()[j];
	    }
	}

	//Actions regarding food
	for(int k = 18; k < 27; k++){
	    if(food == true){
	        chromosome[k] = mum.getChromosome()[k];
	    }else{
		chromosome[k] = dad.getChromosome()[k];
	    }
	}

	//Eating
	if(rand.nextBoolean() == true){
	    chromosome[27] = mum.getChromosome()[27];
	    chromosome[28] = mum.getChromosome()[28];
	}else{
	    chromosome[27] = dad.getChromosome()[27];
	    chromosome[28] = dad.getChromosome()[28];
	}

	if(rand.nextBoolean() == true){
	    chromosome[29] = mum.getChromosome()[29];
	}else{
	    chromosome[29] = dad.getChromosome()[29];
	}

	// //Single point crossover
	// int singlePoint = rand.nextInt(chromosome.length);
	// for(int i = 0; i < chromosome.length; i++){
	//     if(i < singlePoint){
	// 	chromosome[i] = mum.getChromosome()[i];
	//     }else{
	// 	chromosome[i] = dad.getChromosome()[i];
	//     }
	// }

	//Mutation
	if(rand.nextFloat() > 0.9){
	    double mutation = rand.nextGaussian();
	    mutation /= 10;
	    chromosome[rand.nextInt(chromosome.length)] += mutation;
	}

	  
    }

    public float[] getChromosome(){
	return chromosome;
    }
  
    /* This function must be overridden by the MyCreature class, because it implements
       the AgentFunction which controls creature behavoiur.  This behaviour
       should be governed by the model (that you need to come up with) that is
       parameterise by the chromosome.  
  
       Input: percepts - an array of percepts
       numPercepts - the size of the array of percepts depend on the percept
       chosen
       numExpectedAction - this number tells you what the expected size
       of the returned array of percepts should bes
       Returns: an array of actions 
    */
    @Override
    public float[] AgentFunction(int[] percepts, int numPercepts, int numExpectedActions) {
      
	// This is where your chromosome gives rise to the model that maps
	// percepts to actions.  This function governs your creature's behaviour.
	// You need to figure out what model you want to use, and how you're going
	// to encode its parameters in a chromosome.
	
	// At the moment, the actions are chosen completely at random, ignoring
	// the percepts.  You need to replace this code.
	
	float actions[] = new float[numExpectedActions];


	//Actions weights depending on percepts
	for(int i = 0; i < percepts.length; i++){
	   if(percepts[i] == 2){ //Surrounding creatures
	   	actions[8-i] = chromosome[i+9];
	   }if(percepts[i] == 3 && actions[i] < chromosome[i+18]){ //Actions for food
		actions[i] = chromosome[i+18];
	   }if(percepts[i] == 1 && actions[8-i] < chromosome[i]){ //Avoiding monsters 
		actions[8-i] = chromosome[i] ;
	    }
	}

	//Dont stay in the same place
	actions[4] = 0;

	//Action weight to eat food on square
	if(percepts[4] == 1){
	    actions[9] = chromosome[27];
	}if(percepts[4] == 2){
	    actions[9] = chromosome[28];
	}

	//Weight for a random move
	actions[10] = chromosome[29];
	
	
	return actions;
    }
  
}
