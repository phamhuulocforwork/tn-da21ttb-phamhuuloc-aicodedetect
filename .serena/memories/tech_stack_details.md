# Tech Stack Chi tiết

## Core ML Components (src/src/)
- **Python 3** với pandas==2.3.1
- **Jupyter Notebook** cho data exploration (index.ipynb)
- **Google Gemini API** để sinh code AI
- **Dataset structure**: C/C++ code từ human và AI
- **Features extraction**: Trích xuất đặc trưng từ source code

## Backend API (src/backend/)
- **FastAPI** 0.104.1 - Modern Python web framework
- **uvicorn** 0.24.0 - ASGI server với hot reload
- **python-multipart** 0.0.6 - File upload support
- **CORS middleware** - Cho phép frontend truy cập API
- **Cổng mặc định**: 8000
- **API Documentation**: http://localhost:8000/docs

## Frontend Web App (src/frontend/) 
- **Next.js 15.3.5** - React framework với App Router
- **React 19** - Latest version
- **TypeScript 5** - Type safety
- **TailwindCSS 4** - Utility-first CSS framework
- **Radix UI** - Accessible component library
- **Monaco Editor** - Code editor component
- **Framer Motion** - Animation library
- **Lucide React** - Icon library
- **three.js** - 3D graphics (optional)

## Development Tools
- **Node.js**: v22.17.1
- **npm**: 10.9.2  
- **Python**: via uv cache
- **ESLint** + **Prettier** - Code formatting và linting
- **TypeScript** - Type checking