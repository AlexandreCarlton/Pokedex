package com.carlton.pokedex;

import android.app.Activity;
import android.os.Bundle;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.AdapterView;
import android.widget.GridView;
import android.widget.AdapterView.OnItemClickListener;

public class PokedexGridActivity extends Activity {
	/** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
    	/* Remove Title and Notification bars */
    	//can use android:theme="@android:style/Theme.Black.NoTitleBar" in Application tab as well.
    	this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        this.requestWindowFeature(Window.FEATURE_NO_TITLE);
    	     
        super.onCreate(savedInstanceState);
        setContentView(R.layout.pokemongridlayout);
   
        GridView gridview = (GridView) findViewById(R.id.pokedex_grid);
        gridview.setAdapter(new PokemonIconAdapter(this));
   
        gridview.setOnItemClickListener(new OnItemClickListener() {
        	public void onItemClick(AdapterView<?> parent, View v, int position, long id) {
        		/* Makes a toast indication the position of the item clicked
        		 * So we should make an Intent to go to the pokemon at position+1
        		 */
        		//Toast.makeText(PokedexGridActivity.this, "" + position, Toast.LENGTH_SHORT).show();
        	}
        });
    }
}
