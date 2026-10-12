---
name: get-spec
description: "Tạo hoặc cập nhật spec Markdown RealWorld từ mã như US_002: tra Method và Endpoint trong my_tasks/ENDPOINTS.md, tìm mục tương ứng trên tài liệu RealWorld và tạo spec kèm response format với liên kết tương đối. Không dùng để triển khai API."
---

# Get Spec

Tạo spec ngắn gọn từ tài liệu RealWorld, giữ cấu trúc tài liệu hiện có trong repository. Spec endpoint và response format là hai file riêng; spec liên kết đến response format trong repository.

## Quy ước mặc định

- Danh mục mã endpoint: `my_tasks/ENDPOINTS.md`.
- Spec endpoint: `my_tasks/<CODE>.md`, ví dụ `my_tasks/US_001.md`.
- Mẫu spec: `my_tasks/AR_004.md`; có thể tham khảo thêm `my_tasks/US_001.md` nếu có.
- Response format: `my_tasks/response_format/<name>.md`.
- Mẫu response format: `my_tasks/response_format/single_article.md`.
- Nguồn endpoint: https://realworld-docs.netlify.app/specifications/backend/endpoints/
- Nguồn response: https://realworld-docs.netlify.app/specifications/backend/api-response-format/

Ưu tiên đường dẫn, mẫu và nguồn do người dùng chỉ định. Các đường dẫn trên tính từ gốc repository đang làm việc, không gắn với một đường dẫn tuyệt đối trên máy.

## Cách thực hiện

1. Nhận đầu vào là mã trong cột `Code`, ví dụ `$get-spec US_002`. Đọc `my_tasks/ENDPOINTS.md`, tìm dòng có mã tương ứng và lấy đúng hai cột `Method`, `Endpoint`. Người dùng chỉ cần cung cấp mã; không yêu cầu nhập thêm method hoặc path nếu đã tra được. Chuẩn hóa method thành chữ hoa và bỏ dấu backtick bao quanh endpoint; giữ nguyên path và placeholder như `:username`. Dùng mã đã tra để đặt tên `my_tasks/<CODE>.md`, rồi đọc các file mẫu. Chỉ hỏi khi mã không tồn tại, có nhiều dòng cùng mã hoặc dòng thiếu thông tin không thể xác định; không tự đặt mã hay suy đoán endpoint từ mã.
2. Mở tài liệu nguồn và tìm mục khớp cả method lẫn path, sau đó mở mục response được liên kết. Mã chỉ là quy ước local để đặt tên file; không tìm mã đó trên website RealWorld. Nếu không truy cập được nguồn và chưa có nội dung nguồn trong phiên làm việc, báo rõ phần thiếu thay vì tự dựng yêu cầu.
3. Tạo hoặc cập nhật spec theo bố cục mẫu: tiêu đề chức năng, khối `http`, request mẫu trong khối `json` nếu nguồn có, yêu cầu xác thực và liên kết response, các trường bắt buộc/tùy chọn hoặc query parameters nếu có.
4. Với response được nguồn chỉ định, tìm file tương ứng trong `response_format` trước. Dùng lại file có cùng schema và ý nghĩa; nếu chưa có thì tạo file chỉ chứa khối `json` theo mẫu `single_article.md`. Dùng tên snake_case mô tả response, ví dụ `user.md`, `single_article.md`, `multiple_articles.md`, `profile.md`. Giữ đúng wrapper, tên trường, kiểu dữ liệu và giá trị mẫu từ nguồn, kể cả `null`.
5. Trong spec, dùng liên kết tương đối đến file response, ví dụ `[User](./response_format/user.md)`. Không để liên kết response trỏ ra website khi đã có thể tạo file local. Endpoint không có response được tài liệu chỉ định thì không tự thêm response.
6. Đối chiếu request, response và yêu cầu với nguồn, rồi chạy script kiểm tra bên dưới để kiểm tra mã/method/path, cú pháp JSON và đích liên kết. Với thay đổi chỉ gồm tài liệu, không cần chạy Docker hay PHPUnit.

