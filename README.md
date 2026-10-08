## Chạy local bằng Docker

Lần đầu, tạo `.env` từ `.env.example` nếu chưa có, sau đó:

```bash
docker compose up -d --build
docker compose exec php composer install
docker compose exec php php artisan key:generate
docker compose exec php php artisan migrate
docker compose exec node npm install
```

Khởi động Vite thủ công và giữ terminal này mở:

```bash
docker compose exec node npm run dev
```

Truy cập ứng dụng tại http://localhost:8000.
Vite dùng cổng `5173`.

PHPUnit dùng database riêng `pplike_testing`, được tạo bởi `docker/postgres/local/init.sql` khi PostgreSQL khởi tạo volume lần đầu. Nếu volume đã tồn tại, chạy script một lần:

```bash
docker compose exec postgres psql -U pplike -d pplike -f /docker-entrypoint-initdb.d/01-testing.sql
docker compose exec php php artisan test
```

```bash
docker compose logs -f php # Xem log backend.
docker compose down        # Dừng các container.
```
