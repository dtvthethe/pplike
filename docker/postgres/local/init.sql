-- Database riêng cho PHPUnit, không dùng database chứa dữ liệu ứng dụng.
-- Chỉ tạo khi chưa tồn tại; \gexec chạy câu lệnh được SELECT trả về trong psql.
SELECT 'CREATE DATABASE pplike_testing'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'pplike_testing')
\gexec
