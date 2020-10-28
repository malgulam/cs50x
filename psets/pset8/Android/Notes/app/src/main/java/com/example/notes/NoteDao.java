package com.example.notes;

import androidx.room.Dao;
import androidx.room.Query;

import java.util.List;

//note data access object interface
@Dao
public interface NoteDao {
    @Query("INSERT INTO notes(title, contents) VALUES ('New title','New note' )")
    void create();

    @Query("SELECT * FROM notes")
    List<Note> getAll();

    //saving new data
    @Query("UPDATE notes SET  title = :title, contents = :contents  WHERE id = :id")
    void save(String title, String contents, int id);

    //Delete note entry
    @Query("DELETE FROM notes WHERE id = :id")
    void delete(int id);
}
