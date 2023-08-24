package com.example.golden_time1

import android.content.Intent
import androidx.activity.ComponentActivity
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import com.google.firebase.FirebaseApp


class MainActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val button1 = findViewById<Button>(R.id.button4)
        button1.setOnClickListener {
            Toast.makeText(this, "Streaming Service", Toast.LENGTH_LONG).show()

            val intent = Intent(this, LiveStreamPage::class.java)
            startActivity(intent)
        }

        val button2 = findViewById<Button>(R.id.button5)
        button2.setOnClickListener {
            Toast.makeText(this, "Streaming Service", Toast.LENGTH_LONG).show()

            val intent = Intent(this, StoredVideoPage::class.java)
            startActivity(intent)
        }

    }
}