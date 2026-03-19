package com.openagenda.app

import android.os.Bundle
import android.view.View
import android.widget.*
import androidx.appcompat.app.AppCompatActivity

class MainActivity : AppCompatActivity() {

    private var currentScreen = "home"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        showHome()
    }

    private fun showHome() {
        currentScreen = "home"
        
        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL
        layout.setPadding(50, 100, 50, 50)
        layout.setBackgroundColor(0xFF0D0D1A.toInt())
        
        val title = TextView(this)
        title.text = "OpenAgenda v1.4"
        title.textSize = 24f
        title.setTextColor(0xFFFFFFFF.toInt())
        title.gravity = android.view.Gravity.CENTER
        
        val weather = TextView(this)
        weather.text = "🌤️ São Paulo: 25°C"
        weather.textSize = 18f
        weather.setTextColor(0xFFFFFFFF.toInt())
        weather.gravity = android.view.Gravity.CENTER
        weather.setPadding(0, 30, 0, 30)
        
        val events = TextView(this)
        events.text = "📅 0 eventos"
        events.textSize = 18f
        events.setTextColor(0xFFFFFFFF.toInt())
        events.gravity = android.view.Gravity.CENTER
        
        val btnAdd = Button(this)
        btnAdd.text = "➕ Adicionar Evento"
        btnAdd.setBackgroundColor(0xFF4D7CFF.toInt())
        btnAdd.setTextColor(0xFFFFFFFF.toInt())
        btnAdd.setPadding(20, 30, 20, 30)
        btnAdd.setOnClickListener { showAddEvent() }
        
        val btnList = Button(this)
        btnList.text = "📋 Ver Eventos"
        btnList.setBackgroundColor(0xFF33CCBB.toInt())
        btnList.setTextColor(0xFFFFFFFF.toInt())
        btnList.setPadding(20, 30, 20, 30)
        btnList.setOnClickListener { showEventList() }
        
        val btnSettings = Button(this)
        btnSettings.text = "⚙️ Configurações"
        btnSettings.setBackgroundColor(0xFFFF7F50.toInt())
        btnSettings.setTextColor(0xFFFFFFFF.toInt())
        btnSettings.setPadding(20, 30, 20, 30)
        btnSettings.setOnClickListener { showSettings() }
        
        layout.addView(title)
        layout.addView(weather)
        layout.addView(events)
        layout.addView(btnAdd)
        layout.addView(btnList)
        layout.addView(btnSettings)
        
        setContentView(layout)
    }

    private fun showAddEvent() {
        currentScreen = "add"
        
        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL
        layout.setPadding(50, 50, 50, 50)
        layout.setBackgroundColor(0xFF0D0D1A.toInt())
        
        val titleLabel = TextView(this)
        titleLabel.text = "Novo Evento"
        titleLabel.textSize = 22f
        titleLabel.setTextColor(0xFFFFFFFF.toInt())
        titleLabel.gravity = android.view.Gravity.CENTER
        
        val inputTitle = EditText(this)
        inputTitle.hint = "Título"
        inputTitle.setTextColor(0xFFFFFFFF.toInt())
        inputTitle.setHintTextColor(0x80FFFFFF.toInt())
        
        val inputDate = EditText(this)
        inputDate.hint = "Data (ex: 19/03/2026)"
        inputDate.setTextColor(0xFFFFFFFF.toInt())
        inputDate.setHintTextColor(0x80FFFFFF.toInt())
        
        val inputTime = EditText(this)
        inputTime.hint = "Hora (ex: 14:00)"
        inputTime.setTextColor(0xFFFFFFFF.toInt())
        inputTime.setHintTextColor(0x80FFFFFF.toInt())
        
        val inputDesc = EditText(this)
        inputDesc.hint = "Descrição"
        inputDesc.setTextColor(0xFFFFFFFF.toInt())
        inputDesc.setHintTextColor(0x80FFFFFF.toInt())
        inputDesc.minLines = 3
        
        val btnSave = Button(this)
        btnSave.text = "💾 Salvar"
        btnSave.setBackgroundColor(0xFF4D7CFF.toInt())
        btnSave.setTextColor(0xFFFFFFFF.toInt())
        
        val btnBack = Button(this)
        btnBack.text = "⬅️ Voltar"
        btnBack.setBackgroundColor(0xFF666666.toInt())
        btnBack.setTextColor(0xFFFFFFFF.toInt())
        btnBack.setOnClickListener { showHome() }
        
        layout.addView(titleLabel)
        layout.addView(inputTitle)
        layout.addView(inputDate)
        layout.addView(inputTime)
        layout.addView(inputDesc)
        layout.addView(btnSave)
        layout.addView(btnBack)
        
        setContentView(layout)
    }

    private fun showEventList() {
        currentScreen = "list"
        
        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL
        layout.setPadding(50, 50, 50, 50)
        layout.setBackgroundColor(0xFF0D0D1A.toInt())
        
        val title = TextView(this)
        title.text = "Meus Eventos"
        title.textSize = 22f
        title.setTextColor(0xFFFFFFFF.toInt())
        title.gravity = android.view.Gravity.CENTER
        
        val empty = TextView(this)
        empty.text = "Nenhum evento cadastrado"
        empty.textSize = 16f
        empty.setTextColor(0x80FFFFFF.toInt())
        empty.gravity = android.view.Gravity.CENTER
        
        val btnBack = Button(this)
        btnBack.text = "⬅️ Voltar"
        btnBack.setBackgroundColor(0xFF666666.toInt())
        btnBack.setTextColor(0xFFFFFFFF.toInt())
        btnBack.setOnClickListener { showHome() }
        
        layout.addView(title)
        layout.addView(empty)
        layout.addView(btnBack)
        
        setContentView(layout)
    }

    private fun showSettings() {
        currentScreen = "settings"
        
        val layout = LinearLayout(this)
        layout.orientation = LinearLayout.VERTICAL
        layout.setPadding(50, 50, 50, 50)
        layout.setBackgroundColor(0xFF0D0D1A.toInt())
        
        val title = TextView(this)
        title.text = "Configurações"
        title.textSize = 22f
        title.setTextColor(0xFFFFFFFF.toInt())
        title.gravity = android.view.Gravity.CENTER
        
        val version = TextView(this)
        version.text = "OpenAgenda v1.4"
        version.textSize = 14f
        version.setTextColor(0x80FFFFFF.toInt())
        version.gravity = android.view.Gravity.CENTER
        
        val btnBack = Button(this)
        btnBack.text = "⬅️ Voltar"
        btnBack.setBackgroundColor(0xFF666666.toInt())
        btnBack.setTextColor(0xFFFFFFFF.toInt())
        btnBack.setOnClickListener { showHome() }
        
        layout.addView(title)
        layout.addView(version)
        layout.addView(btnBack)
        
        setContentView(layout)
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
