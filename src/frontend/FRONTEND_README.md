# AI Code Detection Frontend

Next.js 15 frontend application for AI-generated code detection system.

## 🎯 Features Implemented

### ✅ Core Components

1. **AnalysisSelector Component**
   - 4 analysis modes: Combined, AST, Human Style, Advanced
   - Real-time API integration
   - Method descriptions and time estimates
   - Dynamic loading states

2. **CodeEditor Component**  
   - Monaco Editor with C/C++ syntax highlighting
   - Language detection and autocomplete
   - Dark/light theme support
   - Real-time analysis submission

3. **ResultsDashboard Component**
   - 5-tab interface: Overview, Features, Charts, Details, Raw Data
   - Comprehensive vs Individual analysis support
   - Interactive progress tracking
   - Export functionality

4. **FeatureCharts Component**
   - Recharts v3 integration (Bar, Line, Radar charts)
   - Chart.js box plot support  
   - Interactive tooltips and legends
   - Responsive design

### ✅ API Integration

- **Complete API Client** (`lib/api-client.ts`)
- **TypeScript Types** (`lib/api-types.ts`)
- **Error Handling** with user-friendly messages
- **Caching Support** for repeated analyses
- **File Upload** support

### ✅ Analysis Methods

1. **Combined Analysis** (80+ features)
   - Complete feature extraction
   - Assessment scoring (0-1 scale)
   - Confidence indicators
   - Key findings summary

2. **Individual Analysis**
   - AST analysis only
   - Human style patterns only
   - Advanced complexity metrics only

### ✅ UI/UX Features

- **Responsive Design** (mobile-friendly)
- **Dark/Light Theme** with system detection
- **Loading States** and progress indicators
- **Error Boundaries** with retry functionality
- **Toast Notifications** for user feedback
- **Export Reports** (JSON format)

## 🏗️ Architecture

```
src/frontend/
├── app/analysis/                 # Analysis page
│   ├── page.tsx                 # Main analysis page
│   └── _components/             # Analysis-specific components
│       ├── analysis-selector.tsx    # Method selection
│       ├── code-editor.tsx         # Monaco editor
│       ├── results-dashboard.tsx   # Results display
│       ├── feature-charts.tsx      # Charts visualization
│       └── header.tsx              # Page header
├── components/ui/               # Shadcn/UI components
├── lib/                        # Utilities and API
│   ├── api-client.ts           # Backend API client
│   ├── api-types.ts            # TypeScript interfaces
│   └── utils.ts                # Utility functions
└── styles/                     # Global styles
```

## 🔧 Technical Stack

- **Framework**: Next.js 15 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4
- **UI Components**: Shadcn/UI (Radix primitives)
- **Code Editor**: Monaco Editor
- **Charts**: Recharts v3 + Chart.js v4
- **State Management**: React hooks
- **HTTP Client**: Fetch API
- **Theme**: next-themes
- **Icons**: Lucide React

## 📊 Visualization Types

### Feature Groups Display

1. **Structure Metrics** → Bar Charts
   - LOC, complexity, control flow
   - Node depth and branching factor

2. **Style Metrics** → Radar Charts  
   - Spacing issues, indentation consistency
   - Naming patterns, formatting quality

3. **Complexity Metrics** → Line Charts
   - Halstead complexity, cognitive load
   - Maintainability index

4. **AI Detection Metrics** → Box Plots
   - Template usage, boilerplate patterns
   - Error handling, over-engineering

## 🔌 API Integration

### Endpoints Used

```typescript
GET  /health                           # Health check
GET  /api/analysis/methods            # Available methods
POST /api/analysis/combined-analysis  # Complete analysis
POST /api/analysis/ast-analysis       # AST only
POST /api/analysis/human-style        # Style only
POST /api/analysis/advanced-features  # Advanced only
POST /api/analysis/upload-file        # File upload
```

### Request Format

```typescript
{
  code: string;        // Source code
  filename?: string;   // Optional filename
  language: string;    // Programming language
}
```

### Response Format

