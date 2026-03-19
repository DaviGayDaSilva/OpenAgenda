package com.openagenda.app

import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity
import androidx.cardview.widget.CardView
import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import okhttp3.*
import java.io.File
import java.util.*
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {

    private val client = OkHttpClient()
    private val gson = Gson()
    private val API_KEY = "cc4577b215b574d3700c5be607a104c1"
    
    private lateinit var events: MutableList<Event>
    private var currentScreen = "home"

    data class Event(val title: String, val date: String, val time: String, val desc: String)
    data class WeatherResponse(val main: Main, val weather: List<WeatherDesc>)
    data class Main(val temp: Double)
    data class WeatherDesc(val description: String)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        try {
            loadEvents()
            showHome()
        } catch (e: Exception) {
            e.printStackTrace()
            Toast.makeText(this, "Erro ao iniciar: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }

    private fun getDataFile(): File {
        val dir = File(filesDir, "data")
        if (!dir.exists()) dir.mkdirs()
        return File(dir, "events.json")
    }

    private fun loadEvents() {
        val file = getDataFile()
        if (file.exists()) {
            val json = file.readText()
            val type = object : TypeToken<MutableList<Event>>() {}.type
            events = gson.fromJson(json, type) ?: mutableListOf()
        } else {
            events = mutableListOf()
        }
    }

    private fun saveEvents() {
        val json = gson.toJson(events)
        getDataFile().writeText(json)
    }

    private fun showHome() {
        currentScreen = "home"
        setContentView(R.layout.home)
        
        findViewById<TextView>(R.id.eventCount).text = "📅 ${events.size} eventos"
        fetchWeather()
    }

    private fun fetchWeather() {
        thread {
            try {
                val request = Request.Builder()
                    .url("https://api.openweathermap.org/data/2.5/weather?q=SaoPaulo&appid=$API_KEY&units=metric")
                    .build()
                
                client.newCall(request).execute().use { response ->
                    if (response.isSuccessful) {
                        val weather = gson.fromJson(response.body?.string(), WeatherResponse::class.java)
                        runOnUiThread {
                            findViewById<TextView>(R.id.weatherText).text = 
                                "🌤️ ${weather.main.temp.toInt()}°C - ${weather.weather[0].description.replaceFirstChar { it.uppercase() }}"
                        }
                    }
                }
            } catch (e: Exception) {
                runOnUiThread {
                    findViewById<TextView>(R.id.weatherText).text = "🌤️ --°C"
                }
            }
        }
    }

    fun goToAddEvent(view: View) {
        currentScreen = "add"
        setContentView(R.layout.add_event)
    }

    fun goToEventList(view: View) {
        currentScreen = "list"
        setContentView(R.layout.event_list)
        
        val listView = findViewById<ListView>(R.id.eventsList)
        if (events.isEmpty()) {
            listView.adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, arrayOf("Nenhum evento"))
        } else {
            val eventStrings = events.map { "${it.date} - ${it.title}" }.toTypedArray()
            listView.adapter = ArrayAdapter(this, android.R.layout.simple_list_item_1, eventStrings)
        }
    }

    fun goToSettings(view: View) {
        currentScreen = "settings"
        setContentView(R.layout.settings)
    }

    fun saveEvent(view: View) {
        val title = findViewById<EditText>(R.id.titleInput).text.toString()
        val date = findViewById<EditText>(R.id.dateInput).text.toString()
        val time = findViewById<EditText>(R.id.timeInput).text.toString()
        val desc = findViewById<EditText>(R.id.descInput).text.toString()

        if (title.isNotEmpty() && date.isNotEmpty()) {
            events.add(Event(title, date, time, desc))
            saveEvents()
            Toast.makeText(this, "Evento salvo!", Toast.LENGTH_SHORT).show()
            showHome()
        } else {
            Toast.makeText(this, "Preencha título e data!", Toast.LENGTH_SHORT).show()
        }
    }

    fun goHome(view: View) {
        showHome()
    }

    @Deprecated("Deprecated in Java")
    override fun onBackPressed() {
        if (currentScreen != "home") {
            showHome()
        } else {
            super.onBackPressed()
        }
    }
}
