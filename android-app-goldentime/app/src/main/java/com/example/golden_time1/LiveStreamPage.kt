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

import com.example.golden_time1.theme.Rtsp_testTheme

class LiveStreamPage : ComponentActivity(), Player.Listener {
    private lateinit var player: ExoPlayer
    private lateinit var playerView: PlayerView

//    private var videoUri = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
//    private var videoUri = "rtsp://pi:asd12@192.168.10.56:8555/unicast"
//    private var videoUri = "rtsp://pi:asd12@rlaehdqja98.iptime.org:17854/unicast"

    private var videoUri = "rtsp://192.168.200.117:8555/unicast"

//    private var videoUri = "rtsp://192.168.10.56:8555/unicast"

    private var playWhenReady = true
    private var currentWindow = 0
    private var playbackPosition = 0L

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContentView(R.layout.activity_livestream)

//        setupPlayer() //이건 샘플 동영상
        addMp4Files()   //이건 우리 라이브 rtsp 통신용

//        initializePlayer()


    }

    private fun setupPlayer(){
        player = ExoPlayer.Builder(this).build()
        playerView = findViewById(R.id.playerView1)
        playerView.player = player
        player.addListener(this)
    }

    private fun addMp4Files(){
        player = ExoPlayer.Builder(this).build()
        playerView = findViewById(R.id.playerView1)
        playerView.player = player
        player.addListener(this)
        val mediaItem = MediaItem.fromUri(Uri.parse(videoUri))
        player.addMediaItem(mediaItem)
        player.prepare()
        player.play()
    }

//    public override fun onStart() {
//        super.onStart()
//
//        initializePlayer()
//
//    }
//
//
//    public override fun onResume() {
//        super.onResume()
//        hideSystemUi()
//        initializePlayer()
//    }
//
//    public override fun onPause() {
//        super.onPause()
//        releasePlayer()
//    }
//
//    public override fun onStop() {
//        super.onStop()
//        releasePlayer()
//    }
//
//    @SuppressLint("InlinedApi")
//    private fun hideSystemUi() {
//        playerView.systemUiVisibility = (View.SYSTEM_UI_FLAG_LOW_PROFILE
//                or View.SYSTEM_UI_FLAG_FULLSCREEN
//                or View.SYSTEM_UI_FLAG_LAYOUT_STABLE
//                or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
//                or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
//                or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION)
//    }

    private fun initializePlayer(){
        player = ExoPlayer.Builder(this)
            .build()
//            .also{exoPlayer ->
//                playerView.player=exoPlayer
//                val mediaItem = MediaItem.fromUri(Uri.parse("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"))
//                exoPlayer.setMediaItem(mediaItem)
//            }
        playerView.player=player
        val mediaItem = MediaItem.fromUri(Uri.parse("http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"))
        player!!.setMediaItem(mediaItem)
//        player!!.playWhenReady = playWhenReady
//        player!!.seekTo(currentWindow, playbackPosition)
        player!!.prepare()
        player!!.play()
    }
    // 종료
//    private fun releasePlayer() {
//        player?.run {
//            playbackPosition = this.currentPosition
//            currentWindow = this.currentMediaItemIndex
//            playWhenReady = this.playWhenReady
//            release()
//        }
//        player = null
//    }
}

@Composable
fun Greeting(name: String, modifier: Modifier = Modifier) {
    Text(
        text = "Hello $name!",
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    Rtsp_testTheme {
        Greeting("Android")
    }
}