```typescript
{
  success: boolean;
  analysis_id: string;
  timestamp: string;
  code_info: {
    filename: string;
    language: string;
    loc: number;
    file_size: number;
  };
  feature_groups: {
    structure_metrics: FeatureGroup;
    style_metrics: FeatureGroup;
    complexity_metrics: FeatureGroup;
    ai_detection_metrics: FeatureGroup;
  };
  assessment: {
    overall_score: number;  // 0=human-like, 1=AI-like
    confidence: number;
    key_indicators: string[];
    summary: string;
  };
  raw_features?: Record<string, number>;
}
```

## 🚀 Getting Started

### Development Setup

```bash
cd src/frontend

# Install dependencies
npm install

# Set up environment
cp .env.local.example .env.local

# Start development server
npm run dev

# Server will be available at: http://localhost:3000
```

### Environment Variables

```bash
# Required
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional
NEXT_PUBLIC_ENABLE_CHARTS=true
NEXT_PUBLIC_ENABLE_EXPORT=true
NEXT_PUBLIC_MAX_CODE_LENGTH=50000
```

### Building for Production

```bash
# Build the application
npm run build

# Start production server
npm run start

# Or deploy to Vercel/Netlify
```

## 📱 User Interface

### Analysis Workflow

1. **Select Analysis Method**
   - Choose from 4 different analysis types
   - See method descriptions and time estimates

2. **Input Code**
   - Paste code into Monaco editor
   - Or upload .c/.cpp/.txt files
   - Language auto-detection

3. **Run Analysis**
   - Real-time progress indicators
   - Connect to backend API
   - Handle errors gracefully

4. **View Results**
   - Overview with key metrics
   - Feature details with interpretations
   - Interactive charts and visualizations
   - Raw data export

### Responsive Design

- **Desktop**: Full featured interface
- **Tablet**: Optimized layouts
- **Mobile**: Simplified navigation

## 🔍 Analysis Results

### Overview Tab
- High-level assessment summary
- Overall AI likelihood score
- Confidence indicators
- Key findings badges

### Features Tab  
- Grouped feature display
- Individual feature interpretations
- Normalized vs raw values
- Feature importance weights

### Charts Tab
- Interactive visualizations
- Multiple chart types per group
- Hover tooltips with details
- Responsive chart sizing

### Details Tab
- Analysis metadata
- Code information
- Processing timestamps
- Success/error status

### Raw Data Tab
- Complete JSON response
- All extracted features
- Copy/export functionality

## 🎨 Design System

### Colors
- **Primary**: Blue (#3b82f6)
- **Success**: Green (#10b981) 
- **Warning**: Yellow (#f59e0b)
- **Error**: Red (#ef4444)
- **Muted**: Gray (#6b7280)

### Typography
- **Headings**: Inter font family
- **Body**: System font stack
- **Code**: JetBrains Mono

### Components
- Consistent spacing (4px grid)
- Rounded corners (6px default)
- Subtle shadows and borders
- Smooth animations (200ms)

## 🚦 Status

### ✅ Completed Features

- [x] Analysis method selection
- [x] Code editor with syntax highlighting
- [x] API integration with all endpoints
- [x] Results dashboard with 5 tabs
- [x] Interactive charts (Recharts v3)
- [x] Export functionality
- [x] Error handling and loading states
- [x] Responsive design
- [x] Dark/light theme support

### 🚀 Ready for Production

The frontend is **production-ready** with:

- Complete feature implementation
- Comprehensive error handling
- Responsive design for all devices
- API integration with backend
- User-friendly interface
- Performance optimizations

### 🔗 Integration Status

- **Backend**: ✅ Fully integrated
- **Charts**: ✅ Recharts v3 + Chart.js v4
- **File Upload**: ✅ Drag & drop support
- **Export**: ✅ JSON report generation
- **Themes**: ✅ Dark/light mode

## 📝 Next Steps

1. **Start Frontend**: `npm run dev`
2. **Start Backend**: `cd ../backend && make dev`  
3. **Access Application**: http://localhost:3000
4. **Run Analysis**: Upload code and see results!

The frontend is ready to connect with the backend and provide a complete AI code detection experience.