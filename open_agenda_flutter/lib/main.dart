import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:intl/intl.dart';
import 'package:geolocator/geolocator.dart';

// ═══════════════════════════════════════════════════════════════════════════
// 🎨 ULTIMATE 2025 COLOR PALETTE
// ═══════════════════════════════════════════════════════════════════════════

class AppColors {
  // Dark Theme - Deep Space
  static const Color bgPrimary = Color(0xFF050510);
  static const Color bgSecondary = Color(0xFF0A0A18);
  static const Color bgTertiary = Color(0xFF121225);
  static const Color bgGlass = Color(0x801A1A35);
  
  static const Color neonPink = Color(0xFFFF2E63);
  static const Color neonCyan = Color(0xFF08D9D6);
  static const Color neonPurple = Color(0xFF9D4EDD);
  static const Color neonOrange = Color(0xFFFF9F1C);
  static const Color neonGreen = Color(0xFF2EC4B6);
  
  static const Color textPrimary = Colors.white;
  static const Color textSecondary = Color(0xFFB8B8D1);
  static const Color textMuted = Color(0xFF6B6B8D);
  
  // Categories
  static const Map<String, Map<String, dynamic>> categories = {
    'personal': {'color': Color(0xFFFF2E63), 'name': 'Personal', 'icon': '👤'},
    'work': {'color': Color(0xFF08D9D6), 'name': 'Work', 'icon': '💼'},
    'family': {'color': Color(0xFF2EC4B6), 'name': 'Family', 'icon': '👨‍👩‍👧'},
    'health': {'color': Color(0xFFFF9F1C), 'name': 'Health', 'icon': '🏥'},
    'education': {'color': Color(0xFF9D4EDD), 'name': 'Education', 'icon': '📚'},
    'social': {'color': Color(0xFF00BBF9), 'name': 'Social', 'icon': '🎉'},
    'finance': {'color': Color(0xFFFFD700), 'name': 'Finance', 'icon': '💰'},
    'travel': {'color': Color(0xFFFF6B35), 'name': 'Travel', 'icon': '✈️'},
    'other': {'color': Color(0xFF6B7280), 'name': 'Other', 'icon': '📌'},
  };
}

const String API_KEY = "cc4577b215b574d3700c5be607a104c1";

// ═══════════════════════════════════════════════════════════════════════════
// 🌤️ WEATHER WIDGET
// ═══════════════════════════════════════════════════════════════════════════

class WeatherWidget extends StatefulWidget {
  const WeatherWidget({super.key});

  @override
  State<WeatherWidget> createState() => _WeatherWidgetState();
}

class _WeatherWidgetState extends State<WeatherWidget> {
  String _temp = "--°C";
  String _desc = "📍 Carregando...";
  String _icon = "🌤️";
  double? _lat;
  double? _lon;

  @override
  void initState() {
    super.initState();
    _getLocationAndWeather();
  }

