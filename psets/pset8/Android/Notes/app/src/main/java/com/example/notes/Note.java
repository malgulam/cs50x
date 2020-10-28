package com.example.notes;

//declaring database structure

import androidx.room.ColumnInfo;
import androidx.room.Entity;
import androidx.room.PrimaryKey;

@Entity(tableName = "notes")
public class Note {
    @PrimaryKey
    public int id;

    @ColumnInfo(name="title")
    public String title;

    @ColumnInfo(name="contents")
    public String contents;
}
