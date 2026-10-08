import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
        tailwindcss(),
    ],

    // cái server này chỉ có tác dụng khi chạy `npm run dev`, không có tác dụng khi chạy `npm run build`
    // tác dụng là hot reload, tức là khi thay đổi file CSS/JS thì trình duyệt tự load lại mà không cần F5.
    server: {
        // lằng nghe tất cả các địa chỉ IP để trình duyệt trên máy host có thể truy cập được.
        // Nếu Vite chỉ lắng nghe localhost trong container, trình duyệt trên máy host không tải được CSS/JS.
        host: '0.0.0.0', // tương đương `host: true`

        // Chạy Vite trên cổng 5173, khớp với mapping 5173:5173 trong Docker Compose.
        port: 5173,

        // Báo lỗi nếu cổng 5173 bị chiếm; không tự đổi sang cổng khác mà Docker chưa publish.
        strictPort: true,

        // Địa chỉ dùng để tạo URL tài nguyên khi chạy dev, để trình duyệt trên máy host truy cập được.
        // localhost:5173 là cổng Vite được Docker publish ra máy host.
        origin: 'http://localhost:5173',

        watch: {
            // Bỏ qua các file được Laravel/Vite tự sinh và dependencies PHP.
            // Vite đã bỏ qua node_modules và .git theo mặc định.
            ignored: [
                '**/storage/framework/**', // View đã biên dịch, cache và session dạng file.
                '**/storage/logs/**', // Log thay đổi khi ứng dụng xử lý request.
                '**/bootstrap/cache/**', // Cache cấu hình, route và thông tin package.
                '**/vendor/**', // Thư viện được Composer cài đặt.
                '**/public/build/**', // CSS/JS đã được Vite build.
                '**/public/hot', // File chứa địa chỉ Vite dev server.
            ],
        },
    },
});
