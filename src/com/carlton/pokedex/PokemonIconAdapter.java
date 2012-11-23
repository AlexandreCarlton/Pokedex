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
		
		/* Set the text */
		TextView textView = (TextView) gridView.findViewById(R.id.dex_number);
		textView.setText(String.format("%03d", position+1));
		
		/* Set the image */
		ImageView imageView = (ImageView) gridView.findViewById(R.id.pokemon_icon);
		String iconName = "icon_" + Integer.toString(position + 1);
		int imageResource = context.getResources().getIdentifier(iconName, "drawable", context.getPackageName());
		imageView.setImageResource(imageResource);
		
		return gridView;
    }
	
	
	
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
