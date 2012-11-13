package com.carlton.pokedex;


import android.content.Context;
import android.content.res.TypedArray;
import android.graphics.drawable.Drawable;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.GridView;
import android.widget.ImageView;
import android.widget.TextView;
/**
 * Class to display each individual Pokemon (and its National Dex Number)
 * in the Grid
 * @author Alexandre Carlton
 *
 */
public class PokemonIconAdapter extends BaseAdapter {
	
	private Context context;
	private static final int GEN_5 = 649;
	/* Using this for now; will change it for 649 later */
	private Integer[] iconIds;
	
	public PokemonIconAdapter(Context c) {
		context = c;
		
	}
	
	/* Displays item at given position */
	public View getView(int position, View convertView, ViewGroup parent) {
		View gridView;
		LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
		if (convertView == null) {
			gridView = new View(context);
			gridView = inflater.inflate(R.layout.pokemongriditem, null);
		} else {
			gridView = (View) convertView;
		}
		/* View recycling - set content of view outside of if/else */
		
		TextView textView = (TextView) gridView.findViewById(R.id.dexnumber);
		textView.setText(String.format("%03d", position+1));
		/* Set the image */
		ImageView imageView = (ImageView) gridView.findViewById(R.id.pokemonicon);
		//imageView.setImageResource(iconIds[position]);
	
	    int imageResource = context.getResources().getIdentifier("icon_" + Integer.toString(position+1), "drawable", context.getPackageName());
	    imageView.setImageResource(imageResource);
		
		return gridView;
    }
	
	
//	public Integer[] getIcons() {
//		int GEN_5 = 649;
//		Integer[] iconId = new Integer[GEN_5];
//		for (int i=0; i<GEN_5; i++){
//			iconId[i] = getResources().getIdentifier(Integer.toString(i),"drawable","com.carlton.pokedex");
//		}	
//		return iconId;
//	}
	
	
	public int getCount() {
		return GEN_5;//iconIds.length;
	}
	
	
	public Object getItem(int i) {
		return null;//iconIds[i];
	}
	
	
	public long getItemId(int arg0) {
		// TODO Auto-generated method stub
		return 0;
	}
	

}