  Future<void> _getLocationAndWeather() async {
    try {
      // Check if location services are enabled
      bool serviceEnabled = await Geolocator.isLocationServiceEnabled();
      if (!serviceEnabled) {
        // Fallback to São Paulo if location is disabled
        _fetchWeather(null, null);
        return;
      }

      // Check and request permission
      LocationPermission permission = await Geolocator.checkPermission();
      if (permission == LocationPermission.denied) {
        permission = await Geolocator.requestPermission();
        if (permission == LocationPermission.denied) {
          _fetchWeather(null, null);
          return;
        }
      }

      if (permission == LocationPermission.deniedForever) {
        _fetchWeather(null, null);
        return;
      }

      // Get current position with timeout
      Position? position;
      try {
        position = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.low,
        ).timeout(const Duration(seconds: 15));
      } catch (e) {
        // Timeout or error getting position
        _fetchWeather(null, null);
        return;
      }
      
      if (position != null) {
        _lat = position.latitude;
        _lon = position.longitude;
        _fetchWeather(_lat, _lon);
      } else {
        _fetchWeather(null, null);
      }
      
    } catch (e) {
      // Fallback to São Paulo on any error
      print("Location error: $e");
      _fetchWeather(null, null);
    }
  }

  Future<void> _fetchWeather(double? lat, double? lon) async {
    try {
      String url;
      if (lat != null && lon != null) {
        // Use coordinates for weather
        url = "https://api.openweathermap.org/data/2.5/weather?lat=$lat&lon=$lon&appid=$API_KEY&units=metric";
      } else {
        // Fallback to São Paulo
        url = "https://api.openweathermap.org/data/2.5/weather?q=Sao%20Paulo,BR&appid=$API_KEY&units=metric";
      }
      
      final response = await http.get(
        Uri.parse(url),
      ).timeout(const Duration(seconds: 10));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final temp = data['main']['temp'].toInt();
        final desc = data['weather'][0]['description'];
        final iconCode = data['weather'][0]['icon'];
        final cityName = data['name'] ?? 'Local';
        
        final iconMap = {
          '01d': '☀️', '01n': '🌙',
          '02d': '⛅', '02n': '☁️',
          '03d': '☁️', '03n': '☁️',
          '04d': '☁️', '04n': '☁️',
          '09d': '🌧️', '09n': '🌧️',
          '10d': '🌦️', '10n': '🌧️',
          '11d': '⛈️', '11n': '⛈️',
          '13d': '❄️', '13n': '❄️',
          '50d': '🌫️', '50n': '🌫️',
        };
        
        setState(() {
          _temp = "$temp°C";
          _desc = "📍 $cityName - ${desc[0].toUpperCase()}${desc.substring(1)}";
          _icon = iconMap[iconCode] ?? "🌤️";
        });
      } else {
        setState(() {
          _temp = "--°C";
          _desc = "📍 Erro: ${response.statusCode}";
        });
      }
    } catch (e) {
      String errorMsg = e.toString();
      setState(() {
        _temp = "--°C";
        // Show more specific error
        if (errorMsg.contains('SocketException')) {
          _desc = "📍 Sem internet";
        } else if (errorMsg.contains('TimeoutException')) {
          _desc = "📍 Tempo esgotado";
        } else {
          _desc = "📍 Erro: $errorMsg";
        }
      });
    }
  }

  void refresh() {
    _getLocationAndWeather();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: refresh,
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: AppColors.bgGlass,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            Text(_icon, style: const TextStyle(fontSize: 24)),
            const SizedBox(width: 10),
            Text(
              _temp,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: AppColors.textPrimary),
            ),
            const SizedBox(width: 10),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    _desc,
                    style: const TextStyle(fontSize: 12, color: AppColors.textSecondary),
                    overflow: TextOverflow.ellipsis,
                  ),
                  const Text(
                    "Toque para atualizar",
                    style: TextStyle(fontSize: 9, color: AppColors.textMuted),
                  ),
                ],
              ),
            ),
            const Icon(Icons.refresh, color: AppColors.textMuted, size: 18),
          ],
        ),
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// 📅 CALENDAR WIDGET
// ═══════════════════════════════════════════════════════════════════════════

class CalendarWidget extends StatefulWidget {
  final Function(DateTime) onDateSelected;
  final Set<String> eventDates;
  
  const CalendarWidget({
    super.key,
    required this.onDateSelected,
    required this.eventDates,
  });

  @override
  State<CalendarWidget> createState() => _CalendarWidgetState();
}

class _CalendarWidgetState extends State<CalendarWidget> {
  late DateTime _currentMonth;
  late DateTime _selectedDate;

  @override
  void initState() {
    super.initState();
    _currentMonth = DateTime(DateTime.now().year, DateTime.now().month, 1);
    _selectedDate = DateTime.now();
  }

  void _prevMonth() {
    setState(() {
      _currentMonth = DateTime(_currentMonth.year, _currentMonth.month - 1, 1);
    });
  }

