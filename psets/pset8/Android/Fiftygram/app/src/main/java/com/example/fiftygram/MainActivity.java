package com.example.fiftygram;

import androidx.annotation.RequiresApi;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.app.Activity;
import android.content.ContentResolver;
import android.content.ContentValues;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.Environment;
import android.os.ParcelFileDescriptor;
import android.provider.MediaStore;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;

import com.bumptech.glide.Glide;
import com.bumptech.glide.load.Transformation;
import com.bumptech.glide.request.RequestOptions;

import java.io.File;
import java.io.FileDescriptor;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import jp.wasabeef.glide.transformations.gpu.SepiaFilterTransformation;
import jp.wasabeef.glide.transformations.gpu.SketchFilterTransformation;
import jp.wasabeef.glide.transformations.gpu.ToonFilterTransformation;

public class MainActivity extends AppCompatActivity implements ActivityCompat.OnRequestPermissionsResultCallback {

    private ImageView imageView;

    private Bitmap original;
    private Bitmap newImage;

    private Button save_btn;

    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);

        imageView = findViewById(R.id.image_view);

        save_btn = (Button) findViewById(R.id.save_btn);
    }


    //checking result of requestPermission dialog answer from user
    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
    }


    public void apply(Transformation<Bitmap> filter){
        if (original != null){
            Glide
                    .with(this)
                    .load(original)
                    .apply(RequestOptions.bitmapTransform(filter))
                    .into(imageView);
            //set save_btn visibility to Visible
            if (save_btn.getVisibility()==View.VISIBLE){

            }else if (save_btn.getVisibility()==View.INVISIBLE){
                save_btn.setVisibility(View.VISIBLE);
            }
        }
    }

    public void applySepia(View view){
        apply (new SepiaFilterTransformation());
    }
    public void applyToon(View view){
        apply(new ToonFilterTransformation());
    }
    public void applySketch(View view){
        apply(new SketchFilterTransformation());
    }
     public void applyGrayscale(View view){
        apply(new GrayscaleTransformation());
    }
    public void applyBlur(View view){
        apply(new BlurTransformation());
    }
    public void applyMask(View view){
        apply(new MaskTransformation());
    }
    public void applySwirl(View view){
        apply(new SwirlFilterTransformation());
    }
    public void choosePhoto(View view){
        Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
        intent.setType("image/*");
        startActivityForResult(intent, 1);
    }
    @RequiresApi(api = Build.VERSION_CODES.O)
    public void savePhoto(View view) throws IOException {
        newImage = ((BitmapDrawable)imageView.getDrawable()).getBitmap();
        boolean saved;
        DateTimeFormatter dtf =  DateTimeFormatter.ofPattern("yyyyMMdd");
        LocalDate localDate = LocalDate.now();
        OutputStream fos;

        CharSequence charSequence = imageView.getContentDescription();
        final StringBuilder sb = new StringBuilder(charSequence.length());
        sb.append(charSequence);

        String name = sb.toString() + "_" + dtf.format(localDate);
        Log.d("date", name);
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q){
            ContentResolver resolver = getApplicationContext().getContentResolver();
            ContentValues contentValues = new ContentValues();
            contentValues.put(MediaStore.MediaColumns.DISPLAY_NAME, name);
            contentValues.put(MediaStore.MediaColumns.MIME_TYPE, "image/png");
            contentValues.put(MediaStore.MediaColumns.RELATIVE_PATH, "Pictures/");
            Uri imageUri = resolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues);
            fos = resolver.openOutputStream(imageUri);
        }else{
            String imagesDir = getApplicationContext().getExternalFilesDir(Environment.DIRECTORY_PICTURES).toString();
            File image = new File(imagesDir, name+".png");
            fos = new FileOutputStream(image);
        }
        saved = newImage.compress(Bitmap.CompressFormat.PNG, 100, fos);
        fos.flush();
        fos.close();
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data){
        super.onActivityResult(requestCode, resultCode, data);
        if (resultCode == Activity.RESULT_OK && data != null){
            try{
                Uri uri = data.getData();
                ParcelFileDescriptor parcelFileDescriptor =
                        getContentResolver().openFileDescriptor(uri, "r");
                FileDescriptor fileDescriptor = parcelFileDescriptor.getFileDescriptor();
                original = BitmapFactory.decodeFileDescriptor(fileDescriptor);
                parcelFileDescriptor.close();
                imageView.setImageBitmap(original);
            }catch (IOException e){
                e.printStackTrace();
            }
        }
    }
}
