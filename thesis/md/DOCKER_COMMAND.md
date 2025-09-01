# Chạy với hot reload cho development
docker-compose -f docker-compose.dev.yml up --build

# Chạy production build
docker-compose up --build

# Dừng containers
docker-compose down

# Xem logs
docker-compose logs -f

# Xem logs của service cụ thể
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild và chạy lại
docker-compose up --build --force-recreate

# Dọn dẹp containers và images
docker-compose down --volumes --remove-orphans
docker system prune -a