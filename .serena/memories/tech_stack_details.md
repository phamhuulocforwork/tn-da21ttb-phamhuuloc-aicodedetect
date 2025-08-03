# Tech Stack Chi tiết (Cập nhật 2025-01-27)

## Core ML Components (src/src/)
- **Python 3** với pandas==2.3.1 (requirements minimal)
- **Jupyter Notebook** cho data exploration (index.ipynb)
- **Google Gemini API** để sinh code AI
- **Dataset structure**: C/C++ code từ human và AI với metadata
- **Features extraction**: Trích xuất đặc trưng từ source code
- **ML Pipeline**: Đã có output từ training process
- **Model types**: Rule-based và Hybrid models

## Backend API (src/backend/)
- **FastAPI** 0.104.1 - Modern Python web framework
- **uvicorn** 0.24.0 - ASGI server với hot reload
- **python-multipart** 0.0.6 - File upload support
- **CORS middleware** - Cho phép frontend truy cập API
- **Cổng mặc định**: 8000
- **API Documentation**: http://localhost:8000/docs

## Frontend Web App (src/frontend/) - **CẬP NHẬT LỚN**
### Core Framework
- **Next.js 15.3.5** - React framework với App Router
- **React 19** - Latest version với compiler plugin
- **TypeScript 5** - Type safety

### Styling & UI
- **TailwindCSS 4** - Utility-first CSS framework với PostCSS
- **@radix-ui/react-select** 2.2.5 - Accessible component library
- **Framer Motion** 12.23.6 - Animation library
- **Lucide React** 0.525.0 - Icon library
- **Class Variance Authority** 0.7.1 - Styling utilities
- **clsx** 2.1.1 - Conditional classes
- **tailwind-merge** 3.3.1 - Merge Tailwind classes
- **next-themes** 0.4.6 - Theme switching

### Code Editing & Display
- **Monaco Editor** 4.7.0 - VS Code editor component
- **Highlight.js** 11.11.1 - Syntax highlighting
- **@firecms/neat** 0.4.0 - UI component library

### 3D Graphics (Optional)
- **three.js** 0.77.1 - 3D graphics library

### Development Tools - **CẬP NHẬT**
- **ESLint 9** với Next.js config 15.3.5
- **React Compiler Plugin** 19.0.0-beta - React 19 optimization
- **Prettier 3.5.2** với multiple plugins:
  - Sort imports: @trivago/prettier-plugin-sort-imports 5.2.2
  - Organize imports: prettier-plugin-organize-imports 4.1.0
  - TailwindCSS: prettier-plugin-tailwindcss 0.6.11
- **tw-animate-css** 1.3.5 - Animation utilities

### Scripts & Commands
- `dev`: Next.js development với Turbopack
- `build`: Production build
- `preview`: Build và start preview
- `format`: Prettier formatting
- `lint`: ESLint checking
- `clean`: Remove .next
- `clean:all`: Remove .next và node_modules

## Development Environment
- **Node.js**: Hỗ trợ Node 20+
- **Package Manager**: npm với lock file
- **Editor Config**: .editorconfig cho consistent formatting
- **Hot Reload**: Next.js dev server với Turbopack
- **Type Checking**: TypeScript với strict config

## ML/AI Pipeline Status
- **Training**: Đã hoàn thành với Rule-based và Hybrid models
- **Performance**: Cần cải thiện (F1-score = 0.039)
- **Output Format**: JSON reports với detailed metrics
- **Evaluation**: Comprehensive evaluation framework đã setup