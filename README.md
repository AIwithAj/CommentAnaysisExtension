# YouTube Sentiment Analysis Pro - Chrome Extension

A modern Chrome extension that provides advanced sentiment analysis for YouTube video comments using AI-powered machine learning models. Features a stunning glassmorphism dashboard with real-time analytics and beautiful visualizations.

## ✨ Features

### 🎯 Core Functionality
- **Real-time Sentiment Analysis**: AI-powered analysis of YouTube comments
- **YouTube Integration**: Seamlessly analyzes comments from any YouTube video
- **Comprehensive Metrics**: Total comments, unique users, engagement scores, and sentiment distribution
- **Advanced Visualizations**: Multiple chart types using Chart.js and D3.js

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Ultra-modern glass-morphism interface with blur effects
- **Dark Theme**: Sleek dark theme with electric blue and purple gradients
- **Responsive Layout**: Optimized for Chrome extension popup (420px width)
- **Smooth Animations**: CSS animations and micro-interactions
- **Real-time Updates**: Live data updates with loading states

### 📊 Analytics Dashboard
- **Sentiment Distribution**: 3D doughnut chart showing positive, neutral, negative sentiment
- **Trend Analysis**: Multi-line area chart for sentiment trends over time
- **Word Cloud**: Interactive keyword visualization with sentiment-based colors
- **Top Comments**: Categorized display of most positive, negative, and engaging comments
- **Metrics Cards**: Animated cards showing key statistics

## 🛠 Tech Stack

### Backend (`backend/`)
- **Python Flask**: Optimized API server for sentiment analysis
- **NLTK**: Natural language processing and text preprocessing
- **Pandas**: Data manipulation and time-series analysis
- **Flask-CORS**: Cross-origin resource sharing for browser integration

### Frontend (`frontend/`)
- **Vue 3**: Progressive JavaScript framework with Options API
- **Bootstrap 5**: Modern CSS framework for responsive design
- **Chart.js v4**: Primary charting library for data visualization
- **D3.js v7**: Advanced data visualizations for word clouds
- **Feather Icons**: Beautiful SVG icons for UI elements
- **Custom CSS**: Glassmorphism effects and smooth animations

## 📁 Project Structure

## 📂 Project Structure

```
├── src/
│   ├── components/
│   │   ├── DashboardApp.vue
│   │   ├── MetricsCards.vue
│   │   ├── SentimentChart.vue
│   │   ├── SentimentGaugeChart.vue
│   │   ├── TrendChart.vue
│   │   ├── SentimentRadarChart.vue
│   │   ├── WordCloud.vue
│   │   └── CommentsSection.vue
│   ├── main.js
│   └── demo.js
├── public/
│   ├── popup.html
│   ├── demo.html
│   ├── manifest.json
│   └── styles/
│       └── dashboard.css
└── dist/ (generated)
    ├── popup.html
    ├── demo.html
    ├── manifest.json
    ├── assets/
    └── styles/
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+ (for development)
- Chrome Browser
- YouTube Data API Key (for fetching comments)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Flask server:**
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:8000`

### Frontend Setup

1. **Get YouTube Data API Key:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create credentials (API key)
   - Copy the API key

2. **Configure API Key:**
   - Open `frontend/components/DashboardApp.js`
   - Replace `YOUR_API_KEY` with your actual YouTube API key:
     ```javascript
     const API_KEY = 'your_actual_api_key_here';
     ```

3. **Update Backend URL (if needed):**
   - In `frontend/components/DashboardApp.js`, update the API URL:
     ```javascript
     apiUrl: 'http://localhost:8000' // Change if backend runs on different port
     ```

## 🌐 Chrome Extension Deployment

### Development Mode (Testing)

1. **Open Chrome Extensions Page:**
   - Go to `chrome://extensions/`
   - Enable "Developer mode" (toggle in top right)

2. **Load Extension:**
   - Click "Load unpacked"
   - Select the `frontend/` folder
   - The extension will appear in your extensions list

3. **Test the Extension:**
   - Navigate to any YouTube video
   - Click the extension icon in the Chrome toolbar
   - The sentiment analysis dashboard should load

### Production Deployment

1. **Prepare for Distribution:**
   - Update `manifest.json` version number
   - Test thoroughly in development mode
   - Create extension screenshots and descriptions

2. **Package Extension:**
   - Zip the entire `frontend/` folder
   - Name it `youtube-sentiment-analysis-pro.zip`

3. **Chrome Web Store Submission:**
   - Go to [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/developer/dashboard)
   - Click "Add new item"
   - Upload your zip file
   - Fill in store listing information
   - Submit for review

## ⚙️ Configuration

### Backend Configuration

**Environment Variables:**
```bash
export PORT=8000                    # Flask server port
export FLASK_ENV=development        # Development mode
export NLTK_DATA=/path/to/nltk_data # NLTK data directory
```

**CORS Settings:**
The backend is configured to accept requests from Chrome extensions. Modify `app.py` if you need different CORS settings.

### Frontend Configuration

**API Endpoints:**
- Update `DashboardApp.js` to point to your production backend
- For production, use HTTPS endpoints

**Permissions:**
The extension requires these permissions (defined in `manifest.json`):
- `tabs` - Access to current tab information
- `activeTab` - Read URLs of active tabs
- `scripting` - Inject content scripts
- `storage` - Local data storage

## 🔧 Development
      
### Running in Development Mode

1. **Start Backend:**
   ```bash
   cd bac         kend
   python app.py
   ```

2. **Load Extension:**
   - Open Chrome and go to `chrome://extensions/`
   - Load the `frontend/` folder as unpacked extension

3. **Live Development:**
   - Make changes to Vue components in `frontend/components/`
   - Refresh the extension popup to see changes
   - Backend changes require server restart

### Adding New     Features

1. **Backend API Endpoints:**
   - Add new routes in `backend/app.py`
   - Test with curl or Postman

2. **Frontend Components:**
   - Create new Vue components in `frontend/components/`
   - Import and use in `DashboardApp.js`
   - Update styling in `frontend/styles/dashboard.css`

## 🎨 Customization

### Styling & Themes

**Color Scheme:**
Edit `frontend/styles/dashboard.css` to change colors:
```css
:root {
  --primary-gradient: linear-gradient(135deg, #00D4FF 0%, #8B5CF6 100%);
  --secondary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  /* Add your custom colors */
}
```

**Chart Colors:**
Modify chart colors in component files:
- `SentimentChart.js` - Doughnut chart colors
- `TrendChart.js` - Line chart colors
- `WordCloud.js` - Word cloud color categories

### Analytics

**Adding New Metrics:**
1. Calculate new metrics in `backend/app.py`
2. Add display cards in `MetricsCards.js`
3. Style new cards in `dashboard.css`

## 🐛 Troubleshooting

### Common Issues

**Extension Not Loading:**
- Check that all files are in `frontend/` folder
- Verify `manifest.json` syntax
- Check browser console for errors

**API Connection Failed:**
- Ensure backend server is running on correct port
- Check CORS configuration
- Verify API URL in frontend components

**YouTube Comments Not Loading:**
- Verify YouTube API key is valid
- Check API quota limits
- Ensure video has comments enabled

**Charts Not Displaying:**
- Check browser console for JavaScript errors
- Verify Chart.js and D3.js libraries are loading
- Test with sample data

### Debug Mode

Enable debug logging:
```javascript
// In DashboardApp.js
console.log('Analysis result:', analysisResult);
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create a GitHub issue
- Check the troubleshooting section
- Review Chrome extension development docs

---

**Note:** This extension uses mock sentiment analysis for demonstration. For production use, integrate with a real machine learning model or API service.
