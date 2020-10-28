package com.example.notes;

import androidx.room.Database;
import androidx.room.RoomDatabase;

@Database(entities = {Note.class}, version=1)
//abstract class can let you create a class with methods with and without bodies(eg interfaces and actual classes)
public abstract class NoteDatabase extends RoomDatabase {
    public abstract NoteDao noteDao();
}
