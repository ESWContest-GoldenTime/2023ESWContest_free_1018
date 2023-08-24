package com.example.golden_time1

import android.annotation.SuppressLint
import android.net.Uri
import android.os.Bundle
import android.provider.MediaStore.Audio.Media
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.databinding.DataBindingUtil
import androidx.media3.common.MediaItem
import androidx.media3.common.Player
import androidx.media3.common.util.Util
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import com.google.firebase.ktx.Firebase
import com.google.firebase.storage.ktx.storage
import android.util.Log


class StoredVideoPage : ComponentActivity(), Player.Listener {
    private lateinit var player: ExoPlayer
    private lateinit var playerView: PlayerView

    private var playWhenReady = true
    private var currentWindow = 0
    private var playbackPosition = 0L
    private val TAG = "FirebaseService"

    val FirebaseStorage = Firebase.storage
    val storageReference = FirebaseStorage.reference
    val videoReference = storageReference.child("videos/example_song.mp4")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_stored_video_page)

        videoReference.downloadUrl.addOnSuccessListener { uri ->
            setupPlayer(uri)
            Log.d(TAG, "ok, downloaded")
        }.addOnFailureListener {
            Log.d(TAG, "error_ no download!")
        }

    }

    private fun setupPlayer(uri: Uri){
        player = ExoPlayer.Builder(this).build()
        playerView = findViewById(R.id.playerView2)
        playerView.player = player

        val mediaItem = MediaItem.fromUri(uri)
        player.setMediaItem(mediaItem)
        player.prepare()
        player.playWhenReady = true
    }
}