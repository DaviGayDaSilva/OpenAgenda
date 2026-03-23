# Open-Agenda 🗓️

**The Best Agenda in the World!** - Open Source, intelligent and easy to use!

---

## Aviso Importante
> O App usa permissão de localização pra nada de malicioso, só pra mostrar a temperatura então se estiver rodando em segundo plano ou usando toda hora, provavelmente você baixou 1 versão maliciosa feito por outro usuário, acesse sempre pelo repo original pra evitar coisas maliciosas

## 🌟 Features

- 🌙 **Beautiful Modern Dark Interface** - Easy on the eyes
- 📅 **Interactive Monthly Calendar** - Navigate months with ease
- ➕ **Add/Edit/Delete Events** - Simple and intuitive
- 💾 **Save & Load Data from JSON** - Upload your agenda files!
- 📱 **Local Storage** - Your data stays on your device
- 🆓 **100% Open Source & Free!**

---

## 📦 Installation

### From .deb Package (Debian/Ubuntu/Linux Mint)

```bash
# Navigate to the package location
cd /path/to/open-agenda_1.0.0_all.deb

# Install the package
sudo dpkg -i open-agenda_1.0.0_all.deb

# Install dependencies
sudo apt-get install -f
```

### Run Directly (Any Python 3 System)

```bash
# Extract the ZIP or navigate to the source
cd open-agenda

# Run the application
python3 usr/share/open-agenda/open_agenda.py
```

---

## 📖 Usage

### Adding Events
1. Click on a date in the calendar
2. Enter the time (HH:MM format)
3. Enter the event title
4. Click "+ Add Event"

### Loading Data (Upload File)
1. Click the **📂 Load File** button
2. Select your previously saved JSON agenda file
3. Your events will be loaded!

### Saving Data
1. Click the **💾 Save File** button
2. Choose where to save your JSON file
3. Your agenda is backed up!

### Deleting Events
- Double-click on an event to delete it, OR
- Select an event and click **🗑️ Delete Selected**

---

## 💾 Data Format

Your agenda is saved as JSON files with the following structure:

```json
{
  "2025-03-06": [
    {
      "time": "09:00",
      "title": "Meeting with team",
      "created": "2025-03-06T10:00:00"
    }
  ],
  "2025-03-15": [
    {
      "time": "14:30",
      "title": "Doctor appointment",
      "created": "2025-03-06T11:00:00"
    }
  ]
}
```

---

## 🔧 Requirements

- Python 3.x
- python3-tk (Tkinter)

### Installing Dependencies (Ubuntu/Debian)

```bash
sudo apt-get install python3 python3-tk
```

### Installing Dependencies (Fedora)

```bash
sudo dnf install python3 tkinter
```

### Installing Dependencies (macOS)

```bash
brew install python-tk
```

---

## 🎨 Screenshots

The app features:
- Beautiful dark purple theme
- Color-coded calendar (today highlighted in blue, events in purple)
- Easy-to-use event management
- Clean and modern interface

---

## 📁 Project Structure

```
open-agenda/
├── DEBIAN/
│   └── control          # Package metadata
├── usr/
│   └── share/
│       ├── open-agenda/
│       │   └── open_agenda.py    # Main application
│       ├── applications/
│       │   └── open-agenda.desktop  # Desktop entry
│       └── pixmaps/
│           └── open-agenda-icon.png  # App icon
```

---

## 🔓 License

MIT License - Open source and free to use!

```
MIT License

Copyright (c) 2025 Open-Agenda Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👨‍💻 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Contact

- Email: team@open-agenda.org
- Website: https://github.com/open-agenda/open-agenda

---

Made with ❤️ by the **Open-Agenda Team**

*The best agenda in the world! 🌍*
