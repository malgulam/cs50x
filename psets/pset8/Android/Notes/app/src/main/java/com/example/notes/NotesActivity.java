package com.example.notes;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class NotesActivity extends AppCompatActivity {
    private EditText editText;
    private EditText titleText;
    private Button save_btn;
    private int id;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_notes);

        Intent intent = getIntent();
        editText = findViewById(R.id.note_edit_text);
        editText.setText(intent.getStringExtra("contents"));
        titleText = findViewById(R.id.title_text);
        titleText.setText(intent.getStringExtra("title"));


    }


    public void save(View view){
        Intent intent = getIntent();
        int id = intent.getIntExtra("id", 0);
        MainActivity.database.noteDao().save(titleText.getText().toString(), editText.getText().toString(), id);
    }
    @Override
    protected void onPause() {
        super.onPause();

        Intent intent = getIntent();
        int id = intent.getIntExtra("id", 0);
        MainActivity.database.noteDao().save(titleText.getText().toString(), editText.getText().toString(), id);
    }
}