## Giảm lượt đọc và gọi tool

- Gộp các lượt đọc local độc lập: dòng mã trong danh mục, spec đích nếu có, mẫu cần dùng và response có khả năng dùng lại. Không cần đọc mọi spec hoặc mọi response.
- Dùng lại mẫu và nội dung nguồn đã đọc trong cùng phiên nếu vẫn đủ thông tin và không có dấu hiệu thay đổi. Nếu đã có đúng mục endpoint và response trong phiên, không mở lại trang hoặc nhấp lại cùng liên kết. File response local cần được kiểm tra trước khi dùng lại.
- Khi cần truy cập web, dùng công cụ đọc web hiện có với output ngắn; tìm đúng mục method/path và chỉ mở đoạn liên quan cùng response được liên kết. Không tìm kiếm web khi đã biết URL nguồn. Nếu công cụ vẫn trả toàn trang, dùng nội dung đó cho các mã tiếp theo trong phiên.
- Không tự tạo cache nguồn lâu dài: nội dung nguồn đã đọc trong phiên đủ cho việc tái sử dụng thông thường. Nếu người dùng yêu cầu bản nguồn local, lưu URL và ngày lấy, đồng thời nói rõ khi dùng bản đó thay cho nguồn trực tuyến.
- Không cần cài MCP, thư viện Python hoặc khởi động Docker cho workflow này.

## Kiểm tra bằng script

Chạy từ gốc repository:

```bash
python3 .agents/skills/get-spec/scripts/check_spec.py US_003
```

Script dùng thư viện chuẩn Python, chỉ đọc file và trả mã thoát khác 0 khi có lỗi. Nó kiểm tra mã duy nhất trong danh mục, method/path trong khối `http`, cú pháp các khối `json`, và các liên kết Markdown tương đối đến file `.md` cùng JSON trong file được liên kết. Script không xác nhận nội dung đúng với RealWorld; vẫn phải đối chiếu schema, giá trị mẫu, xác thực và tham số với nguồn. Endpoint không có request hoặc response vẫn được chấp nhận.

Khi người dùng chỉ định đường dẫn khác, dùng các tùy chọn `--root`, `--catalog`, `--spec` (đường dẫn tương đối tính từ `--root`):

```bash
python3 .agents/skills/get-spec/scripts/check_spec.py US_003 --catalog my_tasks/ENDPOINTS.md --spec my_tasks/US_003.md
```

## Giới hạn nội dung

- Giữ ngôn ngữ và độ chi tiết của mẫu hiện có; với `AR_004.md` và `US_001.md`, nội dung spec dùng tiếng Anh.
- Chỉ đưa vào yêu cầu có trong nguồn. Không tự thêm status code, lỗi đăng nhập, validation, thời hạn token hoặc chi tiết triển khai Laravel.
- Không thêm mục response JSON vào spec endpoint khi đã tách thành file response format.
- Không chỉnh `ENDPOINTS.md`, đánh dấu Done hoặc triển khai API trừ khi người dùng yêu cầu. Tạo spec không có nghĩa endpoint đã được triển khai.
- Khi cập nhật response dùng chung, kiểm tra các spec đang liên kết đến nó; tránh thay đổi schema dành cho endpoint khác.

Ví dụ: `$get-spec US_002` tra dòng `US_002` trong `my_tasks/ENDPOINTS.md` ra `POST /api/users`. Tìm mục Registration trên nguồn bằng cặp method/path này, tạo `my_tasks/US_002.md` và dùng hoặc tạo `my_tasks/response_format/user.md`, liên kết `[User](./response_format/user.md)`. Không tìm chuỗi `US_002` trên website và không yêu cầu người dùng cung cấp thêm Method hoặc Endpoint.
