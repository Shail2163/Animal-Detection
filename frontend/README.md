# YOLO Object Detection Frontend

A modern, professional React application for YOLO object detection with a beautiful user interface.

## Features

- 🎯 **Modern UI/UX**: Clean, professional design with smooth animations
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- 🖼️ **Drag & Drop Upload**: Easy image upload with drag and drop support
- ⚡ **Real-time Processing**: Live feedback during image processing
- 🎨 **Beautiful Results**: Elegant display of detection results
- 🔧 **Error Handling**: Comprehensive error handling and user feedback

## Project Structure

```
frontend/
├─ src/
│  ├─ App.jsx              # Main application component
│  ├─ App.css              # Global styles and responsive design
│  ├─ ImageUpload.jsx      # Image upload component with drag & drop
│  ├─ api.js               # API communication and error handling
│  └─ main.jsx             # React application entry point
├─ package.json            # Dependencies and scripts
├─ vite.config.js          # Vite configuration
├─ index.html              # HTML template
└─ README.md              # This file
```

## Getting Started

### Prerequisites

- Node.js (version 16 or higher)
- npm or yarn package manager

### Installation

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser and visit `http://localhost:3000`

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm start` - Alternative start command

## Features Overview

### Image Upload Component
- **Drag & Drop**: Simply drag images onto the upload area
- **File Validation**: Automatic validation of file types and sizes
- **Preview**: Real-time preview of selected images
- **Progress Feedback**: Visual feedback during processing

### Detection Results
- **Visual Results**: Display of processed images with bounding boxes
- **Object Information**: Detailed information about detected objects
- **Confidence Scores**: Confidence levels for each detection
- **Processing Stats**: Image dimensions and processing time

### Responsive Design
- **Mobile First**: Optimized for mobile devices
- **Tablet Support**: Perfect layout on tablet screens
- **Desktop Enhanced**: Rich experience on desktop computers

## API Integration

The frontend communicates with the backend API through the `api.js` module:

- **Base URL**: `http://localhost:8000`
- **Endpoint**: `POST /predict`
- **Timeout**: 30 seconds
- **Error Handling**: Comprehensive error handling with user-friendly messages

## Styling

The application uses modern CSS with:
- **CSS Grid & Flexbox**: For responsive layouts
- **CSS Variables**: For consistent theming
- **Smooth Animations**: For enhanced user experience
- **Glass Morphism**: Modern design effects
- **Gradient Backgrounds**: Beautiful visual appeal

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Development

### Code Structure
- **Components**: Modular React components
- **Styling**: CSS modules with global styles
- **API**: Centralized API communication
- **Error Handling**: Comprehensive error management

### Customization
- **Colors**: Modify CSS variables for different themes
- **Layout**: Adjust grid and flexbox properties
- **Animations**: Customize transition effects
- **API**: Update base URL and endpoints as needed

## Production Build

To create a production build:

```bash
npm run build
```

The built files will be in the `dist` directory, ready for deployment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

