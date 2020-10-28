package com.example.pokedex;

import androidx.appcompat.app.AppCompatActivity;

import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.net.URL;

public class PokemonActivity extends AppCompatActivity {

    private SharedPreferences sharedPreferences;
    private SharedPreferences.Editor editor;

    private TextView nameTextView;
    private TextView numberTextView;
    private TextView type1textview;
    private TextView type2textview;
    private TextView descriptionTextView;

    private String name;
    private String url;

    private boolean captured;

    private Button button;

    private RequestQueue requestQueue;

    private ImageView spriteImageView;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_pokemon);

        sharedPreferences = getApplicationContext().getSharedPreferences("captured_pokemon", 0);
        editor = sharedPreferences.edit();

        //getting intent
        requestQueue = Volley.newRequestQueue(getApplicationContext());

        url = getIntent().getStringExtra("url");
//        int number = getIntent().getIntExtra("number", 0);

        nameTextView = findViewById(R.id.pokemon_name);
        numberTextView = findViewById(R.id.pokemon_number);
        type1textview = findViewById(R.id.pokemon_type1);
        type2textview = findViewById(R.id.pokemon_type2);
        descriptionTextView= findViewById(R.id.pokemon_description);

        button = findViewById(R.id.catch_button);

        spriteImageView = findViewById(R.id.pokemon_sprite);
        load();

//        nameTextView.setText(name);
////        numberTextView.setText(Integer.toString(number));
//        numberTextView.setText(String.format("#%03d", number));
    }
    public void load(){
        type1textview.setText(" ");
        type2textview.setText(" ");
        captured = sharedPreferences.getBoolean(name, false);
        if (captured){
            catchPokemon();
        }
        else{
            button.setText(R.string.catch_text);
            releasePokemon();
        }
        JsonObjectRequest request = new JsonObjectRequest(Request.Method.GET, url, null, new Response.Listener<JSONObject>() {
            @Override
            public void onResponse(JSONObject response) {
                try {
                    nameTextView.setText(name);
                    numberTextView.setText(String.format("#%03d", response.getInt("id")));

                    JSONArray typeEntries = response.getJSONArray("types");
                    for (int i = 0; i < typeEntries.length(); i++) {
                        JSONObject typeEntry = typeEntries.getJSONObject(i);
                        int slot = typeEntry.getInt("slot");
                        String type = typeEntry.getJSONObject("type").getString("name");

                        if (slot == 1) {
                            type1textview.setText(type);
                        }
                        else if (slot == 2) {
                            type2textview.setText(type);
                        }
                    }

                    JSONObject species = response.getJSONObject("species");
                    String speciesUrl = species.getString("url");
                    JsonObjectRequest request_species = new JsonObjectRequest(Request.Method.GET, speciesUrl, null, new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                JSONArray descriptionEntries = response.getJSONArray("flavor_text_entries");
                                String description = descriptionEntries.getJSONObject(0).getString("flavor_text");
                                descriptionTextView.setText(description);
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }
                        }
                    }, new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            Log.e("cs50", "Pokemon description error", error);
                        }
                    });

                    requestQueue.add(request_species);

                    JSONObject sprites = response.getJSONObject("sprites");
                    String spriteUrl = sprites.getString("front_default");
                    new DownloadSpriteTask().execute(spriteUrl);

                } catch (JSONException e) {
                    Log.e("cs50", "Pokemon json error", e);
                }
            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Log.e("cs50", "Pokemon details error", error);
            }
        });

        requestQueue.add(request);
    }

    public void toggleCatch(View view){
        //gotta catch 'em all
        if (captured){
            releasePokemon();
        }
        else{
            catchPokemon();
        }
    }
    public void catchPokemon(){
        button.setText(R.string.release_text);
        captured = true;

        editor.putBoolean(name, true);
        editor.commit();
    }
    public void releasePokemon(){
        button.setText(R.string.catch_text);
        captured = false;

        editor.remove(name);
        editor.commit();
    }
    private class DownloadSpriteTask extends AsyncTask<String, Void, Bitmap> {
        @Override
        protected Bitmap doInBackground(String ... strings){
            try {
                URL url = new URL(strings[0]);
                return BitmapFactory.decodeStream(url.openStream());
            }
            catch(IOException e ){
                Log.e("cs5-", "Download sprite error", e);
                return null;
            }
        }
        @Override
        protected void onPostExecute(Bitmap bitmap){
            spriteImageView.setImageBitmap(bitmap);
        }
    }


}