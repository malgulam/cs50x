package com.example.notes;

import android.content.Context;
import android.content.Intent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.recyclerview.widget.RecyclerView;

import java.net.CookieHandler;
import java.util.ArrayList;
import java.util.List;

public class NotesAdapter extends RecyclerView.Adapter<NotesAdapter.NoteViewHolder> {


    public static class NoteViewHolder extends RecyclerView.ViewHolder {
        public LinearLayout containerView;
        public TextView nameTextView;
        public Button deleteBtn;

        public NoteViewHolder(View view) {
            super(view);
            this.containerView = view.findViewById(R.id.note_row);
            this.nameTextView = view.findViewById(R.id.note_row_name);


            this.containerView.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Context context = v.getContext();
                    Note note = (Note) containerView.getTag();
                    Intent intent = new Intent(v.getContext(), NotesActivity.class);
                    intent.putExtra("id", note.id);
                    intent.putExtra("title", note.title);
                    intent.putExtra("contents", note.contents);
                    context.startActivity(intent);
                }
            });
//            deleteBtn = view.findViewById(R.id.delete_btn);
//            deleteBtn.setOnClickListener(new View.OnClickListener() {
//                @Override
//                public void onClick(View v) {
//                    Context context = v.getContext();
//                    Note note = (Note) v.getTag();
//                    MainActivity.database.noteDao().delete(note.id);
//
//                }
//            });

        }
    }
    //    public void delete(View view){
//        Context context = view.getContext();
//        Note note = (Note) view.getTag();
//       MainActivity.database.noteDao().delete(note.id);
//        notifyDataSetChanged();
//    }
    public List<Note> notes = new ArrayList<>();

    @Override
    public NoteViewHolder onCreateViewHolder(ViewGroup parent, int viewType){
        View view = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.note_row, parent, false);
        return new NoteViewHolder(view);
    }

    @Override
    public void onBindViewHolder(NoteViewHolder holder, int position){
        Note current = notes.get(position);
        holder.containerView.setTag(current);
        holder.nameTextView.setText(current.title);
    }
    @Override
    public int getItemCount(){return notes.size();}

    public void reload(){
        notes = MainActivity.database.noteDao().getAll();
        notifyDataSetChanged();
    }
    public void removeItem(int id, int position) {
        notes.remove(position);
        MainActivity.database.noteDao().delete(id);
        notifyItemRemoved(position);
    }

    public void restoreItem(Note note, int position) {
        notes.add(position, note);
        MainActivity.database.noteDao().save(note.title, note.contents, note.id);
        notifyItemInserted(position);
    }
}

