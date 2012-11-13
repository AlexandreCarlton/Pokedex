package com.carlton.pokedex;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;


public class PokedexActivity extends Activity {
    /** Called when the activity is first created. */
    
	@Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
        
        /*Immediately switch to grid mode, we'll change it later */
        Intent gridIntent = new Intent(PokedexActivity.this, PokedexGridActivity.class);
        startActivity(gridIntent);
    }
	
}