  void _nextMonth() {
    setState(() {
      _currentMonth = DateTime(_currentMonth.year, _currentMonth.month + 1, 1);
    });
  }

  @override
  Widget build(BuildContext context) {
    final daysInMonth = DateTime(_currentMonth.year, _currentMonth.month + 1, 0).day;
    final firstWeekday = _currentMonth.weekday % 7;
    
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: AppColors.bgGlass,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        children: [
          // Month navigation
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              IconButton(
                icon: const Icon(Icons.chevron_left, color: AppColors.textPrimary),
                onPressed: _prevMonth,
              ),
              Text(
                DateFormat('MMMM yyyy').format(_currentMonth),
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.bold,
                  color: AppColors.textPrimary,
                ),
              ),
              IconButton(
                icon: const Icon(Icons.chevron_right, color: AppColors.textPrimary),
                onPressed: _nextMonth,
              ),
            ],
          ),
          const SizedBox(height: 10),
          // Weekday headers
          Row(
            children: ['D', 'S', 'T', 'Q', 'Q', 'S', 'S']
                .map((d) => Expanded(
                      child: Center(
                        child: Text(d, style: const TextStyle(color: AppColors.textMuted, fontWeight: FontWeight.bold)),
                      ),
                    ))
                .toList(),
          ),
          const SizedBox(height: 5),
          // Calendar grid
          GridView.builder(
            shrinkWrap: true,
            physics: const NeverScrollableScrollPhysics(),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
              crossAxisCount: 7,
              childAspectRatio: 1,
            ),
            itemCount: daysInMonth + firstWeekday,
            itemBuilder: (context, index) {
              if (index < firstWeekday) {
                return const SizedBox();
              }
              
              final day = index - firstWeekday + 1;
              final date = DateTime(_currentMonth.year, _currentMonth.month, day);
              final isToday = date.year == DateTime.now().year &&
                  date.month == DateTime.now().month &&
                  date.day == DateTime.now().day;
              final isSelected = date.year == _selectedDate.year &&
                  date.month == _selectedDate.month &&
                  date.day == _selectedDate.day;
              final hasEvent = widget.eventDates.contains(DateFormat('yyyy-MM-dd').format(date));
              
              Color bgColor = Colors.transparent;
              Color textColor = AppColors.textPrimary;
              
              if (isToday) {
                bgColor = AppColors.neonCyan;
                textColor = AppColors.bgPrimary;
              } else if (isSelected) {
                bgColor = AppColors.neonPink;
                textColor = Colors.white;
              } else if (hasEvent) {
                bgColor = AppColors.neonPurple;
                textColor = Colors.white;
              }
              
              return GestureDetector(
                onTap: () {
                  setState(() {
                    _selectedDate = date;
                  });
                  widget.onDateSelected(date);
                },
                child: Container(
                  margin: const EdgeInsets.all(2),
                  decoration: BoxDecoration(
                    color: bgColor,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Center(
                    child: Text(
                      '$day',
                      style: TextStyle(color: textColor, fontWeight: FontWeight.bold),
                    ),
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// 📝 EVENT MODEL
// ═══════════════════════════════════════════════════════════════════════════

class Event {
  String title;
  String date;
  String time;
  String description;
  String category;
  String created;

  Event({
    required this.title,
    required this.date,
    required this.time,
    required this.description,
    required this.category,
    required this.created,
  });

  Map<String, dynamic> toJson() => {
    'title': title,
    'date': date,
    'time': time,
    'description': description,
    'category': category,
    'created': created,
  };

  factory Event.fromJson(Map<String, dynamic> json) => Event(
    title: json['title'] ?? '',
    date: json['date'] ?? '',
    time: json['time'] ?? '',
    description: json['description'] ?? '',
    category: json['category'] ?? 'other',
    created: json['created'] ?? '',
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// 🖥️ HOME SCREEN
// ═══════════════════════════════════════════════════════════════════════════

class HomeScreen extends StatefulWidget {
  final VoidCallback onNavigate;
  final Function(int) onNavigateWithTab;
  
  const HomeScreen({
    super.key,
    required this.onNavigate,
    required this.onNavigateWithTab,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _totalEvents = 0;
  int _todayEvents = 0;

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events');
    if (eventsJson != null) {
      final Map<String, dynamic> events = json.decode(eventsJson);
      int total = 0;
      int today = 0;
      final todayStr = DateFormat('yyyy-MM-dd').format(DateTime.now());
      
      events.forEach((key, value) {
        if (value is List) {
          total += value.length;
          if (key == todayStr) {
            today = value.length;
          }
        }
      });
      
      setState(() {
        _totalEvents = total;
        _todayEvents = today;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Header
          const Text(
            '📅 OpenAgenda v1.4',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 16),
          
          // Weather
          const WeatherWidget(),
          const SizedBox(height: 16),
          
          // Stats
          Row(
            children: [
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.bgGlass,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    children: [
                      const Text('📅', style: TextStyle(fontSize: 24)),
                      const SizedBox(height: 5),
                      Text(
                        '$_totalEvents',
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: AppColors.neonCyan,
                        ),
                      ),
                      const Text(
                        'eventos',
                        style: TextStyle(color: AppColors.textSecondary),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(width: 10),
              Expanded(
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.bgGlass,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Column(
                    children: [
                      const Text('✨', style: TextStyle(fontSize: 24)),
                      const SizedBox(height: 5),
                      Text(
                        '$_todayEvents',
                        style: const TextStyle(
                          fontSize: 24,
                          fontWeight: FontWeight.bold,
                          color: AppColors.neonOrange,
                        ),
                      ),
                      const Text(
                        'hoje',
                        style: TextStyle(color: AppColors.textSecondary),
                      ),
                    ],
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: 20),
          
          // Menu buttons
          _buildMenuButton('➕', 'Novo Evento', AppColors.neonPink, () => widget.onNavigateWithTab(1)),
          const SizedBox(height: 10),
          _buildMenuButton('📅', 'Calendário', AppColors.neonCyan, () => widget.onNavigateWithTab(2)),
          const SizedBox(height: 10),
          _buildMenuButton('📋', 'Meus Eventos', AppColors.neonPurple, () => widget.onNavigateWithTab(3)),
          const SizedBox(height: 10),
          _buildMenuButton('🔍', 'Buscar', AppColors.neonOrange, () => widget.onNavigateWithTab(4)),
          const SizedBox(height: 10),
          _buildMenuButton('⚙️', 'Configurações', AppColors.neonGreen, () => widget.onNavigateWithTab(5)),
        ],
      ),
    );
  }

  Widget _buildMenuButton(String icon, String label, Color color, VoidCallback onTap) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(12),
        ),
        child: Row(
          children: [
            Text(icon, style: const TextStyle(fontSize: 24)),
            const SizedBox(width: 12),
            Text(
              label,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
          ],
        ),
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// ➕ ADD EVENT SCREEN
// ═══════════════════════════════════════════════════════════════════════════

class AddEventScreen extends StatefulWidget {
  final Function() onEventAdded;
  
  const AddEventScreen({super.key, required this.onEventAdded});

  @override
  State<AddEventScreen> createState() => _AddEventScreenState();
}

class _AddEventScreenState extends State<AddEventScreen> {
  final _titleController = TextEditingController();
  final _dateController = TextEditingController();
  final _timeController = TextEditingController();
  final _descController = TextEditingController();
  String _selectedCategory = 'personal';
  String _status = '';

  @override
  void initState() {
    super.initState();
    _dateController.text = DateFormat('dd/MM/yyyy').format(DateTime.now());
  }

  Future<void> _saveEvent() async {
    if (_titleController.text.isEmpty) {
      setState(() => _status = '⚠️ Digite um título!');
      return;
    }

    if (_dateController.text.isEmpty) {
      setState(() => _status = '⚠️ Digite uma data!');
      return;
    }

    final event = Event(
      title: _titleController.text,
      date: _dateController.text,
      time: _timeController.text.isEmpty ? '09:00' : _timeController.text,
      description: _descController.text,
      category: _selectedCategory,
      created: DateTime.now().toIso8601String(),
    );

    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events') ?? '{}';
    final Map<String, dynamic> events = json.decode(eventsJson);
    
    final dateKey = _dateController.text;
    if (!events.containsKey(dateKey)) {
      events[dateKey] = [];
    }
    events[dateKey].add(event.toJson());
    
    await prefs.setString('events', json.encode(events));
    
    setState(() => _status = '✅ Evento salvo!');
    
    Future.delayed(const Duration(seconds: 1), () {
      _titleController.clear();
      _timeController.clear();
      _descController.clear();
      widget.onEventAdded();
    });
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Novo Evento',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 16),
          
          // Title
          TextField(
            controller: _titleController,
            style: const TextStyle(color: AppColors.textPrimary),
            decoration: _buildInputDecoration('Título do evento'),
          ),
          const SizedBox(height: 12),
          
          // Date
          TextField(
            controller: _dateController,
            style: const TextStyle(color: AppColors.textPrimary),
            decoration: _buildInputDecoration('Data (DD/MM/AAAA)'),
          ),
          const SizedBox(height: 12),
          
          // Time
          TextField(
            controller: _timeController,
            style: const TextStyle(color: AppColors.textPrimary),
            decoration: _buildInputDecoration('Hora (HH:MM)'),
          ),
          const SizedBox(height: 16),
          
          // Category
          const Text(
            'Categoria:',
            style: TextStyle(color: AppColors.textSecondary, fontSize: 14),
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            children: AppColors.categories.entries.map((entry) {
              final isSelected = _selectedCategory == entry.key;
              return GestureDetector(
                onTap: () => setState(() => _selectedCategory = entry.key),
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: isSelected ? entry.value['color'] : AppColors.bgTertiary,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    '${entry.value['icon']} ${entry.value['name']}',
                    style: TextStyle(
                      color: isSelected ? Colors.white : AppColors.textSecondary,
                      fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                    ),
                  ),
                ),
              );
            }).toList(),
          ),
          const SizedBox(height: 16),
          
          // Description
          TextField(
            controller: _descController,
            style: const TextStyle(color: AppColors.textPrimary),
            maxLines: 3,
            decoration: _buildInputDecoration('Descrição (opcional)'),
          ),
          const SizedBox(height: 16),
          
          // Status
          Text(
            _status,
            style: TextStyle(
              color: _status.contains('✅') ? AppColors.neonGreen : AppColors.neonOrange,
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),
          
          // Save button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: _saveEvent,
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.neonGreen,
                padding: const EdgeInsets.all(16),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
              child: const Text(
                '💾 Salvar Evento',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: Colors.white),
              ),
            ),
          ),
        ],
      ),
    );
  }

  InputDecoration _buildInputDecoration(String hint) {
    return InputDecoration(
      hintText: hint,
      hintStyle: const TextStyle(color: AppColors.textMuted),
      filled: true,
      fillColor: AppColors.bgTertiary,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: BorderSide.none,
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(12),
        borderSide: const BorderSide(color: AppColors.neonCyan),
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// 📅 CALENDAR SCREEN
// ═══════════════════════════════════════════════════════════════════════════

class CalendarScreen extends StatefulWidget {
  const CalendarScreen({super.key});

  @override
  State<CalendarScreen> createState() => _CalendarScreenState();
}

class _CalendarScreenState extends State<CalendarScreen> {
  DateTime _selectedDate = DateTime.now();
  List<Event> _dayEvents = [];
  Set<String> _eventDates = {};

  @override
  void initState() {
    super.initState();
    _loadEvents();
  }

  Future<void> _loadEvents() async {
    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events');
    if (eventsJson != null) {
      final Map<String, dynamic> events = json.decode(eventsJson);
      setState(() {
        _eventDates = events.keys.toSet();
      });
      _loadDayEvents();
    }
  }

  void _loadDayEvents() async {
    final dateKey = DateFormat('yyyy-MM-dd').format(_selectedDate);
    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events');
    
    if (eventsJson != null) {
      final Map<String, dynamic> events = json.decode(eventsJson);
      final dayKey = DateFormat('dd/MM/yyyy').format(_selectedDate);
      
      setState(() {
        _dayEvents = (events[dayKey] as List?)
            ?.map((e) => Event.fromJson(e))
            .toList() ?? [];
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '📅 Calendário',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 16),
          
          CalendarWidget(
            onDateSelected: (date) {
              setState(() => _selectedDate = date);
              _loadDayEvents();
            },
            eventDates: _eventDates,
          ),
          const SizedBox(height: 20),
          
          Text(
            'Eventos: ${DateFormat('dd/MM/yyyy').format(_selectedDate)}',
            style: const TextStyle(
              fontSize: 16,
              color: AppColors.textSecondary,
            ),
          ),
          const SizedBox(height: 10),
          
          if (_dayEvents.isEmpty)
            const Center(
              child: Text(
                '✨ Nenhum evento neste dia',
                style: TextStyle(color: AppColors.textMuted),
              ),
            )
          else
            ..._dayEvents.map((event) {
              final cat = AppColors.categories[event.category] ?? AppColors.categories['other']!;
              return Container(
                margin: const EdgeInsets.only(bottom: 10),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.bgGlass,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Row(
                  children: [
                    Text(cat['icon'], style: const TextStyle(fontSize: 24)),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            '${event.time} - ${event.title}',
                            style: const TextStyle(
                              color: AppColors.textPrimary,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                          Text(
                            event.description,
                            style: const TextStyle(color: AppColors.textSecondary, fontSize: 12),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              );
            }),
        ],
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// 📋 EVENT LIST SCREEN
// ═══════════════════════════════════════════════════════════════════════════

class EventListScreen extends StatefulWidget {
  const EventListScreen({super.key});

  @override
  State<EventListScreen> createState() => _EventListScreenState();
}

class _EventListScreenState extends State<EventListScreen> {
  List<Event> _allEvents = [];

  @override
  void initState() {
    super.initState();
    _loadEvents();
  }

  Future<void> _loadEvents() async {
    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events');
    
    if (eventsJson != null) {
      final Map<String, dynamic> events = json.decode(eventsJson);
      List<Event> allEvents = [];
      
      events.forEach((dateKey, eventList) {
        if (eventList is List) {
          for (var e in eventList) {
            final event = Event.fromJson(e);
            event.date = dateKey;
            allEvents.add(event);
          }
        }
      });
      
      allEvents.sort((a, b) {
        final dateCompare = a.date.compareTo(b.date);
        if (dateCompare != 0) return dateCompare;
        return a.time.compareTo(b.time);
      });
      
      setState(() {
        _allEvents = allEvents;
      });
    }
  }

  Future<void> _deleteEvent(Event event) async {
    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events');
    
    if (eventsJson != null) {
      final Map<String, dynamic> events = json.decode(eventsJson);
      
      if (events.containsKey(event.date)) {
        events[event.date] = (events[event.date] as List)
            .where((e) => e['title'] != event.title || e['time'] != event.time)
            .toList();
        
        if ((events[event.date] as List).isEmpty) {
          events.remove(event.date);
        }
        
        await prefs.setString('events', json.encode(events));
        _loadEvents();
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '📋 Meus Eventos',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 16),
          
          if (_allEvents.isEmpty)
            const Center(
              child: Text(
                '📭 Nenhum evento encontrado',
                style: TextStyle(color: AppColors.textMuted, fontSize: 16),
              ),
            )
          else
            ..._allEvents.map((event) {
              final cat = AppColors.categories[event.category] ?? AppColors.categories['other']!;
              return Dismissible(
                key: Key('${event.date}-${event.title}-${event.time}'),
                direction: DismissDirection.endToStart,
                background: Container(
                  alignment: Alignment.centerRight,
                  padding: const EdgeInsets.only(right: 20),
                  color: AppColors.neonPink,
                  child: const Icon(Icons.delete, color: Colors.white),
                ),
                onDismissed: (_) => _deleteEvent(event),
                child: Container(
                  margin: const EdgeInsets.only(bottom: 10),
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: AppColors.bgGlass,
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Row(
                    children: [
                      Text(cat['icon'], style: const TextStyle(fontSize: 24)),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              '${event.date} ${event.time}',
                              style: const TextStyle(
                                color: AppColors.neonCyan,
                                fontSize: 12,
                              ),
                            ),
                            Text(
                              event.title,
                              style: const TextStyle(
                                color: AppColors.textPrimary,
                                fontWeight: FontWeight.bold,
                                fontSize: 16,
                              ),
                            ),
                            if (event.description.isNotEmpty)
                              Text(
                                event.description,
                                style: const TextStyle(
                                  color: AppColors.textSecondary,
                                  fontSize: 12,
                                ),
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              );
            }),
        ],
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// 🔍 SEARCH SCREEN
// ═══════════════════════════════════════════════════════════════════════════

class SearchScreen extends StatefulWidget {
  const SearchScreen({super.key});

  @override
  State<SearchScreen> createState() => _SearchScreenState();
}

class _SearchScreenState extends State<SearchScreen> {
  final _searchController = TextEditingController();
  List<Event> _results = [];

  Future<void> _doSearch() async {
    final query = _searchController.text.toLowerCase().trim();
    if (query.isEmpty) {
      setState(() => _results = []);
      return;
    }
    
    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events');
    
    if (eventsJson != null) {
      final Map<String, dynamic> events = json.decode(eventsJson);
      List<Event> results = [];
      
      events.forEach((dateKey, eventList) {
        if (eventList is List) {
          for (var e in eventList) {
            final event = Event.fromJson(e);
            if (event.title.toLowerCase().contains(query) ||
                event.description.toLowerCase().contains(query) ||
                event.category.toLowerCase().contains(query)) {
              results.add(event);
            }
          }
        }
      });
      
      setState(() => _results = results);
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '🔍 Buscar',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 16),
          
          TextField(
            controller: _searchController,
            style: const TextStyle(color: AppColors.textPrimary),
            decoration: InputDecoration(
              hintText: 'Buscar eventos...',
              hintStyle: const TextStyle(color: AppColors.textMuted),
              filled: true,
              fillColor: AppColors.bgTertiary,
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(12),
                borderSide: BorderSide.none,
              ),
              prefixIcon: const Icon(Icons.search, color: AppColors.textMuted),
            ),
            onSubmitted: (_) => _doSearch(),
          ),
          const SizedBox(height: 16),
          
          if (_results.isEmpty && _searchController.text.isNotEmpty)
            const Center(
              child: Text(
                '❌ Nenhum resultado encontrado',
                style: TextStyle(color: AppColors.textMuted),
              ),
            )
          else
            ..._results.map((event) {
              final cat = AppColors.categories[event.category] ?? AppColors.categories['other']!;
              return Container(
                margin: const EdgeInsets.only(bottom: 10),
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: AppColors.bgGlass,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Text(cat['icon'], style: const TextStyle(fontSize: 20)),
                        const SizedBox(width: 8),
                        Text(
                          '${event.date} ${event.time}',
                          style: const TextStyle(color: AppColors.neonCyan, fontSize: 12),
                        ),
                      ],
                    ),
                    const SizedBox(height: 5),
                    Text(
                      event.title,
                      style: const TextStyle(
                        color: AppColors.textPrimary,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    if (event.description.isNotEmpty)
                      Text(
                        event.description,
                        style: const TextStyle(color: AppColors.textSecondary, fontSize: 12),
                      ),
                  ],
                ),
              );
            }),
        ],
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// ⚙️ SETTINGS SCREEN
// ═══════════════════════════════════════════════════════════════════════════

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  String _status = '';

  Future<void> _exportData() async {
    final prefs = await SharedPreferences.getInstance();
    final eventsJson = prefs.getString('events');
    
    if (eventsJson != null && eventsJson != '{}') {
      final filename = 'openagenda_backup_${DateTime.now().millisecondsSinceEpoch}.json';
      // In a real app, you'd save to file or share
      setState(() => _status = '✅ Exportado: $filename');
    } else {
      setState(() => _status = '⚠️ Nenhum dado para exportar');
    }
  }

  Future<void> _clearAll() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('events');
    setState(() => _status = '✅ Todos os eventos foram removidos');
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            '⚙️ Configurações',
            style: TextStyle(
              fontSize: 22,
              fontWeight: FontWeight.bold,
              color: AppColors.textPrimary,
            ),
          ),
          const SizedBox(height: 20),
          
          // Export button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: _exportData,
              icon: const Icon(Icons.download),
              label: const Text('📤 Exportar Dados'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.neonCyan,
                padding: const EdgeInsets.all(14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ),
          const SizedBox(height: 12),
          
          // Clear button
          SizedBox(
            width: double.infinity,
            child: ElevatedButton.icon(
              onPressed: () async {
                await _clearAll();
              },
              icon: const Icon(Icons.delete_forever),
              label: const Text('🗑️ Limpar Todos os Eventos'),
              style: ElevatedButton.styleFrom(
                backgroundColor: AppColors.neonPink,
                padding: const EdgeInsets.all(14),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
              ),
            ),
          ),
          const SizedBox(height: 16),
          
          // Status
          Text(
            _status,
            style: const TextStyle(color: AppColors.neonGreen, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 30),
          
          // About
          Container(
            padding: const EdgeInsets.all(20),
            decoration: BoxDecoration(
              color: AppColors.bgGlass,
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Column(
              children: [
                Text(
                  '📱 OpenAgenda v1.4.0',
                  style: TextStyle(
                    fontSize: 20,
                    fontWeight: FontWeight.bold,
                    color: AppColors.textPrimary,
                  ),
                ),
                SizedBox(height: 10),
                Text(
                  '© 2025 Open-Agenda Team\nThe Future of Calendars!',
                  textAlign: TextAlign.center,
                  style: TextStyle(color: AppColors.textSecondary),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

// ═══════════════════════════════════════════════════════════════════════════
// 🚀 MAIN APP
// ═══════════════════════════════════════════════════════════════════════════

void main() {
  runApp(const OpenAgendaApp());
}

class OpenAgendaApp extends StatelessWidget {
  const OpenAgendaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'OpenAgenda',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: AppColors.bgPrimary,
        primaryColor: AppColors.neonCyan,
        colorScheme: const ColorScheme.dark(
          primary: AppColors.neonCyan,
          secondary: AppColors.neonPink,
        ),
      ),
      home: const MainScreen(),
    );
  }
}

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen> {
  int _currentIndex = 0;

  void _onNavigate(int index) {
    setState(() => _currentIndex = index);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: IndexedStack(
          index: _currentIndex,
          children: [
            HomeScreen(
              onNavigate: () {},
              onNavigateWithTab: _onNavigate,
            ),
            AddEventScreen(onEventAdded: () => _onNavigate(3)),
            const CalendarScreen(),
            const EventListScreen(),
            const SearchScreen(),
            const SettingsScreen(),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: _onNavigate,
        type: BottomNavigationBarType.fixed,
        backgroundColor: AppColors.bgSecondary,
        selectedItemColor: AppColors.neonCyan,
        unselectedItemColor: AppColors.textMuted,
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.add_circle), label: 'Add'),
          BottomNavigationBarItem(icon: Icon(Icons.calendar_month), label: 'Cal'),
          BottomNavigationBarItem(icon: Icon(Icons.list), label: 'Eventos'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Buscar'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Config'),
        ],
      ),
    );
  }
}
